from pathlib import Path

# Novo app.py com todos os gráficos corrigidos para @render_plotly
app_corrected = '''
from shiny import App, ui, reactive
from shinywidgets import render_plotly
import pandas as pd
import plotly.express as px

@reactive.Calc
def load_data():
    df = pd.read_csv("saudevscelular.csv")
    df.columns = [col.strip().replace(" ", "").replace("_", "").lower() for col in df.columns]

    if "mobilephoneactivities" in df.columns and df["mobilephoneactivities"].dtype == "object":
        df["mobilephoneactivities"] = df["mobilephoneactivities"].str.split(";")
    
    if "usagesymptoms" in df.columns and df["usagesymptoms"].dtype == "object":
        df["usagesymptoms"] = df["usagesymptoms"].str.split(";")
    
    df["gender"] = df["gender"].fillna(df["gender"].mode()[0])
    df["age"] = pd.Categorical(df["age"], categories=["16-20", "21-25", "26-30", "31-35"], ordered=True)

    return df

app_ui = ui.page_fluid(
    ui.h2("📱 Impacto do Uso de Celulares na Educação e Saúde", class_="text-primary"),
    ui.navset_tab(
        ui.nav_panel("📊 Demografia", 
            ui.output_plot("grafico_genero"),
            ui.output_plot("grafico_idade"),
            ui.output_plot("grafico_uso_diario")
        ),
        ui.nav_panel("🎓 Uso Educacional",
            ui.output_plot("grafico_freq_edu"),
            ui.output_plot("grafico_apps_edu")
        ),
        ui.nav_panel("⚠️ Sintomas e Saúde",
            ui.output_plot("grafico_sintomas"),
            ui.output_plot("grafico_precaucao"),
            ui.output_plot("grafico_saude")
        ),
        ui.nav_panel("📈 Correlações e Insights",
            ui.output_plot("grafico_correlacao")
        )
    ),
    ui.hr(),
    ui.markdown("**Fonte dos dados:** [Kaggle](https://www.kaggle.com/datasets/innocentmfa/students-health-and-academic-performance/data)")
)

def server(input, output, session):

    @output
    @render_plotly
    def grafico_genero():
        df = load_data()
        fig = px.pie(df, names="gender", title="Distribuição por Gênero", hole=0.3)
        return fig

    @output
    @render_plotly
    def grafico_idade():
        df = load_data()
        fig = px.histogram(df, x="age", color="age", title="Distribuição por Faixa Etária")
        return fig

    @output
    @render_plotly
    def grafico_uso_diario():
        df = load_data()
        fig = px.histogram(df, x="dailyusages", color="gender", barmode="group", title="Tempo de Uso Diário por Gênero")
        return fig

    @output
    @render_plotly
    def grafico_freq_edu():
        df = load_data()
        fig = px.histogram(df, x="mobilephoneuseforeducation", color="gender", title="Frequência de Uso para Educação")
        return fig

    @output
    @render_plotly
    def grafico_apps_edu():
        df = load_data()
        fig = px.histogram(df, x="educationalapps", color="gender", title="Tipos de Aplicativos Educacionais")
        return fig

    @output
    @render_plotly
    def grafico_sintomas():
        df = load_data()
        def simplificar(val):
            if isinstance(val, list):
                if "All of these" in val: return "Todos"
                elif len(val) > 1: return "Múltiplos"
                else: return val[0]
            return "Não especificado"
        df["sintomas"] = df["usagesymptoms"].apply(simplificar)
        fig = px.histogram(df, x="sintomas", color="gender", title="Sintomas Relatados pelo Uso do Celular")
        return fig

    @output
    @render_plotly
    def grafico_precaucao():
        df = load_data()
        fig = px.histogram(df, x="healthprecautions", color="gender", title="Precauções de Saúde Adotadas")
        return fig

    @output
    @render_plotly
    def grafico_saude():
        df = load_data()
        def simplificar(val):
            if isinstance(val, list): return val[0]
            elif isinstance(val, str) and ";" in val: return val.split(";")[0]
            return val
        df["avaliacao"] = df["healthrating"].apply(simplificar)
        fig = px.histogram(df, x="avaliacao", color="gender", title="Autoavaliação da Saúde")
        return fig

    @output
    @render_plotly
    def grafico_correlacao():
        df = load_data()
        maps = {
            'mobilephoneuseforeducation': {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1},
            'dailyusages': {'<2hours': 1, '2-4hours': 2, '4-6hours': 3, '>6hours': 4},
            'performanceimpact': {'Stronglyagree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Stronglydisagree': 1},
            'symptomfrequency': {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1},
            'healthrating': {'Excellent': 4, 'Good': 3, 'Fair': 2, 'Poor': 1}
        }
        for col, mapping in maps.items():
            if col in df.columns:
                df[col + '_num'] = df[col].map(mapping)

        numeric_cols = [col for col in df.columns if col.endswith('_num')]
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=True, title="Matriz de Correlação entre Variáveis")
        return fig

app = App(app_ui, server)
'''

requirements_full = '''
shiny
shinywidgets
pandas
plotly
'''

readme_content = '''
# Impacto do Uso de Celulares na Educação e Saúde

Este projeto é um painel interativo criado com **Shiny para Python**, utilizando dados reais de estudantes sobre uso de celulares, desempenho acadêmico e saúde mental/física.

## 🔧 Tecnologias utilizadas

- Python
- shiny & shinywidgets
- pandas
- plotly

## 📊 Funcionalidades

- Gráficos interativos com filtro por idade e gênero
- Correlações visuais entre variáveis
- Análise de sintomas, apps educacionais e precauções
- Publicação via Posit Connect ou execução local

## ▶️ Como rodar localmente

```bash
pip install -r requirements.txt
shiny run --reload app.py




