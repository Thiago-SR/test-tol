# Script de ANOVA de Medidas Repetidas

Este script realiza ANOVA de medidas repetidas para dados de testes neuropsicológicos com múltiplas variáveis medidas em 3 momentos diferentes (T0, T1, T2).

## 📋 Funcionalidades

- ✅ Leitura automática de arquivo CSV
- ✅ Identificação automática de variáveis com padrão `Variavel_T0`, `Variavel_T1`, `Variavel_T2`
- ✅ ANOVA de medidas repetidas para cada variável usando `pingouin`
- ✅ Cálculo de p-value e tamanho de efeito (partial eta squared)
- ✅ Exportação dos resultados para Excel
- ✅ Estatísticas descritivas para cada variável
- ✅ Relatório detalhado no console

## 🚀 Como usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o script
```bash
python anova.py
```

### 3. Verificar resultados
- **Console**: Mostra progresso e resultados principais
- **Excel**: Arquivo `resultados_anova_medidas_repetidas.xlsx` com:
  - Planilha `Resultados_ANOVA`: Tabela com todos os resultados
  - Planilhas `Desc_Variavel`: Estatísticas descritivas para cada variável

## 📊 Estrutura dos dados

O script espera um arquivo CSV com:
- Coluna de ID dos participantes (padrão: `id`)
- Variáveis organizadas em 3 colunas por variável:
  - `Variavel_T0`: Momento inicial
  - `Variavel_T1`: Momento intermediário  
  - `Variavel_T2`: Momento final

### Exemplo de estrutura:
```
id,Total_Movimentos_T0,Total_Movimentos_T1,Total_Movimentos_T2,Tempo_Total_ms_T0,Tempo_Total_ms_T1,Tempo_Total_ms_T2
4567,160,158,125,523871,376502,301094
4568,155,152,147,346264,280899,224875
...
```

## 📈 Resultados

### Variáveis analisadas:
- **Total_Movimentos**: Total de movimentos realizados
- **Tempo_Total_ms**: Tempo total em milissegundos
- **Movimentos_por_Trial**: Movimentos por tentativa
- **Tempo_Médio_por_Trial**: Tempo médio por tentativa
- **Tempo_por_Movimento**: Tempo por movimento
- **Trials_Completos**: Tentativas completadas
- **Movimentos_totais**: Movimentos totais
- **Movimentos_minimos**: Movimentos mínimos
- **Movimentos_eficiencia**: Eficiência dos movimentos

### Interpretação dos resultados:
- **p < 0.05**: Diferença significativa entre os momentos
- **η² ≥ 0.14**: Grande tamanho de efeito
- **η² ≥ 0.06**: Médio tamanho de efeito
- **η² < 0.06**: Pequeno tamanho de efeito

## 🔧 Personalização

Para usar com outros dados:
1. Modifique o caminho do arquivo CSV na função `main()`
2. Ajuste o nome da coluna de ID se necessário
3. O script detecta automaticamente variáveis com sufixos `_T0`, `_T1`, `_T2`

## 📝 Dependências

- `pandas`: Manipulação de dados
- `pingouin`: Análises estatísticas
- `numpy`: Operações numéricas
- `openpyxl`: Exportação para Excel

## 📄 Licença

Este script foi desenvolvido para análise de dados neuropsicológicos.