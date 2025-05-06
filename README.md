# 📱 Saúde Celular - Impacto do Uso de Celulares na Educação e Saúde

![Dashboard de análise de uso de celulares](plots/correlacao_uso_celular.png)

Este projeto é um painel interativo desenvolvido com **Shiny para Python**, que analisa o impacto do uso de dispositivos móveis na saúde e educação de estudantes. A aplicação apresenta visualizações detalhadas sobre hábitos de uso, sintomas relatados e correlações entre uso de dispositivos e bem-estar.

## 🎥 Demonstração

Aqui está uma demonstração do aplicativo em funcionamento:

[![Demonstração em vídeo](plots/correlacao_uso_celular.png)](https://github.com/Rebelo81/saudecelular)

*Clique para ver o aplicativo completo*

## 📊 Principais Funcionalidades

- Análise demográfica dos usuários por gênero e faixa etária
- Padrões de uso de dispositivos móveis para educação
- Sintomas relatados associados ao uso prolongado
- Correlações entre tempo de uso, impacto no desempenho e saúde
- Visualizações interativas com filtros dinâmicos

## 🔧 Tecnologias Utilizadas

- **Python** - Linguagem principal
- **Shiny & ShinyWidgets** - Framework de dashboard interativo
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **Jupyter Notebook** - Análise exploratória inicial

## 📈 Versões do Dashboard

O projeto possui duas versões do dashboard:

### 1. Dashboard Original (app.py)
- Focado na visualização de dados específicos
- Dividido em abas temáticas (demografia, educação, saúde)
- Ideal para análise detalhada de dados

### 2. Dashboard Executivo (dashboard_executivo.py)
- **NOVO!** Visão executiva e estratégica do projeto completo
- Inclui contexto, objetivos e metodologia da pesquisa
- Apresenta métricas-chave e resumo executivo
- Oferece insights e recomendações baseadas nos dados
- Design moderno e interface mais amigável
- Inclui painel de conclusões e recomendações

## 🚀 Como Executar

### Requisitos

- Python 3.7+
- Dependências listadas em `requirements.txt`

### Instruções

1. Clone este repositório
```bash
git clone https://github.com/Rebelo81/SaudeCelular.git
cd SaudeCelular
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Execute a aplicação Shiny

Para o dashboard original:
```bash
shiny run --reload app.py
```

Para o dashboard executivo interativo:
```bash
shiny run --reload dashboard_executivo.py
```

4. Acesse a aplicação no navegador (geralmente em http://localhost:8000)

## 📁 Estrutura do Projeto

- `app.py` - Aplicação Shiny principal
- `saudevscelular.py` - Script de processamento de dados
- `saudevscelular.csv` - Dados principais
- `dados_uso_celular_limpos.csv` - Dados processados
- `SaudeVsMiniTelas.ipynb` - Notebook com análise exploratória
- `plots/` - Diretório com gráficos gerados

## 📊 Fonte dos Dados

Os dados utilizados neste projeto foram obtidos do [Kaggle](https://www.kaggle.com/datasets/innocentmfa/students-health-and-academic-performance/data).

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

## 🔗 Compartilhando no LinkedIn

Este projeto demonstra habilidades em:

- **Análise de Dados** com Python e Pandas
- **Visualização interativa** com Plotly e Shiny
- **Dashboard web** com interface responsiva
- **Controle de versão** com Git e GitHub

Ao compartilhar no LinkedIn, destaque estas habilidades técnicas e o impacto do seu projeto:

> Desenvolvi um dashboard interativo para análise do impacto do uso de celulares na saúde e educação, utilizando Python, Shiny e Plotly. O projeto demonstra visualizações interativas e análises estatísticas que revelam correlações importantes entre tempo de uso e indicadores de saúde.
>
> Tecnologias: Python, Pandas, Plotly, Shiny
>
> #DataScience #Python #Dashboard #Visualização

---

Desenvolvido como parte de um estudo sobre o impacto da tecnologia na saúde e educação.
