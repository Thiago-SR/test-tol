import pandas as pd
import os
import glob

def analyze_combined_test_data(file_path):
    # Lê o arquivo CSV ignorando a primeira linha e usando a segunda como cabeçalho
    df = pd.read_csv(file_path, skiprows=1)
    
    # Extrai o ID da pessoa do nome do arquivo
    filename = os.path.basename(file_path)
    person_id = filename.split('_')[0]
    
    results = []
    
    for test_type in ['T0', 'T1', 'T2']:
        # Seleciona as colunas deste teste
        test_cols = [col for col in df.columns if col.startswith(test_type+'_')]
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
        
        results.append({
            'teste': test_type,
            'total_movimentos': total_movements,
            'tempo_total_ms': total_time,
            'trials_completos': completed_trials,
            'movimentos_por_trial': round(movements_per_trial, 2),
            'tempo_medio_por_trial': round(avg_time_per_trial, 2),
            'tempo_por_movimento': round(time_per_movement, 2),
            'num_tentativas': num_attempts,
            'total_movimentos_minimos': total_min_movements,
            'eficiencia_movimentos': round(movement_efficiency, 2)
        })
    
    # Salva o resultado
    output_folder = 'analises_combinadas'
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f'{person_id}_analises.csv')
    pd.DataFrame(results).to_csv(output_file, index=False)

def main():
    input_folder = 'dados_combinados'
    files = glob.glob(os.path.join(input_folder, '*_combined.csv'))
    for file_path in files:
        analyze_combined_test_data(file_path)

if __name__ == '__main__':
    main() 