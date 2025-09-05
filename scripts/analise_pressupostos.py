import pandas as pd
import pingouin as pg
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, normaltest
import warnings
warnings.filterwarnings('ignore')

def testar_normalidade_eficiencia(df):
    """
    Testa normalidade para eficiência em cada tempo (T0, T1, T2) usando Shapiro-Wilk
    """
    resultados = []
    
    # Colunas de eficiência
    colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
    
    for col in colunas_eficiencia:
        if col not in df.columns:
            continue
            
        # Extrair tempo da coluna
        if col.endswith('_T0'):
            tempo = 'T0'
        elif col.endswith('_T1'):
            tempo = 'T1'
        elif col.endswith('_T2'):
            tempo = 'T2'
        else:
            continue
            
        dados_tempo = df[col].dropna()
        
        # Converter para numérico, ignorando strings
        dados_tempo = pd.to_numeric(dados_tempo, errors='coerce').dropna()
        
        if len(dados_tempo) >= 3:  # Mínimo para Shapiro-Wilk
            stat, p_value = shapiro(dados_tempo)
            resultados.append({
                'Tempo': tempo,
                'n': len(dados_tempo),
                'Shapiro_Stat': stat,
                'Shapiro_p': p_value,
                'Normal': 'Sim' if p_value > 0.05 else 'Não'
            })
        else:
            resultados.append({
                'Tempo': tempo,
                'n': len(dados_tempo),
                'Shapiro_Stat': np.nan,
                'Shapiro_p': np.nan,
                'Normal': 'Dados insuficientes'
            })
    
    return pd.DataFrame(resultados)

def detectar_outliers_eficiencia(df):
    """
    Detecta outliers na eficiência usando IQR e Z-score
    """
    resultados = []
    
    # Colunas de eficiência
    colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
    
    for col in colunas_eficiencia:
        if col not in df.columns:
            continue
            
        # Extrair tempo da coluna
        if col.endswith('_T0'):
            tempo = 'T0'
        elif col.endswith('_T1'):
            tempo = 'T1'
        elif col.endswith('_T2'):
            tempo = 'T2'
        else:
            continue
            
        dados_tempo = df[col].dropna()
        
        # Converter para numérico, ignorando strings
        dados_tempo = pd.to_numeric(dados_tempo, errors='coerce').dropna()
        
        if len(dados_tempo) > 0:
            # Método IQR
            Q1 = dados_tempo.quantile(0.25)
            Q3 = dados_tempo.quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            
            outliers_iqr = dados_tempo[(dados_tempo < limite_inferior) | (dados_tempo > limite_superior)]
            
            # Método Z-score
            if len(dados_tempo) > 1:  # Precisa de pelo menos 2 valores para calcular z-score
                z_scores = np.abs(stats.zscore(dados_tempo))
                outliers_z = dados_tempo[z_scores > 3]
            else:
                outliers_z = pd.Series(dtype=float)
            
            resultados.append({
                'Tempo': tempo,
                'n_total': len(dados_tempo),
                'outliers_IQR': len(outliers_iqr),
                'outliers_Zscore': len(outliers_z),
                'percent_outliers_IQR': (len(outliers_iqr) / len(dados_tempo)) * 100,
                'percent_outliers_Zscore': (len(outliers_z) / len(dados_tempo)) * 100,
                'media': dados_tempo.mean(),
                'desvio_padrao': dados_tempo.std(),
                'min': dados_tempo.min(),
                'max': dados_tempo.max()
            })
    
    return pd.DataFrame(resultados)

def criar_boxplot_eficiencia(df, output_folder='graficos'):
    """
    Cria boxplot para visualizar outliers na eficiência
    """
    # Criar pasta de gráficos se não existir
    Path(output_folder).mkdir(exist_ok=True)
    
    plt.figure(figsize=(12, 8))
    
    # Preparar dados para boxplot
    dados_boxplot = []
    tempos = []
    
    colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
    
    for col in colunas_eficiencia:
        if col not in df.columns:
            continue
            
        # Extrair tempo da coluna
        if col.endswith('_T0'):
            tempo = 'T0'
        elif col.endswith('_T1'):
            tempo = 'T1'
        elif col.endswith('_T2'):
            tempo = 'T2'
        else:
            continue
            
        dados_tempo = df[col].dropna()
        
        # Converter para numérico, ignorando strings
        dados_tempo = pd.to_numeric(dados_tempo, errors='coerce').dropna()
        
        if len(dados_tempo) > 0:
            dados_boxplot.append(dados_tempo)
            tempos.append(tempo)
    
    if dados_boxplot:
        # Criar boxplot
        bp = plt.boxplot(dados_boxplot, labels=tempos, patch_artist=True)
        
        # Colorir os boxes
        colors = ['lightblue', 'lightgreen', 'lightcoral']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        plt.title('Boxplot - Eficiência dos Movimentos', fontsize=16, fontweight='bold')
        plt.xlabel('Tempo de Teste', fontsize=12)
        plt.ylabel('Eficiência dos Movimentos', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Adicionar estatísticas no gráfico
        for i, (tempo, dados) in enumerate(zip(tempos, dados_boxplot)):
            media = dados.mean()
            plt.text(i+1, media, f'Média: {media:.3f}', 
                    ha='center', va='bottom', fontweight='bold')
        
        # Salvar gráfico
        filename = f"{output_folder}/boxplot_eficiencia_movimentos.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   Boxplot salvo: {filename}")
    else:
        print(f"   AVISO: Sem dados suficientes para boxplot de eficiência")

def testar_esfericidade_eficiencia(df, id_column):
    """
    Testa esfericidade para eficiência usando Mauchly's test
    """
    try:
        # Preparar dados para pingouin (converter para formato longo)
        anova_data = []
        
        colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
        
        for idx, row in df.iterrows():
            participant_id = row[id_column]
            
            for col in colunas_eficiencia:
                if col not in df.columns:
                    continue
                    
                # Extrair tempo da coluna
                if col.endswith('_T0'):
                    tempo = 'T0'
                elif col.endswith('_T1'):
                    tempo = 'T1'
                elif col.endswith('_T2'):
                    tempo = 'T2'
                else:
                    continue
                    
                value = row[col]
                
                # Converter para numérico
                try:
                    value = pd.to_numeric(value, errors='coerce')
                    if pd.notna(value):
                        anova_data.append({
                            'participant': participant_id,
                            'time': tempo,
                            'value': value
                        })
                except:
                    continue
        
        anova_df = pd.DataFrame(anova_data)
        
        if len(anova_df) == 0:
            return {'Erro': 'Sem dados válidos'}
        
        # Teste de esfericidade
        sphericity = pg.sphericity(anova_df, dv='value', within='time', subject='participant')
        
        return {
            'Mauchly_W': sphericity['W'][0],
            'Mauchly_p': sphericity['pval'][0],
            'Esferico': 'Sim' if sphericity['pval'][0] > 0.05 else 'Não',
            'Correcao_GG': sphericity['eps'][0],  # Greenhouse-Geisser
            'Correcao_HF': sphericity['eps'][1]   # Huynh-Feldt
        }
    except Exception as e:
        return {
            'Mauchly_W': np.nan,
            'Mauchly_p': np.nan,
            'Esferico': 'Erro',
            'Correcao_GG': np.nan,
            'Correcao_HF': np.nan,
            'Erro': str(e)
        }

def comparacoes_post_hoc_eficiencia(df, id_column):
    """
    Realiza comparações post-hoc para eficiência usando Bonferroni
    """
    try:
        # Preparar dados (converter para formato longo)
        anova_data = []
        
        colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
        
        for idx, row in df.iterrows():
            participant_id = row[id_column]
            
            for col in colunas_eficiencia:
                if col not in df.columns:
                    continue
                    
                # Extrair tempo da coluna
                if col.endswith('_T0'):
                    tempo = 'T0'
                elif col.endswith('_T1'):
                    tempo = 'T1'
                elif col.endswith('_T2'):
                    tempo = 'T2'
                else:
                    continue
                    
                value = row[col]
                
                # Converter para numérico
                try:
                    value = pd.to_numeric(value, errors='coerce')
                    if pd.notna(value):
                        anova_data.append({
                            'participant': participant_id,
                            'time': tempo,
                            'value': value
                        })
                except:
                    continue
        
        anova_df = pd.DataFrame(anova_data)
        
        if len(anova_df) == 0:
            return pd.DataFrame([{'Erro': 'Sem dados válidos'}])
        
        # Comparações post-hoc com Bonferroni
        posthoc = pg.pairwise_ttests(anova_df, dv='value', within='time', subject='participant', 
                                   padjust='bonf')
        
        # Organizar resultados
        resultados = []
        for _, row in posthoc.iterrows():
            resultados.append({
                'Comparacao': f"{row['A']} vs {row['B']}",
                'T_statistic': row['T'],
                'p_value': row['p-unc'],
                'p_corrigido': row['p-corr'],
                'Significativo': 'Sim' if row['p-corr'] < 0.05 else 'Não',
                'Tamanho_efeito': row['cohen-d']
            })
        
        return pd.DataFrame(resultados)
    except Exception as e:
        return pd.DataFrame([{'Erro': str(e)}])

def anova_eficiencia(df, id_column):
    """
    Realiza ANOVA de medidas repetidas para eficiência
    """
    try:
        # Preparar dados (converter para formato longo)
        anova_data = []
        
        colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
        
        for idx, row in df.iterrows():
            participant_id = row[id_column]
            
            for col in colunas_eficiencia:
                if col not in df.columns:
                    continue
                    
                # Extrair tempo da coluna
                if col.endswith('_T0'):
                    tempo = 'T0'
                elif col.endswith('_T1'):
                    tempo = 'T1'
                elif col.endswith('_T2'):
                    tempo = 'T2'
                else:
                    continue
                    
                value = row[col]
                
                # Converter para numérico
                try:
                    value = pd.to_numeric(value, errors='coerce')
                    if pd.notna(value):
                        anova_data.append({
                            'participant': participant_id,
                            'time': tempo,
                            'value': value
                        })
                except:
                    continue
        
        anova_df = pd.DataFrame(anova_data)
        
        if len(anova_df) == 0:
            return {'Erro': 'Sem dados válidos'}
        
        # ANOVA de medidas repetidas
        aov = pg.rm_anova(data=anova_df, dv='value', within='time', subject='participant')
        
        # Extrair resultados
        time_row = aov.loc[aov['Source'] == 'time']
        if time_row.empty:
            return {'Erro': 'Não foi possível encontrar resultados para o fator time'}
        
        p_value = time_row['p-unc'].iloc[0]
        f_value = time_row['F'].iloc[0]
        
        # Calcular partial eta squared
        if 'ng2' in time_row.columns:
            partial_eta_squared = time_row['ng2'].iloc[0]
        else:
            df1 = time_row['ddof1'].iloc[0]
            df2 = time_row['ddof2'].iloc[0]
            partial_eta_squared = (f_value * df1) / (f_value * df1 + df2)
        
        return {
            'F': f_value,
            'p_value': p_value,
            'partial_eta_squared': partial_eta_squared,
            'significativo': 'Sim' if p_value < 0.05 else 'Não',
            'tamanho_efeito': 'Grande' if partial_eta_squared >= 0.14 else 'Médio' if partial_eta_squared >= 0.06 else 'Pequeno'
        }
    except Exception as e:
        return {'Erro': str(e)}

def analise_eficiencia_completa(csv_path, output_path=None, criar_graficos=True):
    """
    Realiza análise completa da eficiência dos movimentos
    
    Args:
        csv_path (str): Caminho para o arquivo CSV
        output_path (str): Caminho para salvar resultados Excel
        criar_graficos (bool): Se deve criar boxplots
    """
    
    print("=== ANÁLISE COMPLETA DA EFICIÊNCIA DOS MOVIMENTOS ===\n")
    
    # 1. Leitura dos dados (pular primeira linha que contém descrições)
    print("1. CARREGANDO DADOS...")
    df = pd.read_csv(csv_path, skiprows=1)
    print(f"Dados carregados: {df.shape[0]} participantes, {df.shape[1]} colunas")
    
    # Identificar coluna de ID
    id_column = 'id'
    if id_column not in df.columns:
        possible_id_cols = [col for col in df.columns if 'participante' in col.lower() or 'id' in col.lower()]
        if possible_id_cols:
            id_column = possible_id_cols[0]
        else:
            raise ValueError("Coluna de ID não encontrada")
    
    print(f"Coluna de ID identificada: {id_column}")
    
    # Verificar se as colunas de eficiência existem
    colunas_eficiencia = ['Movimentos_eficiencia_T0', 'Movimentos_eficiencia_T1', 'Movimentos_eficiencia_T2']
    colunas_existentes = [col for col in colunas_eficiencia if col in df.columns]
    
    if len(colunas_existentes) == 0:
        print("ERRO: Nenhuma coluna de eficiência encontrada!")
        return
    
    print(f"Colunas de eficiência encontradas: {colunas_existentes}")
    
    # Preparar arquivo de saída
    if output_path is None:
        output_path = 'analise_eficiencia_completa.xlsx'
    
    # Criar pasta para gráficos
    if criar_graficos:
        output_folder = 'graficos_eficiencia'
        Path(output_folder).mkdir(exist_ok=True)
        print(f"\nGráficos serão salvos em: {output_folder}/\n")
    
    # 2. ANÁLISE DA EFICIÊNCIA
    print("2. ANALISANDO EFICIÊNCIA DOS MOVIMENTOS")
    print("-" * 50)
    
    # 2.1 Teste de Normalidade
    print("   Testando normalidade...")
    normalidade = testar_normalidade_eficiencia(df)
    if not normalidade.empty:
        print(f"   Resultados normalidade:")
        for _, row in normalidade.iterrows():
            print(f"     {row['Tempo']}: p = {row['Shapiro_p']:.4f} ({row['Normal']})")
    else:
        print("   AVISO: Não foi possível testar normalidade")
    
    # 2.2 Detecção de Outliers
    print("   Detectando outliers...")
    outliers = detectar_outliers_eficiencia(df)
    if not outliers.empty:
        print(f"   Outliers detectados:")
        for _, row in outliers.iterrows():
            print(f"     {row['Tempo']}: {row['outliers_IQR']} outliers ({row['percent_outliers_IQR']:.1f}%)")
            print(f"       Estatísticas: Média={row['media']:.3f}, DP={row['desvio_padrao']:.3f}")
    else:
        print("   AVISO: Não foi possível detectar outliers")
    
    # 2.3 Criar Boxplot
    if criar_graficos:
        print("   Criando boxplot...")
        criar_boxplot_eficiencia(df, output_folder)
    
    # 2.4 ANOVA de Medidas Repetidas
    print("   Realizando ANOVA de medidas repetidas...")
    anova_result = anova_eficiencia(df, id_column)
    if 'Erro' not in anova_result:
        print(f"   ANOVA: F = {anova_result['F']:.3f}, p = {anova_result['p_value']:.4f}")
        print(f"   Tamanho de efeito (η²) = {anova_result['partial_eta_squared']:.4f} ({anova_result['tamanho_efeito']})")
        print(f"   Resultado: {anova_result['significativo']}")
    else:
        print(f"   ERRO: {anova_result['Erro']}")
    
    # 2.5 Teste de Esfericidade
    print("   Testando esfericidade...")
    esfericidade = testar_esfericidade_eficiencia(df, id_column)
    if 'Erro' not in esfericidade:
        print(f"   Esfericidade: p = {esfericidade['Mauchly_p']:.4f} ({esfericidade['Esferico']})")
        print(f"   Correção GG: {esfericidade['Correcao_GG']:.3f}")
        print(f"   Correção HF: {esfericidade['Correcao_HF']:.3f}")
    else:
        print(f"   ERRO: {esfericidade['Erro']}")
    
    # 2.6 Comparações Post-hoc
    print("   Realizando comparações post-hoc...")
    posthoc = comparacoes_post_hoc_eficiencia(df, id_column)
    if not posthoc.empty and 'Comparacao' in posthoc.columns:
        print("   Comparações post-hoc:")
        for _, row in posthoc.iterrows():
            print(f"     {row['Comparacao']}: p = {row['p_corrigido']:.4f} ({row['Significativo']})")
            print(f"       Tamanho de efeito (Cohen's d) = {row['Tamanho_efeito']:.3f}")
    else:
        print("   AVISO: Não foi possível realizar comparações post-hoc")
    
    # 3. SALVAR RESULTADOS
    print("\n3. SALVANDO RESULTADOS...")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Resumo geral
        resumo_geral = pd.DataFrame({
            'Analise': ['Normalidade_T0', 'Normalidade_T1', 'Normalidade_T2', 
                       'ANOVA_F', 'ANOVA_p', 'ANOVA_eta2', 'ANOVA_significativo',
                       'Esfericidade_p', 'Esfericidade_resultado'],
            'Valor': [
                normalidade.loc[0, 'Shapiro_p'] if len(normalidade) > 0 else np.nan,
                normalidade.loc[1, 'Shapiro_p'] if len(normalidade) > 1 else np.nan,
                normalidade.loc[2, 'Shapiro_p'] if len(normalidade) > 2 else np.nan,
                anova_result.get('F', np.nan),
                anova_result.get('p_value', np.nan),
                anova_result.get('partial_eta_squared', np.nan),
                anova_result.get('significativo', 'Erro'),
                esfericidade.get('Mauchly_p', np.nan),
                esfericidade.get('Esferico', 'Erro')
            ]
        })
        resumo_geral.to_excel(writer, sheet_name='Resumo_Geral', index=False)
        
        # Detalhes de normalidade
        if not normalidade.empty:
            normalidade.to_excel(writer, sheet_name='Normalidade', index=False)
        
        # Detalhes de outliers
        if not outliers.empty:
            outliers.to_excel(writer, sheet_name='Outliers', index=False)
        
        # Comparações post-hoc
        if not posthoc.empty and 'Comparacao' in posthoc.columns:
            posthoc.to_excel(writer, sheet_name='PostHoc', index=False)
    
    print(f"\nAnálise completa salva em: {output_path}")
    if criar_graficos:
        print(f"Gráfico salvo em: {output_folder}/")
    
    return output_path

def main():
    """
    Função principal
    """
    csv_path = '03_analises_combinadas/todos_usuarios_analises.csv'
    
    if not Path(csv_path).exists():
        print(f"ERRO: Arquivo não encontrado: {csv_path}")
        print("Por favor, execute primeiro o pipeline principal.")
        return
    
    print("Este script analisa especificamente a EFICIÊNCIA DOS MOVIMENTOS.")
    print("Inclui:")
    print("- Teste de normalidade (Shapiro-Wilk)")
    print("- Detecção de outliers (IQR e Z-score)")
    print("- Boxplot para visualização")
    print("- ANOVA de medidas repetidas")
    print("- Teste de esfericidade (Mauchly)")
    print("- Comparações post-hoc (Bonferroni)")
    print()
    
    analise_eficiencia_completa(csv_path, criar_graficos=True)

if __name__ == "__main__":
    main()