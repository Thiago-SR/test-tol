import pandas as pd
import pingouin as pg
import numpy as np
from pathlib import Path

def realizar_anova_medidas_repetidas(csv_path, output_path=None):
    """
    Realiza ANOVA de medidas repetidas para todas as variáveis em um arquivo CSV.
    
    Args:
        csv_path (str): Caminho para o arquivo CSV com os dados
        output_path (str): Caminho para salvar o arquivo Excel com resultados (opcional)
    
    Returns:
        pd.DataFrame: DataFrame com os resultados das ANOVAs
    """
    
    # 1. Leitura do arquivo CSV
    print("Lendo arquivo CSV...")
    # Ler o arquivo pulando a primeira linha (cabeçalho descritivo)
    df = pd.read_csv(csv_path, skiprows=1)
    print(f"Dados carregados: {df.shape[0]} participantes, {df.shape[1]} colunas")
    
    # Identificar a coluna de ID
    id_column = 'id'  # Assumindo que a coluna se chama 'id'
    if id_column not in df.columns:
        # Tentar encontrar coluna de ID
        possible_id_cols = [col for col in df.columns if 'id' in col.lower() or 'participante' in col.lower()]
        if possible_id_cols:
            id_column = possible_id_cols[0]
            print(f"Coluna de ID identificada: {id_column}")
        else:
            raise ValueError("Não foi possível encontrar a coluna de ID")
    
    # 2. Identificar variáveis e momentos de teste
    print("\nIdentificando variáveis...")
    
    # Encontrar todas as colunas que terminam com _T0, _T1, _T2
    time_suffixes = ['_T0', '_T1', '_T2']
    variable_groups = {}
    
    for col in df.columns:
        if col == id_column:
            continue
            
        for suffix in time_suffixes:
            if col.endswith(suffix):
                # Extrair o nome da variável (removendo o sufixo)
                variable_name = col[:-3]  # Remove _T0, _T1, _T2
                
                if variable_name not in variable_groups:
                    variable_groups[variable_name] = []
                
                variable_groups[variable_name].append(col)
                break
    
    print(f"Encontradas {len(variable_groups)} variáveis para análise:")
    for var_name, cols in variable_groups.items():
        print(f"  - {var_name}: {len(cols)} colunas ({', '.join(cols)})")
    
    # 3. Realizar ANOVA para cada variável
    print("\nRealizando ANOVAs de medidas repetidas...")
    resultados = []
    
    for variable_name, columns in variable_groups.items():
        print(f"\nAnalisando: {variable_name}")
        
        # Verificar se temos as 3 colunas necessárias (T0, T1, T2)
        if len(columns) != 3:
            print(f"  AVISO: Variável {variable_name} não tem exatamente 3 momentos. Pulando...")
            continue
        
        # Mostrar as colunas que serão analisadas
        print(f"  Colunas: {columns}")
        
        # Preparar dados para ANOVA
        # Criar DataFrame no formato longo (long format) necessário para pingouin
        anova_data = []
        
        for idx, row in df.iterrows():
            participant_id = row[id_column]
            
            # Adicionar dados para cada momento
            for i, col in enumerate(columns):
                value = row[col]
                if pd.notna(value):  # Ignorar valores NaN
                    anova_data.append({
                        'participant': participant_id,
                        'time': f'T{i}',  # T0, T1, T2
                        'value': value
                    })
        
        anova_df = pd.DataFrame(anova_data)
        
        if len(anova_df) == 0:
            print(f"  AVISO: Nenhum dado válido para {variable_name}. Pulando...")
            continue
        
        # Mostrar informações sobre os dados
        print(f"  Dados preparados: {len(anova_df)} observações")
        print(f"  Valores únicos por momento: {anova_df['time'].value_counts().to_dict()}")
        
        # Verificar se há variabilidade nos dados
        if anova_df['value'].std() == 0:
            print(f"  AVISO: Sem variabilidade nos dados para {variable_name}. Pulando...")
            continue
        
        try:
            # Realizar ANOVA de medidas repetidas
            aov = pg.rm_anova(data=anova_df, dv='value', within='time', subject='participant')
            
            # Verificar se a ANOVA foi bem-sucedida
            if aov.empty or 'time' not in aov['Source'].values:
                raise ValueError("ANOVA não retornou resultados válidos")
            
            # Extrair resultados
            time_row = aov.loc[aov['Source'] == 'time']
            if time_row.empty:
                raise ValueError("Não foi possível encontrar resultados para o fator 'time'")
            
            p_value = time_row['p-unc'].iloc[0]
            f_value = time_row['F'].iloc[0]
            
            # Calcular partial eta squared (tamanho de efeito)
            # Usar a coluna 'ng2' que é o partial eta squared calculado pelo pingouin
            if 'ng2' in time_row.columns:
                partial_eta_squared = time_row['ng2'].iloc[0]
            else:
                # Fallback: calcular usando F e graus de liberdade
                df1 = time_row['ddof1'].iloc[0]
                df2 = time_row['ddof2'].iloc[0]
                partial_eta_squared = (f_value * df1) / (f_value * df1 + df2)
            
            # Adicionar resultado
            resultados.append({
                'Variavel': variable_name,
                'F': f_value,
                'p_value': p_value,
                'partial_eta_squared': partial_eta_squared,
                'significancia': 'Sim' if p_value < 0.05 else 'Não',
                'tamanho_efeito': 'Grande' if partial_eta_squared >= 0.14 else 'Médio' if partial_eta_squared >= 0.06 else 'Pequeno'
            })
            
            print(f"  OK: ANOVA concluída - p = {p_value:.4f}, η² = {partial_eta_squared:.4f}")
            
        except Exception as e:
            print(f"  ERRO: Erro na ANOVA para {variable_name}: {str(e)}")
            # Adicionar resultado com erro
            resultados.append({
                'Variavel': variable_name,
                'F': np.nan,
                'p_value': np.nan,
                'partial_eta_squared': np.nan,
                'significancia': 'Erro',
                'tamanho_efeito': 'Erro'
            })
    
    # 4️⃣ Criar DataFrame com resultados
    resultados_df = pd.DataFrame(resultados)
    
    # Ordenar por p-value (menor primeiro)
    resultados_df = resultados_df.sort_values('p_value', na_position='last')
    
    print(f"\nResumo dos resultados:")
    print(f"Total de variáveis analisadas: {len(resultados_df)}")
    print(f"Variáveis significativas (p < 0.05): {len(resultados_df[resultados_df['significancia'] == 'Sim'])}")
    
    # 5. Exportar para Excel
    if output_path is None:
        output_path = 'resultados_anova_medidas_repetidas.xlsx'
    
    print(f"\nSalvando resultados em: {output_path}")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Planilha principal com resultados
        resultados_df.to_excel(writer, sheet_name='Resultados_ANOVA', index=False)
        
        # Planilha com estatísticas descritivas
        descritivas = []
        for variable_name, columns in variable_groups.items():
            if len(columns) == 3:
                stats = df[columns].describe()
                stats.index.name = 'Estatistica'
                stats.columns = ['T0', 'T1', 'T2']
                descritivas.append((variable_name, stats))
        
        # Criar planilhas com estatísticas descritivas
        if descritivas:
            for var_name, stats in descritivas:
                sheet_name = f'Desc_{var_name[:25]}'  # Limitar nome da planilha
                stats.to_excel(writer, sheet_name=sheet_name)
    
    print(f"Análise concluída! Resultados salvos em: {output_path}")
    
    return resultados_df

def main():
    """
    Função principal para executar a análise
    """
    # Caminho para o arquivo CSV
    csv_path = '03_analises_combinadas/todos_usuarios_analises.csv'
    
    # Verificar se o arquivo existe
    if not Path(csv_path).exists():
        print(f"ERRO: Arquivo não encontrado: {csv_path}")
        print("Por favor, verifique o caminho do arquivo CSV.")
        return
    
    # Executar análise
    resultados = realizar_anova_medidas_repetidas(csv_path)
    
    # Mostrar resultados principais
    print("\n" + "="*80)
    print("RESULTADOS PRINCIPAIS")
    print("="*80)
    
    # Mostrar variáveis significativas
    significativas = resultados[resultados['significancia'] == 'Sim']
    if len(significativas) > 0:
        print(f"\nVariáveis com diferenças significativas (p < 0.05):")
        for _, row in significativas.iterrows():
            print(f"  • {row['Variavel']}: p = {row['p_value']:.4f}, η² = {row['partial_eta_squared']:.4f}")
    else:
        print("\nAVISO: Nenhuma variável apresentou diferenças significativas.")
    
    # Mostrar variáveis com maior tamanho de efeito
    grandes_efeitos = resultados[resultados['tamanho_efeito'] == 'Grande']
    if len(grandes_efeitos) > 0:
        print(f"\nVariáveis com grande tamanho de efeito (η² ≥ 0.14):")
        for _, row in grandes_efeitos.iterrows():
            print(f"  • {row['Variavel']}: η² = {row['partial_eta_squared']:.4f}")

if __name__ == "__main__":
    main()
