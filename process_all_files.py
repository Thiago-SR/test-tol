import pandas as pd
from collections import deque
import copy
import logging
from typing import List, Tuple, Set, Optional
import os
import glob
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constantes
NUM_PINOS = 3
PONTUACAO_INICIAL = 10
PONTUACAO_MINIMA = 0

class EstadoInvalidoError(Exception):
    """Exceção lançada quando um estado é inválido."""
    pass

def string_para_estado(s: str) -> List[List[str]]:
    """
    Converte uma string no formato '|A|B|C|' para uma lista de listas representando o estado.
    
    Args:
        s: String no formato '|A|B|C|' onde cada letra representa uma bola
        
    Returns:
        Lista de listas representando o estado dos pinos
        
    Raises:
        EstadoInvalidoError: Se a string não estiver no formato correto
    """
    if not s or not s.startswith('|'):
        raise EstadoInvalidoError("String de estado deve começar com '|'")
        
    partes = s.split('|')[1:]  # Remove o primeiro item vazio antes do primeiro '|'
    
    # Remove o último elemento vazio apenas se ele for causado por um '|' final extra
    if len(partes) > 0 and partes[-1] == '':
        partes = partes[:-1]
    
    return [list(pino) for pino in partes]

def estado_para_tupla(estado: List[List[str]]) -> Tuple[Tuple[str, ...], ...]:
    """
    Transforma um estado em uma tupla imutável para poder usar em sets.
    
    Args:
        estado: Lista de listas representando o estado dos pinos
        
    Returns:
        Tupla de tuplas representando o estado
    """
    return tuple(tuple(pino) for pino in estado)

def movimentos_possiveis(estado: List[List[str]], altura_max: int) -> List[List[List[str]]]:
    """
    Gera todos os próximos estados válidos a partir do estado atual.
    
    Args:
        estado: Estado atual dos pinos
        altura_max: Altura máxima permitida para cada pino
        
    Returns:
        Lista de estados possíveis após um movimento
    """
    estados = []
    for i in range(len(estado)):
        if not estado[i]:  # Pula pinos vazios
            continue
        bola = estado[i][-1]
        for j in range(len(estado)):
            if i != j and len(estado[j]) < altura_max:
                novo_estado = copy.deepcopy(estado)
                novo_estado[i].pop()
                novo_estado[j].append(bola)
                estados.append(novo_estado)
    return estados

def normalizar_estados(estado_inicial: List[List[str]], estado_final: List[List[str]]) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Normaliza o tamanho dos estados para que tenham exatamente 3 pinos.
    
    Args:
        estado_inicial: Estado inicial dos pinos
        estado_final: Estado final dos pinos
        
    Returns:
        Tupla contendo os estados normalizados
        
    Raises:
        EstadoInvalidoError: Se os estados não puderem ser normalizados
    """
    # Verifica se o estado inicial tem menos de 3 pinos e adiciona pinos vazios
    while len(estado_inicial) < NUM_PINOS:
        estado_inicial.append([])

    # Verifica se o estado final tem menos de 3 pinos e adiciona pinos vazios
    while len(estado_final) < NUM_PINOS:
        estado_final.append([])

    # Garante que ambos os estados tenham exatamente 3 pinos
    if len(estado_inicial) != NUM_PINOS or len(estado_final) != NUM_PINOS:
        raise EstadoInvalidoError("Erro na normalização: o estado não tem exatamente 3 pinos!")

    return estado_inicial, estado_final

def movimentos_minimos(estado_inicial: List[List[str]], estado_objetivo: List[List[str]], altura_max: int) -> int:
    """
    Calcula a quantidade mínima de movimentos necessários para atingir o estado objetivo.
    
    Args:
        estado_inicial: Estado inicial dos pinos
        estado_objetivo: Estado objetivo dos pinos
        altura_max: Altura máxima permitida para cada pino
        
    Returns:
        Número mínimo de movimentos necessários, ou -1 se for impossível
    """
    # Verifica se o número total de bolas é igual
    total_bolas_inicial = sum(len(pino) for pino in estado_inicial)
    total_bolas_objetivo = sum(len(pino) for pino in estado_objetivo)
    if total_bolas_inicial != total_bolas_objetivo:
        return -1

    # Verifica se algum pino excede a altura máxima
    for pino in estado_inicial:
        if len(pino) > altura_max:
            return -1
    
    for pino in estado_objetivo:
        if len(pino) > altura_max:
            return -1

    # Verifica se o estado inicial e final são iguais
    if estado_para_tupla(estado_inicial) == estado_para_tupla(estado_objetivo):
        return 0

    visitados = {}  # Dicionário para armazenar estados e seus passos
    fila = deque([(estado_inicial, 0)])
    max_movimentos = 1000  # Limite máximo de movimentos para evitar loops infinitos

    while fila:
        estado_atual, passos = fila.popleft()
        estado_tupla = estado_para_tupla(estado_atual)
        
        if passos > max_movimentos:
            logging.warning("Limite máximo de movimentos atingido")
            return -1
            
        if estado_tupla in visitados and visitados[estado_tupla] <= passos:
            continue
            
        visitados[estado_tupla] = passos

        if estado_tupla == estado_para_tupla(estado_objetivo):
            return passos

        for prox in movimentos_possiveis(estado_atual, altura_max):
            # Verifica se o próximo estado excede a altura máxima
            if any(len(pino) > altura_max for pino in prox):
                continue
                
            prox_tupla = estado_para_tupla(prox)
            if prox_tupla not in visitados or visitados[prox_tupla] > passos + 1:
                fila.append((prox, passos + 1))

    return -1

def calcular_pontuacao(row: pd.Series, min_movs: int) -> int:
    """
    Calcula a pontuação baseada na diferença entre movimentos feitos e mínimos.
    
    Args:
        row: Linha do DataFrame com os dados do jogo
        min_movs: Número mínimo de movimentos necessários
        
    Returns:
        Pontuação calculada
    """
    if (row['done'] != 1) or min_movs == -1:
        return 0  # Nenhuma pontuação se não acertou

    extra_movs = row['step'] - min_movs
    pontuacao = max(PONTUACAO_MINIMA, PONTUACAO_INICIAL - extra_movs)

    return pontuacao

def processar_arquivo(caminho_entrada: str, caminho_saida: str) -> None:
    """
    Processa o arquivo de entrada e gera o arquivo de saída com as pontuações.
    
    Args:
        caminho_entrada: Caminho do arquivo de entrada
        caminho_saida: Caminho do arquivo de saída
    """
    try:
        df = pd.read_csv(caminho_entrada, sep=',')
    except Exception as e:
        logging.error(f"Erro ao ler arquivo de entrada {caminho_entrada}: {e}")
        raise

    col_minimos = []
    col_pontuacao = []
    estado_inicial = None
    estado_final = None

    for idx, row in df.iterrows():
        try:
            if row['step'] == 0:
                estado_inicial = string_para_estado(row['current'])
                estado_final = string_para_estado(row['end'])
                logging.info(f"Arquivo {os.path.basename(caminho_entrada)} - Estado inicial: {estado_inicial}")
                logging.info(f"Arquivo {os.path.basename(caminho_entrada)} - Estado final: {estado_final}")

            if row['done'] == 1:
                min_movs = movimentos_minimos(estado_inicial, estado_final, altura_max=row['size'])
                logging.info(f"Arquivo {os.path.basename(caminho_entrada)} - Movimentos mínimos: {min_movs}")
                pontuacao = calcular_pontuacao(row, min_movs)
            else:
                min_movs = 0
                pontuacao = 0

            col_minimos.append(min_movs)
            col_pontuacao.append(pontuacao)
            
        except Exception as e:
            logging.error(f"Erro ao processar linha {idx} do arquivo {caminho_entrada}: {e}")
            col_minimos.append(-1)
            col_pontuacao.append(0)

    df['movimentos_minimos'] = col_minimos
    df['pontuacao_acumulada'] = pd.Series(col_pontuacao).cumsum()

    try:
        df.to_csv(caminho_saida, index=False)
        logging.info(f"Arquivo {os.path.basename(caminho_saida)} processado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo de saída {caminho_saida}: {e}")
        raise

def main():
    """Função principal que processa todos os arquivos CSV."""
    
    # Criar pasta de resultados se não existir
    pasta_resultados = "resultados_processados"
    Path(pasta_resultados).mkdir(exist_ok=True)
    
    # pasta de dados originais
    pasta_dados_originais = "dados_originais"
    Path(pasta_dados_originais).mkdir(exist_ok=True)
    
    # Encontrar todos os arquivos CSV na pasta de dados originais
    arquivos_csv = glob.glob(os.path.join(pasta_dados_originais, "*.csv"))
    
    if not arquivos_csv:
        logging.warning(f"Nenhum arquivo CSV encontrado na pasta '{pasta_dados_originais}'!")
        return
    
    logging.info(f"Encontrados {len(arquivos_csv)} arquivos CSV para processar na pasta '{pasta_dados_originais}'")
    
    # Processar cada arquivo
    for arquivo in arquivos_csv:
        try:
            nome_arquivo = os.path.basename(arquivo)
            # Manter o nome original do arquivo
            caminho_saida = os.path.join(pasta_resultados, nome_arquivo)
            
            logging.info(f"Processando arquivo: {nome_arquivo}")
            processar_arquivo(arquivo, caminho_saida)
            
        except Exception as e:
            logging.error(f"Erro ao processar arquivo {arquivo}: {e}")
            continue
    
    logging.info(f"Processamento concluído! Resultados salvos na pasta '{pasta_resultados}'")

if __name__ == "__main__":
    main() 