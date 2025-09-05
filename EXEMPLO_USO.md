# Exemplo de Uso do Sistema TOL

Este arquivo demonstra como usar o sistema de processamento de dados TOL.

## Execução Rápida

Para executar todo o pipeline automaticamente:

```bash
python run_pipeline.py
```

## Execução Manual (Passo a Passo)

Se preferir executar cada etapa individualmente:

### 1. Processamento de Dados Originais
```bash
python scripts/process_all_files.py
```
- Processa arquivos CSV da pasta `dados_originais/`
- Calcula movimentos mínimos e pontuações
- Salva resultados em `01_dados_processados/`

### 2. Combinação de Dados por Usuário
```bash
python scripts/combine_user_data.py
```
- Combina dados dos três testes (T0, T1, T2) por usuário
- Adiciona prefixos às colunas
- Salva arquivos combinados em `02_dados_combinados/`

### 3. Análise de Dados Combinados
```bash
python scripts/analyze_combined_data.py
```
- Analisa dados combinados de cada usuário
- Calcula métricas para cada teste
- Salva análises em `03_analises_combinadas/`

#### 4. Análise Estatística ANOVA

```bash
python scripts/anova.py
```

## Estrutura de Arquivos Esperada

### Dados Originais (`dados_originais/`)
```
T0_4567_Tol.csv    # Teste inicial do usuário 4567
T1_4567_Tol.csv    # Teste após intervenção do usuário 4567
T2_4567_Tol.csv    # Teste final do usuário 4567
T0_4568_Tol.csv    # Teste inicial do usuário 4568
T1_4568_Tol.csv    # Teste após intervenção do usuário 4568
T2_4568_Tol.csv    # Teste final do usuário 4568
...                # E assim por diante
```

### Arquivos Gerados

Após a execução, você terá:

1. **01_dados_processados/** - Dados processados com pontuações
2. **02_dados_combinados/** - Dados combinados por usuário
3. **03_analises_combinadas/** - Análises dos dados combinados
4. **resultados_anova_medidas_repetidas.xlsx** - Análise estatística ANOVA
5. **pipeline_execution.log** - Log detalhado da execução

## Exemplo de Saída do Pipeline

```
============================================================
INICIANDO PIPELINE DE PROCESSAMENTO TOL
============================================================
Verificando pré-requisitos...
[OK] Encontrados 45 arquivos CSV na pasta 'dados_originais'
[OK] Todos os scripts necessários estão presentes
[OK] Pré-requisitos atendidos

--- ETAPA 1/4 ---
Executando: Processamento de dados originais e cálculo de pontuações
Script: process_all_files.py
[OK] Processamento de dados originais e cálculo de pontuações - Concluído com sucesso

--- ETAPA 2/4 ---
Executando: Combinação de dados por usuário
Script: combine_user_data.py
[OK] Combinação de dados por usuário - Concluído com sucesso

--- ETAPA 3/4 ---
Executando: Análise de dados combinados
Script: analyze_combined_data.py
[OK] Análise de dados combinados - Concluído com sucesso

--- ETAPA 4/4 ---
Executando: Análise estatística ANOVA de medidas repetidas
Script: anova.py
[OK] Análise estatística ANOVA de medidas repetidas - Concluído com sucesso

============================================================
RESUMO DA EXECUÇÃO
============================================================
Etapas executadas com sucesso: 4/4
Tempo total de execução: 8.96 segundos
[OK] PIPELINE CONCLUÍDO COM SUCESSO!

Arquivos gerados:
  - 01_dados_processados/ - Dados processados com pontuações
  - 02_dados_combinados/ - Dados combinados por usuário
  - 03_analises_combinadas/ - Análises dos dados combinados
  - resultados_anova_medidas_repetidas.xlsx - Análise estatística ANOVA
```

## Troubleshooting

### Problema: "Pasta 'dados_originais' não encontrada!"
**Solução**: Certifique-se de que a pasta `dados_originais/` existe e contém arquivos CSV.

### Problema: "Nenhum arquivo CSV encontrado na pasta 'dados_originais'!"
**Solução**: Verifique se os arquivos CSV estão na pasta correta e têm a extensão `.csv`.

### Problema: "Script obrigatório não encontrado"
**Solução**: Certifique-se de que todos os scripts estão na pasta `scripts/`.

### Problema: Erro de encoding no Windows
**Solução**: O sistema foi atualizado para evitar problemas de encoding. Se ainda ocorrer, execute em um terminal com suporte UTF-8.

## Logs e Monitoramento

- **Log em arquivo**: `pipeline_execution.log` - Log detalhado de toda a execução
- **Log no console**: Saída em tempo real durante a execução
- **Logs individuais**: Cada script gera logs detalhados sobre seu processamento

## Dependências

- Python 3.7+
- pandas
- pathlib
- logging

Instale as dependências com:
```bash
pip install pandas
```
