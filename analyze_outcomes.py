import pandas as pd
import os
import glob
from collections import defaultdict

def analyze_test_data(file_path):
    """
    Analisa um arquivo de teste e retorna as métricas calculadas
    """
    # Lê o arquivo CSV
    df = pd.read_csv(file_path)
    
    # Extrai o ID da pessoa e tipo de teste do nome do arquivo
    filename = os.path.basename(file_path)
    test_type = filename.split('_')[0]  # T0, T1, T2
    person_id = filename.split('_')[1]  # 4567, 4568, etc.
    
    # Calcula as métricas solicitadas
    
    # 1. Total de movimentos: conta quantas linhas possuem "step" maior que 0
    total_movements = len(df[df['step'] > 0])
    
    # 2. Tempo total em ms: soma os valores de "trialtime" quando "done" = 1
    total_time = df[df['done'] == 1]['trialtime'].sum()
    
    # 3. Trials completos: numero de linhas com "done" = 1
    completed_trials = len(df[df['done'] == 1])
    
    # 4. Movimentos por trial: divide o total de movimentos pelo numero de linhas com "done" = 1
    movements_per_trial = total_movements / completed_trials if completed_trials > 0 else 0
    
    # 5. Tempo medio por trial: divide o tempo total pelo numero de linhas com "done" = 1
    avg_time_per_trial = total_time / completed_trials if completed_trials > 0 else 0
    
    # 6. Tempo por movimento: tempo total dividido pelo total de movimentos
    time_per_movement = total_time / total_movements if total_movements > 0 else 0
    
    # 7. Numero de tentativas: conta quantas linhas possuem "tries" > 1
    num_attempts = len(df[df['tries'] > 1])
    
    # 8. Total movimentos mínimos: soma dos valores da coluna movimentos_minimos
    total_min_movements = df['movimentos_minimos'].sum()
    
    # 9. Movimentos eficiencia: total movimentos minimos dividido pelo total de movimentos
    movement_efficiency = total_min_movements / total_movements if total_movements > 0 else 0
    
    return {
        'person_id': person_id,
        'test_type': test_type,
        'total_movements': total_movements,
        'total_time_ms': total_time,
        'completed_trials': completed_trials,
        'movements_per_trial': movements_per_trial,
        'avg_time_per_trial': avg_time_per_trial,
        'time_per_movement': time_per_movement,
        'num_attempts': num_attempts,
        'total_min_movements': total_min_movements,
        'movement_efficiency': movement_efficiency
    }

def process_all_files():
    """
    Processa todos os arquivos da pasta resultados_processados
    """
    # Pasta com os arquivos processados
    input_folder = 'resultados_processados'
    
    # Dicionário para armazenar resultados por pessoa
    results_by_person = defaultdict(list)
    
    # Lista todos os arquivos CSV na pasta
    csv_files = glob.glob(os.path.join(input_folder, '*.csv'))
    
    print(f"Encontrados {len(csv_files)} arquivos para processar...")
    
    # Processa cada arquivo
    for file_path in csv_files:
        try:
            result = analyze_test_data(file_path)
            person_id = result['person_id']
            results_by_person[person_id].append(result)
            print(f"Processado: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
    
    # Cria pasta de saída se não existir
    output_folder = 'analises_resultados'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Cria arquivo de saída para cada pessoa
    for person_id, results in results_by_person.items():
        if len(results) == 3:  # Deve ter 3 testes (T0, T1, T2)
            # Ordena por tipo de teste (T0, T1, T2)
            results.sort(key=lambda x: x['test_type'])
            
            # Cria DataFrame com os resultados
            df_results = pd.DataFrame(results)
            
            # Reorganiza as colunas para melhor visualização
            columns_order = [
                'test_type', 'total_movements', 'total_time_ms', 'completed_trials',
                'movements_per_trial', 'avg_time_per_trial', 'time_per_movement',
                'num_attempts', 'total_min_movements', 'movement_efficiency'
            ]
            
            df_results = df_results[columns_order]
            
            # Formata os valores numéricos com casas decimais apropriadas
            # Valores inteiros
            df_results['total_movements'] = df_results['total_movements'].astype(int)
            df_results['total_time_ms'] = df_results['total_time_ms'].astype(int)
            df_results['completed_trials'] = df_results['completed_trials'].astype(int)
            df_results['num_attempts'] = df_results['num_attempts'].astype(int)
            df_results['total_min_movements'] = df_results['total_min_movements'].astype(int)
            
            # Valores decimais com 2 casas
            df_results['movements_per_trial'] = df_results['movements_per_trial'].round(2)
            df_results['avg_time_per_trial'] = df_results['avg_time_per_trial'].round(2)
            df_results['time_per_movement'] = df_results['time_per_movement'].round(2)
            df_results['movement_efficiency'] = df_results['movement_efficiency'].round(2)
            
            # Salva o arquivo
            output_file = os.path.join(output_folder, f'{person_id}_analises.csv')
            df_results.to_csv(output_file, index=False)
            print(f"Arquivo criado: {output_file}")
        else:
            print(f"Aviso: Pessoa {person_id} tem {len(results)} testes (esperado 3)")

if __name__ == "__main__":
    process_all_files()
    print("\nProcessamento concluído!") 