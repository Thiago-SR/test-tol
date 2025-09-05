#!/usr/bin/env python3
"""
Script principal para executar todo o pipeline de processamento de dados de testes TOL.

Este script executa todos os scripts na ordem correta:
1. process_all_files.py - Processa os dados originais e calcula pontuações
2. combine_user_data.py - Combina dados de diferentes testes por usuário
3. analyze_combined_data.py - Analisa dados combinados
4. analyze_outcomes.py - Analisa resultados individuais

Autor: Sistema de Processamento TOL
Data: 2025
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_script(script_name, description):
    """
    Executa um script Python e retorna True se bem-sucedido.
    
    Args:
        script_name: Nome do script a ser executado
        description: Descrição do que o script faz
        
    Returns:
        bool: True se o script foi executado com sucesso
    """
    script_path = os.path.join('scripts', script_name)
    
    if not os.path.exists(script_path):
        logging.error(f"Script não encontrado: {script_path}")
        return False
    
    logging.info(f"Executando: {description}")
    logging.info(f"Script: {script_name}")
    
    try:
        # Executa o script
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=300  # Timeout de 5 minutos
        )
        
        if result.returncode == 0:
            logging.info(f"[OK] {description} - Concluído com sucesso")
            if result.stdout:
                logging.info(f"Saída: {result.stdout}")
            return True
        else:
            logging.error(f"[ERRO] {description} - Falhou com código {result.returncode}")
            if result.stderr:
                logging.error(f"Erro: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"[ERRO] {description} - Timeout (5 minutos)")
        return False
    except Exception as e:
        logging.error(f"[ERRO] {description} - Erro inesperado: {e}")
        return False

def check_prerequisites():
    """
    Verifica se os pré-requisitos estão atendidos.
    
    Returns:
        bool: True se todos os pré-requisitos estão OK
    """
    logging.info("Verificando pré-requisitos...")
    
    # Verifica se a pasta de dados originais existe
    dados_originais = Path("dados_originais")
    if not dados_originais.exists():
        logging.error("Pasta 'dados_originais' não encontrada!")
        return False
    
    # Verifica se há arquivos CSV na pasta de dados originais
    csv_files = list(dados_originais.glob("*.csv"))
    if not csv_files:
        logging.error("Nenhum arquivo CSV encontrado na pasta 'dados_originais'!")
        return False
    
    logging.info(f"[OK] Encontrados {len(csv_files)} arquivos CSV na pasta 'dados_originais'")
    
    # Verifica se a pasta scripts existe
    scripts_folder = Path("scripts")
    if not scripts_folder.exists():
        logging.error("Pasta 'scripts' não encontrada!")
        return False
    
    # Verifica se todos os scripts necessários existem
    required_scripts = [
        "process_all_files.py",
        "combine_user_data.py", 
        "analyze_combined_data.py",
        "anova.py"
    ]
    
    for script in required_scripts:
        script_path = scripts_folder / script
        if not script_path.exists():
            logging.error(f"Script obrigatório não encontrado: {script}")
            return False
    
    logging.info("[OK] Todos os scripts necessários estão presentes")
    logging.info("[OK] Pré-requisitos atendidos")
    return True

def main():
    """
    Função principal que executa todo o pipeline.
    """
    start_time = time.time()
    
    logging.info("=" * 60)
    logging.info("INICIANDO PIPELINE DE PROCESSAMENTO TOL")
    logging.info("=" * 60)
    
    # Verifica pré-requisitos
    if not check_prerequisites():
        logging.error("Pré-requisitos não atendidos. Abortando execução.")
        sys.exit(1)
    
    # Define a sequência de execução dos scripts
    pipeline_steps = [
        {
            "script": "process_all_files.py",
            "description": "Processamento de dados originais e cálculo de pontuações"
        },
        {
            "script": "combine_user_data.py", 
            "description": "Combinação de dados por usuário"
        },
        {
            "script": "analyze_combined_data.py",
            "description": "Análise de dados combinados"
        },
        {
            "script": "anova.py",
            "description": "Análise estatística ANOVA de medidas repetidas"
        }
    ]
    
    # Executa cada etapa do pipeline
    successful_steps = 0
    total_steps = len(pipeline_steps)
    
    for i, step in enumerate(pipeline_steps, 1):
        logging.info(f"\n--- ETAPA {i}/{total_steps} ---")
        
        if run_script(step["script"], step["description"]):
            successful_steps += 1
        else:
            logging.error(f"Falha na etapa {i}. Interrompendo pipeline.")
            break
    
    # Resumo final
    end_time = time.time()
    execution_time = end_time - start_time
    
    logging.info("\n" + "=" * 60)
    logging.info("RESUMO DA EXECUÇÃO")
    logging.info("=" * 60)
    logging.info(f"Etapas executadas com sucesso: {successful_steps}/{total_steps}")
    logging.info(f"Tempo total de execução: {execution_time:.2f} segundos")
    
    if successful_steps == total_steps:
        logging.info("[OK] PIPELINE CONCLUÍDO COM SUCESSO!")
        logging.info("\nArquivos gerados:")
        logging.info("  - 01_dados_processados/ - Dados processados com pontuações")
        logging.info("  - 02_dados_combinados/ - Dados combinados por usuário")
        logging.info("  - 03_analises_combinadas/ - Análises dos dados combinados")
        logging.info("  - resultados_anova_medidas_repetidas.xlsx - Análise estatística ANOVA")
        sys.exit(0)
    else:
        logging.error("[ERRO] PIPELINE INTERROMPIDO COM FALHAS")
        sys.exit(1)

if __name__ == "__main__":
    main()
