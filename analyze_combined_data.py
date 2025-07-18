import pandas as pd
import os
import glob

def analyze_combined_test_data(file_path):
    # Lê o arquivo CSV ignorando a primeira linha e usando a segunda como cabeçalho
    df = pd.read_csv(file_path, skiprows=1)
    
    # Extrai o ID da pessoa do nome do arquivo
    filename = os.path.basename(file_path)
    person_id = filename.split('_')[0]
    
    results = {'id': person_id}
    
    # Verifica se todas as colunas dos 3 testes estão presentes
    test_types = ['T0', 'T1', 'T2']
    missing_tests = []
    
    for test_type in test_types:
        # Seleciona as colunas deste teste
        test_cols = [col for col in df.columns if col.startswith(test_type+'_')]
        if not test_cols:
            missing_tests.append(test_type)
        else:
            test_df = df[test_cols].copy()
            test_df.columns = [col.replace(test_type+'_', '') for col in test_cols]
            
            # Converte apenas as colunas numéricas
            for col in ['step', 'trialtime', 'done', 'tries', 'movimentos_minimos']:
                if col in test_df.columns:
                    test_df[col] = pd.to_numeric(test_df[col], errors='coerce')
            
            # 1. Total de movimentos: conta quantas linhas possuem "step" maior que 0
            total_movements = test_df['step'][test_df['step'] > 0].count() if 'step' in test_df else 0
            # 2. Tempo total em ms: soma os valores de "trialtime" quando "done" = 1
            total_time = test_df['trialtime'][test_df['done'] == 1].sum() if 'trialtime' in test_df and 'done' in test_df else 0
            # 3. Trials completos: numero de linhas com "done" = 1
            completed_trials = test_df['done'][test_df['done'] == 1].count() if 'done' in test_df else 0
            # 4. Movimentos por trial: total_movements / completed_trials
            movements_per_trial = total_movements / completed_trials if completed_trials > 0 else 0
            # 5. Tempo médio por trial: total_time / completed_trials
            avg_time_per_trial = total_time / completed_trials if completed_trials > 0 else 0
            # 6. Tempo por movimento: total_time / total_movements
            time_per_movement = total_time / total_movements if total_movements > 0 else 0
            # 7. Número de tentativas: linhas com tries > 1
            num_attempts = test_df['tries'][test_df['tries'] > 1].count() if 'tries' in test_df else 0
            # 8. Total movimentos mínimos: soma dos valores da coluna movimentos_minimos
            total_min_movements = test_df['movimentos_minimos'].sum() if 'movimentos_minimos' in test_df else 0
            # 9. Movimentos eficiência: total_min_movements / total_movements
            movement_efficiency = total_min_movements / total_movements if total_movements > 0 else 0
            
            # Adiciona os resultados seguindo o padrão de nomenclatura especificado
            results[f'Total_Movimentos_{test_type}'] = total_movements
            results[f'Tempo_Total_ms_{test_type}'] = total_time
            results[f'Movimentos_por_Trial_{test_type}'] = round(movements_per_trial, 2)
            results[f'Tempo_Médio_por_Trial_{test_type}'] = round(avg_time_per_trial, 2)
            results[f'Tempo_por_Movimento_{test_type}'] = round(time_per_movement, 2)
            results[f'Trials_Completos_{test_type}'] = completed_trials
            results[f'Número_de_Tentativas_{test_type}'] = num_attempts
            results[f'Movimentos_totais_{test_type}'] = total_movements
            results[f'Movimentos_minimos_{test_type}'] = total_min_movements
            results[f'Movimentos_eficiencia_{test_type}'] = round(movement_efficiency, 2)
    
    # Retorna None se algum teste estiver faltando
    if missing_tests:
        print(f"Usuário {person_id} não tem todos os testes. Testes faltando: {missing_tests}")
        return None
    
    return results

def get_variable_descriptions():
    """
    Retorna as descrições das variáveis seguindo os padrões do modelo PEBL.
    """
    descriptions = {
        'id': 'Identificador único do participante',
        'Total_Movimentos_T0': 'Total de Movimentos (T0)',
        'Tempo_Total_ms_T0': 'Tempo Total (ms) (T0)',
        'Movimentos_por_Trial_T0': 'Movimentos por Trial (T0)',
        'Tempo_Médio_por_Trial_T0': 'Tempo Médio por Trial (T0)',
        'Tempo_por_Movimento_T0': 'Tempo por Movimento (T0)',
        'Trials_Completos_T0': 'Trials Completos (T0)',
        'Número_de_Tentativas_T0': 'Nº de Tentativas (T0)',
        'Movimentos_totais_T0': 'Movimentos Totais (T0)',
        'Movimentos_minimos_T0': 'Movimentos Mínimos (T0)',
        'Movimentos_eficiencia_T0': 'Eficiência (T0)',
        'Total_Movimentos_T1': 'Total de Movimentos (T1)',
        'Tempo_Total_ms_T1': 'Tempo Total (ms) (T1)',
        'Movimentos_por_Trial_T1': 'Movimentos por Trial (T1)',
        'Tempo_Médio_por_Trial_T1': 'Tempo Médio por Trial (T1)',
        'Tempo_por_Movimento_T1': 'Tempo por Movimento (T1)',
        'Trials_Completos_T1': 'Trials Completos (T1)',
        'Número_de_Tentativas_T1': 'Nº de Tentativas (T1)',
        'Movimentos_totais_T1': 'Movimentos Totais (T1)',
        'Movimentos_minimos_T1': 'Movimentos Mínimos (T1)',
        'Movimentos_eficiencia_T1': 'Eficiência (T1)',
        'Total_Movimentos_T2': 'Total de Movimentos (T2)',
        'Tempo_Total_ms_T2': 'Tempo Total (ms) (T2)',
        'Movimentos_por_Trial_T2': 'Movimentos por Trial (T2)',
        'Tempo_Médio_por_Trial_T2': 'Tempo Médio por Trial (T2)',
        'Tempo_por_Movimento_T2': 'Tempo por Movimento (T2)',
        'Trials_Completos_T2': 'Trials Completos (T2)',
        'Número_de_Tentativas_T2': 'Nº de Tentativas (T2)',
        'Movimentos_totais_T2': 'Movimentos Totais (T2)',
        'Movimentos_minimos_T2': 'Movimentos Mínimos (T2)',
        'Movimentos_eficiencia_T2': 'Eficiência (T2)'
    }
    return descriptions

def main():
    input_folder = 'dados_combinados'
    files = glob.glob(os.path.join(input_folder, '*_combined.csv'))
    
    all_results = []
    excluded_users = []
    
    for file_path in files:
        result = analyze_combined_test_data(file_path)
        if result is not None:
            all_results.append(result)
        else:
            # Extrai o ID do usuário excluído
            filename = os.path.basename(file_path)
            person_id = filename.split('_')[0]
            excluded_users.append(person_id)
    
    if all_results:
        # Cria o DataFrame com todos os resultados
        df_results = pd.DataFrame(all_results)
        
        # Ordena por ID
        df_results = df_results.sort_values('id')
        
        # Salva o resultado em um único arquivo
        output_folder = 'analises_combinadas'
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, 'todos_usuarios_analises.csv')
        
        # Obtém as descrições das variáveis
        descriptions = get_variable_descriptions()
        
        # Cria a linha de descrições
        description_line = ','.join([descriptions.get(col, col) for col in df_results.columns])
        
        # Salva o arquivo com descrições na primeira linha
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.write(description_line + '\n')
            df_results.to_csv(f, index=False)
        
        print(f"Arquivo salvo: {output_file}")
        print(f"Total de usuários processados: {len(all_results)}")
        print(f"Variáveis analisadas: {len(df_results.columns) - 1}")  # -1 para excluir ID
        
        if excluded_users:
            print(f"Usuários excluídos (não completaram todos os testes): {excluded_users}")
    else:
        print("Nenhum usuário completou todos os 3 testes!")

if __name__ == '__main__':
    main() 