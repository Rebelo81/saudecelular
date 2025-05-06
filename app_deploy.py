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

app = App(app_ui, server) 