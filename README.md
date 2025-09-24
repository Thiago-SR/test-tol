# Sistema de Análise de Dados de Testes PEBL - Torre de Londres

## Visão Geral

Este projeto implementa um sistema completo de processamento e análise de dados de testes cognitivos baseados no paradigma da Torre de Londres (Tower of London - ToL). O sistema processa dados brutos de testes PEBL (Psychology Experiment Building Language) e gera análises estatísticas detalhadas para avaliação de funções executivas.

## Estrutura Organizada

O projeto foi reorganizado para melhor manutenibilidade e execução:

```
test-tol/
├── dados_originais/          # Dados brutos dos testes
├── 01_dados_processados/     # Dados processados com pontuações
├── 02_dados_combinados/      # Dados combinados por usuário
├── 03_analises_combinadas/   # Análises dos dados combinados
├── scripts/                  # Todos os scripts de processamento
│   ├── process_all_files.py      # Processamento de dados originais
│   ├── combine_user_data.py      # Combinação de dados por usuário
│   ├── analyze_combined_data.py  # Análise de dados combinados
│   └── anova.py                  # Análise estatística ANOVA
├── run_pipeline.py          # Script principal para executar todo o pipeline
└── README.md
```

Nota: as pastas de entrada e saída (dados_originais, 01_dados_processados, 02_dados_combinados, 03_analises_combinadas) são geradas durante a execução e não são versionadas (ignoradas no .gitignore).

## Como Usar

### Execução Automática (Recomendado)

Execute o script principal que executa todo o pipeline automaticamente:

```bash
python run_pipeline.py
```

Este script irá executar todos os passos na ordem correta:
1. **Processamento de dados originais** - Calcula pontuações baseadas em movimentos mínimos
2. **Combinação de dados por usuário** - Combina dados dos três testes (T0, T1, T2) para cada usuário
3. **Análise de dados combinados** - Analisa os dados combinados de cada usuário
4. **Análise estatística ANOVA** - Realiza ANOVA de medidas repetidas para identificar diferenças significativas

### Execução Manual (Passo a Passo)

Se preferir executar cada script individualmente:

#### 1. Preparação dos Dados

Coloque os arquivos CSV dos testes na pasta `dados_originais/`. Os arquivos devem seguir o padrão:
- `T0_[ID]_Tol.csv` - Teste inicial
- `T1_[ID]_Tol.csv` - Teste após intervenção
- `T2_[ID]_Tol.csv` - Teste final

#### 2. Processamento de Dados Originais

```bash
python scripts/process_all_files.py
```

#### 3. Combinação de Dados por Usuário

```bash
python scripts/combine_user_data.py
```

#### 4. Análise dos Dados Combinados

```bash
python scripts/analyze_combined_data.py
```

#### 5. Análise Estatística ANOVA

```bash
python scripts/anova.py
```

## Funcionalidades Principais

### 1. Processamento de Dados Brutos (`scripts/process_all_files.py`)
- **Objetivo**: Processa arquivos CSV brutos dos testes PEBL
- **Funcionalidades**:
  - Calcula o número mínimo de movimentos necessários para resolver cada puzzle
  - Implementa algoritmo de busca em largura (BFS) para encontrar solução ótima
  - Calula pontuação baseada na eficiência dos movimentos
  - Adiciona colunas de análise: `movimentos_minimos` e `pontuacao_acumulada`
- **Algoritmo**: Utiliza busca em largura para encontrar o caminho mais curto entre estados iniciais e finais
- **Saída**: Arquivos processados na pasta `01_dados_processados/`

### 2. Combinação de Dados (`scripts/combine_user_data.py`)
- **Objetivo**: Combina dados dos três testes (T0, T1, T2) de cada participante
- **Funcionalidades**:
  - Agrupa arquivos por ID do participante
  - Adiciona prefixos às colunas (T0_, T1_, T2_) para identificação
  - Converte tipos de dados apropriados
  - Adiciona descrições das colunas para facilitar interpretação
- **Saída**: Arquivos combinados na pasta `02_dados_combinados/`

### 3. Análise de Dados Combinados (`scripts/analyze_combined_data.py`)
- **Objetivo**: Analisa dados combinados dos três testes
- **Funcionalidades**:
  - Processa arquivos combinados com prefixos T0_, T1_, T2_
  - Calcula as mesmas métricas para cada teste
  - Permite comparação entre diferentes momentos de teste
- **Saída**: Arquivos de análise na pasta `03_analises_combinadas/`

### 4. Análise Estatística ANOVA (`scripts/anova.py`)
- **Objetivo**: Realiza ANOVA de medidas repetidas para identificar diferenças significativas entre os testes
- **Funcionalidades**:
  - Analisa todas as variáveis com dados de T0, T1, T2
  - Calcula estatísticas F, p-valor e tamanho de efeito (η²)
  - Identifica variáveis com diferenças significativas
  - Gera relatório em Excel com resultados detalhados
- **Dependências**: pandas, pingouin, numpy, openpyxl
- **Saída**: Arquivo Excel `resultados_anova_medidas_repetidas.xlsx`

### 5. Análise de Pressupostos e Post-hoc (`scripts/analise_pressupostos.py`)
- **Objetivo**: Verificar pressupostos e realizar análises adicionais para a variável de eficiência dos movimentos
- **Funcionalidades**:
  - Teste de normalidade (Shapiro-Wilk) por tempo (T0, T1, T2)
  - Detecção de outliers (IQR e Z-score) e boxplots
  - ANOVA de medidas repetidas (p-valor, F, η² parcial)
  - Teste de esfericidade de Mauchly (W, p)
  - Comparações post-hoc pareadas com correção de Bonferroni
  - Relato de diferença de médias, IC 95% e tamanho de efeito (Cohen’s d para dados pareados – d_z)
- **Saídas**:
  - Planilha de resultados detalhados (quando acionado pelo pipeline)
  - Gráficos em `graficos_eficiencia/` ou `graficos_pressupostos/` (não versionados)

## Métricas Calculadas

Para cada teste, são calculadas as seguintes métricas:

1. **Total de movimentos**: Número total de movimentos realizados
2. **Tempo total (ms)**: Tempo total gasto nos testes completados
3. **Trials completos**: Número de trials concluídos com sucesso
4. **Movimentos por trial**: Média de movimentos por trial
5. **Tempo médio por trial**: Tempo médio gasto por trial
6. **Tempo por movimento**: Tempo médio por movimento
7. **Número de tentativas**: Número de trials que precisaram de múltiplas tentativas
8. **Total movimentos mínimos**: Soma dos movimentos mínimos necessários
9. **Eficiência de movimentos**: Razão entre movimentos mínimos e totais

## Dependências

- Python 3.7+
- pandas
- pingouin (para ANOVA)
- numpy
- openpyxl (para arquivos Excel)
- pathlib
- logging

## Estrutura dos Dados

### Arquivos de Entrada
Os arquivos CSV devem conter as seguintes colunas:
- `sub`: ID do teste
- `trial`: Número do trial
- `size`: Tamanho do problema
- `current`: Estado atual dos pinos
- `end`: Estado objetivo dos pinos
- `step`: Número de passos realizados
- `reset`: Indicador de reinício
- `tries`: Número de tentativas
- `score`: Pontuação
- `abstime`: Tempo absoluto
- `trialtime`: Tempo do trial
- `clicktime`: Tempo de clique
- `done`: Indicador de conclusão (1 = sucesso, 0 = falha)

### Arquivos de Saída
Os arquivos processados incluem colunas adicionais:
- `movimentos_minimos`: Número mínimo de movimentos necessários
- `pontuacao_acumulada`: Pontuação acumulada baseada na eficiência

## Logs e Monitoramento

### Logs Automáticos
O script principal (`run_pipeline.py`) gera:
- Log detalhado em arquivo `pipeline_execution.log`
- Saída em tempo real no console
- Resumo final da execução
- Tempo total de processamento

### Logs Individuais
Cada script gera logs detalhados incluindo:
- Informações sobre o processamento de cada arquivo
- Estados inicial e final dos problemas
- Cálculos de movimentos mínimos
- Erros e avisos

## Tratamento de Erros

O sistema inclui tratamento robusto de erros:
- Validação de pré-requisitos antes da execução
- Verificação de existência de arquivos e pastas
- Validação de formatos de arquivo
- Verificação de estados válidos
- Tratamento de dados ausentes
- Logs de erro detalhados
- Interrupção automática em caso de falha

## Exemplo de Uso Completo

```bash
# 1. Colocar arquivos CSV na pasta dados_originais/
# 2. Executar pipeline completo
python run_pipeline.py

# Saída esperada:
# ============================================================
# INICIANDO PIPELINE DE PROCESSAMENTO TOL
# ============================================================
# Verificando pré-requisitos...
# ✓ Encontrados 45 arquivos CSV na pasta 'dados_originais'
# ✓ Todos os scripts necessários estão presentes
# ✓ Pré-requisitos atendidos
# 
# --- ETAPA 1/4 ---
# Executando: Processamento de dados originais e cálculo de pontuações
# ✓ Processamento de dados originais e cálculo de pontuações - Concluído com sucesso
# 
# --- ETAPA 2/4 ---
# Executando: Combinação de dados por usuário
# ✓ Combinação de dados por usuário - Concluído com sucesso
# 
# --- ETAPA 3/4 ---
# Executando: Análise de dados combinados
# ✓ Análise de dados combinados - Concluído com sucesso
# 
# --- ETAPA 4/4 ---
# Executando: Análise de resultados individuais
# ✓ Análise de resultados individuais - Concluído com sucesso
# 
# ============================================================
# RESUMO DA EXECUÇÃO
# ============================================================
# Etapas executadas com sucesso: 4/4
# Tempo total de execução: 45.32 segundos
# ✓ PIPELINE CONCLUÍDO COM SUCESSO!
```

## Arquivos Gerados

Após a execução bem-sucedida, você terá:

- **01_dados_processados/** - Dados processados com pontuações calculadas
- **02_dados_combinados/** - Dados combinados por usuário (T0, T1, T2)
- **03_analises_combinadas/** - Análises dos dados combinados
- **resultados_anova_medidas_repetidas.xlsx** - Análise estatística ANOVA
- **pipeline_execution.log** - Log detalhado da execução

## Algoritmo de Busca de Movimentos Mínimos

O sistema implementa um algoritmo de busca em largura (BFS) para encontrar o número mínimo de movimentos:

1. **Representação de Estados**: Estados são representados como listas de pinos
2. **Geração de Movimentos**: Para cada estado, gera todos os movimentos válidos
3. **Busca em Largura**: Explora todos os estados possíveis nível por nível
4. **Critério de Parada**: Encontra o estado objetivo ou atinge limite de movimentos
5. **Validação**: Verifica restrições de altura máxima dos pinos

## Notas Técnicas

- O algoritmo de movimentos mínimos usa busca em largura (BFS)
- Estados são normalizados para ter exatamente 3 pinos
- Pontuação máxima é 10, reduzida por movimentos extras
- Timeout de 1000 movimentos para evitar loops infinitos
- Suporte a diferentes tamanhos de problemas (altura máxima configurável)
- Timeout de 5 minutos por script para evitar travamentos
- Execução sequencial com interrupção automática em caso de falha

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
