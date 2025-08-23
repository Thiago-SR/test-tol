# Sistema de Análise de Dados de Testes PEBL - Torre de Londres

## Visão Geral

Este projeto implementa um sistema completo de processamento e análise de dados de testes cognitivos baseados no paradigma da Torre de Londres (Tower of London - ToL). O sistema processa dados brutos de testes PEBL (Psychology Experiment Building Language) e gera análises estatísticas detalhadas para avaliação de funções executivas.

## Funcionalidades Principais

### 1. Processamento de Dados Brutos (`process_all_files.py`)
- **Objetivo**: Processa arquivos CSV brutos dos testes PEBL
- **Funcionalidades**:
  - Calcula o número mínimo de movimentos necessários para resolver cada puzzle
  - Implementa algoritmo de busca em largura (BFS) para encontrar solução ótima
  - Calcula pontuação baseada na eficiência dos movimentos
  - Adiciona colunas de análise: `movimentos_minimos` e `pontuacao_acumulada`
- **Algoritmo**: Utiliza busca em largura para encontrar o caminho mais curto entre estados iniciais e finais
- **Saída**: Arquivos processados na pasta `resultados_processados/`

### 2. Combinação de Dados (`combine_user_data.py`)
- **Objetivo**: Combina dados dos três testes (T0, T1, T2) de cada participante
- **Funcionalidades**:
  - Agrupa arquivos por ID do participante
  - Adiciona prefixos às colunas (T0_, T1_, T2_) para identificação
  - Converte tipos de dados apropriados
  - Adiciona descrições das colunas para facilitar interpretação
- **Saída**: Arquivos combinados na pasta `dados_combinados/`

### 3. Análise de Resultados Individuais (`analyze_outcomes.py`)
- **Objetivo**: Analisa dados individuais de cada teste
- **Métricas Calculadas**:
  - Total de movimentos realizados
  - Tempo total de execução
  - Número de trials completados
  - Movimentos por trial
  - Tempo médio por trial
  - Tempo por movimento
  - Número de tentativas
  - Total de movimentos mínimos
  - Eficiência dos movimentos
- **Saída**: Arquivos de análise na pasta `analises_resultados/`

### 4. Análise de Dados Combinados (`analyze_combined_data.py`)
- **Objetivo**: Analisa dados combinados dos três testes
- **Funcionalidades**:
  - Processa arquivos combinados com prefixos T0_, T1_, T2_
  - Calcula as mesmas métricas para cada teste
  - Permite comparação entre diferentes momentos de teste
- **Saída**: Arquivos de análise na pasta `analises_combinadas/`

## Estrutura de Dados

### Dados Originais (`dados_originais/`)
Arquivos CSV com formato PEBL contendo:
- `sub`: Identificador do participante
- `trial`: Número do trial
- `size`: Tamanho do puzzle (3, 4, 5 pinos)
- `current`: Estado atual dos pinos (formato `|A|B|C|`)
- `end`: Estado objetivo dos pinos
- `step`: Número do passo atual
- `reset`: Indicador de reinício
- `tries`: Número de tentativas
- `score`: Pontuação
- `abstime`: Tempo absoluto em milissegundos
- `trialtime`: Tempo do trial em milissegundos
- `clicktime`: Tempo do clique em milissegundos
- `done`: Indicador de conclusão (1 = completo, 0 = incompleto)

### Dados Processados (`resultados_processados/`)
Arquivos originais enriquecidos com:
- `movimentos_minimos`: Número mínimo de movimentos calculado
- `pontuacao_acumulada`: Pontuação acumulada baseada na eficiência

### Dados Combinados (`dados_combinados/`)
Arquivos com dados dos três testes combinados, com colunas prefixadas:
- `T0_*`: Dados do primeiro teste
- `T1_*`: Dados do segundo teste  
- `T2_*`: Dados do terceiro teste

### Análises (`analises_resultados/` e `analises_combinadas/`)
Arquivos CSV com métricas calculadas para cada participante e teste.

## Métricas Calculadas

### 1. Eficiência de Movimentos
- **Movimentos por Trial**: Total de movimentos ÷ Trials completos
- **Eficiência**: Movimentos mínimos ÷ Movimentos realizados
- **Tentativas**: Número de trials com múltiplas tentativas

### 2. Métricas Temporais
- **Tempo Total**: Soma dos tempos de trials completos
- **Tempo Médio por Trial**: Tempo total ÷ Trials completos
- **Tempo por Movimento**: Tempo total ÷ Total de movimentos

### 3. Indicadores de Performance
- **Trials Completos**: Número de puzzles resolvidos com sucesso
- **Pontuação Acumulada**: Baseada na diferença entre movimentos realizados e mínimos

## Como Executar

### Pré-requisitos
```bash
pip install pandas numpy
```

### Ordem de Execução
1. **Processar dados brutos**:
   ```bash
   python process_all_files.py
   ```

2. **Combinar dados por participante**:
   ```bash
   python combine_user_data.py
   ```

3. **Analisar resultados individuais**:
   ```bash
   python analyze_outcomes.py
   ```

4. **Analisar dados combinados**:
   ```bash
   python analyze_combined_data.py
   ```

### Execução Completa
```bash
python process_all_files.py && python combine_user_data.py && python analyze_outcomes.py && python analyze_combined_data.py
```

## Estrutura de Pastas

```
test-tol/
├── dados_originais/          # Arquivos CSV brutos do PEBL
├── resultados_processados/    # Dados enriquecidos com métricas
├── dados_combinados/         # Dados dos três testes combinados
├── analises_resultados/      # Análises individuais por teste
├── analises_combinadas/      # Análises dos dados combinados
├── Documentação/             # Documentação do projeto
├── process_all_files.py      # Script de processamento principal
├── combine_user_data.py      # Script de combinação de dados
├── analyze_outcomes.py       # Script de análise individual
├── analyze_combined_data.py  # Script de análise combinada
└── README.md                 # Este arquivo
```

## Algoritmo de Busca de Movimentos Mínimos

O sistema implementa um algoritmo de busca em largura (BFS) para encontrar o número mínimo de movimentos:

1. **Representação de Estados**: Estados são representados como listas de pinos
2. **Geração de Movimentos**: Para cada estado, gera todos os movimentos válidos
3. **Busca em Largura**: Explora todos os estados possíveis nível por nível
4. **Critério de Parada**: Encontra o estado objetivo ou atinge limite de movimentos
5. **Validação**: Verifica restrições de altura máxima dos pinos

## Aplicações

Este sistema é útil para:
- **Pesquisa em Neuropsicologia**: Avaliação de funções executivas
- **Estudos de Desenvolvimento**: Comparação entre diferentes faixas etárias
- **Avaliação Clínica**: Monitoramento de pacientes com déficits executivos
- **Estudos de Intervenção**: Avaliação de eficácia de tratamentos
- **Pesquisa Básica**: Estudos sobre tomada de decisão e planejamento

## Formato de Saída

### Arquivos de Análise
Cada arquivo de análise contém uma linha por teste (T0, T1, T2) com as seguintes colunas:
- `teste`: Tipo do teste (T0, T1, T2)
- `total_movimentos`: Total de movimentos realizados
- `tempo_total_ms`: Tempo total em milissegundos
- `trials_completos`: Número de trials completados
- `movimentos_por_trial`: Média de movimentos por trial
- `tempo_medio_por_trial`: Tempo médio por trial
- `tempo_por_movimento`: Tempo médio por movimento
- `num_tentativas`: Número de tentativas múltiplas
- `total_movimentos_minimos`: Soma dos movimentos mínimos
- `eficiencia_movimentos`: Razão movimentos mínimos/realizados

## Contribuições

Este projeto foi desenvolvido para processar dados de testes cognitivos PEBL, especificamente para o paradigma da Torre de Londres, fornecendo ferramentas robustas para análise de dados neuropsicológicos.

## Licença

Este projeto é destinado para uso acadêmico e de pesquisa.