from shiny import App, ui, reactive
from shinywidgets import render_plotly, output_widget, register_widget
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Carregamento de dados
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

# Interface do usuário
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap"),
        ui.tags.style("""
            body { font-family: 'Roboto', sans-serif; }
            .card { margin-bottom: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .card-header { background-color: #6e8efb; color: white; font-weight: 500; border-radius: 10px 10px 0 0; }
            .section-title { color: #4A4A4A; border-bottom: 2px solid #6e8efb; padding-bottom: 8px; margin-bottom: 20px; }
            .chart-container { border-radius: 8px; overflow: hidden; border: 1px solid #eaeaea; }
            .metric-card { padding: 15px; text-align: center; background: linear-gradient(135deg, #f5f7ff 0%, #e9efff 100%); 
                           border-radius: 8px; margin-bottom: 20px; }
            .metric-value { font-size: 24px; font-weight: bold; color: #6e8efb; }
            .metric-label { font-size: 14px; color: #4A4A4A; }
            .text-primary { color: #6e8efb !important; }
            .text-secondary { color: #a777e3 !important; }
            .highlight-box { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #6e8efb; margin: 15px 0; }
            .nav-tabs .nav-link.active { color: #6e8efb; border-bottom: 3px solid #6e8efb; }
        """)
    ),

    ui.div(
        ui.tags.img(src="https://raw.githubusercontent.com/Rebelo81/saudecelular/master/plots/correlacao_uso_celular.png", 
                    height="80px", style="float: left; margin-right: 20px;"),
        ui.h1("📱 Saúde Celular", class_="text-primary"),
        ui.p("Dashboard executivo sobre o impacto do uso de celulares na saúde e educação", 
             class_="lead text-secondary"),
        style="padding: 20px 0; margin-bottom: 20px; border-bottom: 1px solid #eaeaea;"
    ),
    
    # Painel informativo sobre o projeto
    ui.card(
        ui.card_header("Sobre o Projeto"),
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.h4("Contexto"),
                ui.p("Este projeto analisa dados de estudantes sobre o uso de dispositivos móveis e seu impacto na saúde e na educação. A pesquisa foi conduzida com estudantes de diferentes faixas etárias e gêneros para entender como o uso de celulares afeta diversos aspectos de suas vidas."),
                ui.h4("Objetivos"),
                ui.tags.ul(
                    ui.tags.li("Analisar padrões de uso de celulares entre estudantes"),
                    ui.tags.li("Identificar correlações entre tempo de uso e impactos na saúde"),
                    ui.tags.li("Avaliar o uso de celulares para fins educacionais"),
                    ui.tags.li("Fornecer insights para políticas de uso consciente"),
                ),
                width=4
            ),
            ui.panel_main(
                ui.h4("Principais Perguntas de Pesquisa"),
                ui.div(
                    ui.tags.ol(
                        ui.tags.li("Qual é a relação entre o tempo de uso diário de celulares e a percepção de saúde dos estudantes?"),
                        ui.tags.li("Como o uso de celulares para fins educacionais impacta o desempenho acadêmico?"),
                        ui.tags.li("Quais são os principais sintomas relatados associados ao uso prolongado de dispositivos móveis?"),
                        ui.tags.li("Existe diferença nos padrões de uso entre gêneros e faixas etárias?"),
                    )
                ),
                ui.h4("Metodologia"),
                ui.p("Os dados foram coletados por meio de pesquisa com estudantes e incluem informações sobre tempo de uso diário, sintomas relatados, aplicativos educacionais utilizados, e autoavaliação de saúde. A análise foi realizada utilizando Python com bibliotecas de análise de dados e visualização interativa.")
            )
        )
    ),
    
    # Resumo Executivo - Principais métricas
    ui.h2("Resumo Executivo", class_="section-title"),
    ui.row(
        ui.column(3,
            ui.div(
                ui.div(ui.output_text("metrica_tempo_medio"), class_="metric-value"),
                ui.div("Tempo médio de uso diário", class_="metric-label"),
                class_="metric-card"
            )
        ),
        ui.column(3,
            ui.div(
                ui.div(ui.output_text("metrica_uso_educacional"), class_="metric-value"),
                ui.div("Uso para fins educacionais", class_="metric-label"),
                class_="metric-card"
            )
        ),
        ui.column(3,
            ui.div(
                ui.div(ui.output_text("metrica_sintomas"), class_="metric-value"),
                ui.div("Relatam sintomas", class_="metric-label"),
                class_="metric-card"
            )
        ),
        ui.column(3,
            ui.div(
                ui.div(ui.output_text("metrica_impacto_saude"), class_="metric-value"),
                ui.div("Consideram impacto na saúde", class_="metric-label"),
                class_="metric-card"
            )
        )
    ),
    
    # Painel com abas para análises detalhadas
    ui.navset_tab(
        ui.nav_panel("📊 Análise Demográfica", 
            ui.row(
                ui.column(6, 
                    ui.card(
                        ui.card_header("Distribuição por Gênero e Faixa Etária"),
                        ui.output_plot("grafico_demografia"),
                    ),
                ),
                ui.column(6, 
                    ui.card(
                        ui.card_header("Tempo de Uso Diário por Perfil"),
                        ui.output_plot("grafico_uso_diario")
                    ),
                )
            ),
            ui.card(
                ui.card_header("Insights - Análise Demográfica"),
                ui.div(
                    ui.h5("Principais Observações:"),
                    ui.tags.ul(
                        ui.tags.li("A distribuição etária mostra maior concentração nas faixas 21-25 anos, indicando uma população de estudantes universitários."),
                        ui.tags.li("Existe uma diferença significativa nos padrões de uso diário entre gêneros, com grupos específicos apresentando uso mais intenso."),
                        ui.tags.li("Os usuários na faixa de 16-20 anos mostram maior tempo médio de uso diário."),
                    ),
                    class_="highlight-box"
                )
            )
        ),
        
        ui.nav_panel("🎓 Uso Educacional",
            ui.row(
                ui.column(6, 
                    ui.card(
                        ui.card_header("Frequência de Uso para Educação"),
                        ui.output_plot("grafico_freq_edu")
                    ),
                ),
                ui.column(6, 
                    ui.card(
                        ui.card_header("Tipos de Aplicativos Educacionais"),
                        ui.output_plot("grafico_apps_edu")
                    ),
                )
            ),
            ui.card(
                ui.card_header("Correlação: Uso Educacional x Desempenho"),
                ui.output_plot("grafico_correlacao_edu")
            ),
            ui.card(
                ui.card_header("Insights - Uso Educacional"),
                ui.div(
                    ui.h5("Principais Observações:"),
                    ui.tags.ul(
                        ui.tags.li("Estudantes que usam celulares para fins educacionais com frequência moderada tendem a relatar melhor desempenho acadêmico."),
                        ui.tags.li("Os aplicativos educacionais mais populares estão relacionados a cursos online e ferramentas de pesquisa."),
                        ui.tags.li("Existe uma correlação positiva entre o uso de aplicativos educacionais e a satisfação com o aprendizado."),
                    ),
                    class_="highlight-box"
                )
            )
        ),
        
        ui.nav_panel("⚠️ Saúde e Sintomas",
            ui.row(
                ui.column(6, 
                    ui.card(
                        ui.card_header("Sintomas Relatados pelo Uso"),
                        ui.output_plot("grafico_sintomas")
                    ),
                ),
                ui.column(6, 
                    ui.card(
                        ui.card_header("Autoavaliação da Saúde"),
                        ui.output_plot("grafico_saude")
                    ),
                )
            ),
            ui.card(
                ui.card_header("Precauções de Saúde Adotadas"),
                ui.output_plot("grafico_precaucao")
            ),
            ui.card(
                ui.card_header("Insights - Saúde e Sintomas"),
                ui.div(
                    ui.h5("Principais Observações:"),
                    ui.tags.ul(
                        ui.tags.li("Dores de cabeça e problemas visuais são os sintomas mais relatados entre usuários com uso diário superior a 4 horas."),
                        ui.tags.li("Existe uma correlação negativa entre o tempo de uso diário e a autoavaliação de saúde."),
                        ui.tags.li("Usuários que adotam precauções como pausas regulares e filtros de luz azul relatam menos sintomas físicos."),
                    ),
                    class_="highlight-box"
                )
            )
        ),
        
        ui.nav_panel("📈 Análise de Correlações",
            ui.card(
                ui.card_header("Matriz de Correlação entre Variáveis"),
                ui.output_plot("grafico_correlacao")
            ),
            ui.row(
                ui.column(6, 
                    ui.card(
                        ui.card_header("Tempo de Uso vs. Saúde"),
                        ui.output_plot("grafico_uso_vs_saude")
                    ),
                ),
                ui.column(6, 
                    ui.card(
                        ui.card_header("Sintomas vs. Precauções"),
                        ui.output_plot("grafico_sintomas_vs_precaucoes")
                    ),
                )
            ),
            ui.card(
                ui.card_header("Insights - Correlações"),
                ui.div(
                    ui.h5("Principais Observações:"),
                    ui.tags.ul(
                        ui.tags.li("A correlação mais forte observada é entre o tempo de uso diário e a frequência de sintomas reportados."),
                        ui.tags.li("Existe uma relação positiva entre o uso educacional e impacto no desempenho, quando o uso é moderado."),
                        ui.tags.li("Precauções de saúde mostram efeito mitigador na frequência e intensidade dos sintomas reportados."),
                    ),
                    class_="highlight-box"
                )
            )
        ),
        
        ui.nav_panel("🔍 Conclusões",
            ui.card(
                ui.card_header("Principais Achados"),
                ui.div(
                    ui.h4("Impacto na Saúde"),
                    ui.p("O uso prolongado de celulares (acima de 4 horas diárias) está significativamente associado a maior incidência de sintomas como dores de cabeça, problemas visuais e problemas de sono. No entanto, a adoção de precauções adequadas pode mitigar estes efeitos."),
                    
                    ui.h4("Impacto na Educação"),
                    ui.p("O uso de celulares para fins educacionais mostra correlação positiva com o desempenho acadêmico quando utilizado de forma moderada e com propósito específico. Aplicativos educacionais estruturados apresentam maior benefício."),
                    
                    ui.h4("Diferenças Demográficas"),
                    ui.p("Existem padrões distintos de uso entre diferentes faixas etárias e gêneros, o que sugere a necessidade de abordagens personalizadas para promover o uso saudável."),
                    
                    ui.h4("Equilíbrio é Chave"),
                    ui.p("Os dados apontam para a importância do equilíbrio: nem a proibição total nem o uso irrestrito são ideais. Estabelecer limites saudáveis e promover o uso consciente parecem ser as melhores abordagens."),
                    class_="p-3"
                )
            ),
            ui.card(
                ui.card_header("Recomendações"),
                ui.div(
                    ui.h5("Para Instituições Educacionais:"),
                    ui.tags.ul(
                        ui.tags.li("Implementar políticas de uso consciente, em vez de proibições totais"),
                        ui.tags.li("Promover intervalos regulares durante atividades que envolvam dispositivos eletrônicos"),
                        ui.tags.li("Incentivar o uso de aplicativos educacionais estruturados"),
                    ),
                    
                    ui.h5("Para Estudantes:"),
                    ui.tags.ul(
                        ui.tags.li("Adotar precauções como filtros de luz azul e ajuste de postura"),
                        ui.tags.li("Estabelecer limites de tempo de uso diário"),
                        ui.tags.li("Priorizar aplicativos que contribuam efetivamente para o aprendizado"),
                    ),
                    
                    ui.h5("Para Pesquisas Futuras:"),
                    ui.tags.ul(
                        ui.tags.li("Estudos longitudinais para avaliar efeitos a longo prazo"),
                        ui.tags.li("Investigação de estratégias de mitigação mais eficazes"),
                        ui.tags.li("Desenvolvimento de diretrizes baseadas em evidências para uso saudável"),
                    ),
                    class_="p-3"
                )
            )
        )
    ),
    
    # Rodapé
    ui.div(
        ui.hr(),
        ui.row(
            ui.column(6,
                ui.p("Dados obtidos do ", ui.a("Kaggle", href="https://www.kaggle.com/datasets/innocentmfa/students-health-and-academic-performance/data", target="_blank")),
                ui.p("Desenvolvido como parte de um estudo sobre o impacto da tecnologia na saúde e educação"),
            ),
            ui.column(6, {"class": "text-end"},
                ui.p(ui.a("Código fonte no GitHub", href="https://github.com/Rebelo81/saudecelular", target="_blank")),
                ui.p("© 2024 - ", ui.a("Rebelo81", href="https://github.com/Rebelo81", target="_blank"))
            )
        ),
        class_="mt-5 mb-3 text-muted"
    )
)

# Servidor para processamento e visualizações
def server(input, output, session):
    # Métricas para o resumo executivo
    @output
    @render_text
    def metrica_tempo_medio():
        df = load_data()
        # Aqui seria ideal ter uma coluna numérica, mas vamos fazer uma aproximação
        mapping = {'<2hours': 1, '2-4hours': 3, '4-6hours': 5, '>6hours': 7}
        if 'dailyusages' in df.columns:
            counts = df['dailyusages'].value_counts()
            total = counts.sum()
            weighted_avg = sum(mapping.get(k, 0) * v for k, v in counts.items()) / total
            return f"{weighted_avg:.1f} horas"
        return "N/A"
    
    @output
    @render_text
    def metrica_uso_educacional():
        df = load_data()
        if 'mobilephoneuseforeducation' in df.columns:
            frequently = df['mobilephoneuseforeducation'].str.lower().isin(['frequently', 'sometimes']).mean() * 100
            return f"{frequently:.1f}%"
        return "N/A"
    
    @output
    @render_text
    def metrica_sintomas():
        df = load_data()
        if 'usagesymptoms' in df.columns:
            # Considerando quem relatou pelo menos um sintoma
            has_symptoms = df['usagesymptoms'].apply(lambda x: isinstance(x, list) and len(x) > 0).mean() * 100
            return f"{has_symptoms:.1f}%"
        return "N/A"
    
    @output
    @render_text
    def metrica_impacto_saude():
        df = load_data()
        if 'healthimpact' in df.columns:
            impact = df['healthimpact'].str.lower().isin(['yes', 'sometimes']).mean() * 100
            return f"{impact:.1f}%"
        elif 'healthprecautions' in df.columns:
            # Alternativa se não tiver coluna específica
            takes_precautions = df['healthprecautions'].str.lower().str.contains('yes').mean() * 100
            return f"{takes_precautions:.1f}%"
        return "N/A"
    
    # Gráficos para Demografia
    @output
    @render_plotly
    def grafico_demografia():
        df = load_data()
        fig = make_subplots(rows=1, cols=2, 
                           subplot_titles=("Distribuição por Gênero", "Distribuição por Faixa Etária"),
                           specs=[[{"type": "pie"}, {"type": "bar"}]])
        
        # Gráfico de gênero
        gender_counts = df['gender'].value_counts()
        fig.add_trace(go.Pie(
            labels=gender_counts.index, 
            values=gender_counts.values,
            hole=0.4,
            marker_colors=['#6e8efb', '#a777e3', '#63cdda'],
            textinfo='percent+label'
        ), row=1, col=1)
        
        # Gráfico de idade
        age_counts = df['age'].value_counts().sort_index()
        fig.add_trace(go.Bar(
            x=age_counts.index, 
            y=age_counts.values,
            marker_color='#6e8efb',
            text=age_counts.values,
            textposition='auto'
        ), row=1, col=2)
        
        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, t=60, b=40),
            showlegend=False
        )
        return fig
    
    @output
    @render_plotly
    def grafico_uso_diario():
        df = load_data()
        # Criar pivot table para mostrar contagem de tempo de uso por gênero e idade
        if 'dailyusages' in df.columns and 'gender' in df.columns and 'age' in df.columns:
            pivot = pd.crosstab(
                index=[df['gender'], df['age']], 
                columns=df['dailyusages']
            ).reset_index()
            
            # Reorganizar para formato longo para plotly
            pivot_long = pd.melt(
                pivot, 
                id_vars=['gender', 'age'], 
                value_vars=['<2hours', '2-4hours', '4-6hours', '>6hours'] if all(c in pivot.columns for c in ['<2hours', '2-4hours', '4-6hours', '>6hours']) else pivot.columns[2:],
                var_name='Tempo de Uso', 
                value_name='Contagem'
            )
            
            fig = px.bar(
                pivot_long,
                x='Tempo de Uso',
                y='Contagem',
                color='gender',
                facet_col='age',
                color_discrete_sequence=['#6e8efb', '#a777e3', '#63cdda'],
                labels={'gender': 'Gênero', 'age': 'Faixa Etária'},
                title='Tempo de Uso Diário por Gênero e Faixa Etária'
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=10, r=10, t=60, b=40),
            )
            return fig
        
        # Fallback simples se não tiver dados adequados
        return px.histogram(
            df, 
            x='dailyusages' if 'dailyusages' in df.columns else df.columns[0], 
            color='gender' if 'gender' in df.columns else None,
            title='Tempo de Uso Diário'
        )
    
    # Gráficos para Uso Educacional
    @output
    @render_plotly
    def grafico_freq_edu():
        df = load_data()
        if 'mobilephoneuseforeducation' in df.columns and 'gender' in df.columns:
            fig = px.histogram(
                df, 
                x='mobilephoneuseforeducation', 
                color='gender',
                barmode='group',
                color_discrete_sequence=['#6e8efb', '#a777e3', '#63cdda'],
                category_orders={'mobilephoneuseforeducation': ['Frequently', 'Sometimes', 'Rarely', 'Never']},
                title='Frequência de Uso para Educação por Gênero'
            )
            
            fig.update_layout(
                xaxis_title='Frequência de Uso',
                yaxis_title='Contagem',
                legend_title='Gênero',
                height=400
            )
            return fig
        
        return go.Figure()
    
    @output
    @render_plotly
    def grafico_apps_edu():
        df = load_data()
        if 'educationalapps' in df.columns:
            app_counts = df['educationalapps'].value_counts().sort_values(ascending=True).tail(10)
            
            fig = go.Figure(go.Bar(
                x=app_counts.values,
                y=app_counts.index,
                orientation='h',
                marker_color='#6e8efb',
                text=app_counts.values,
                textposition='auto'
            ))
            
            fig.update_layout(
                title='Top 10 Aplicativos Educacionais Usados',
                xaxis_title='Contagem',
                yaxis_title='Aplicativo',
                height=400
            )
            return fig
        
        return go.Figure()
    
    @output
    @render_plotly
    def grafico_correlacao_edu():
        df = load_data()
        # Aqui podemos tentar criar um gráfico de dispersão ou correlação
        # entre uso educacional e alguma medida de desempenho
        mapping_edu = {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1}
        mapping_perf = {'Stronglyagree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Stronglydisagree': 1}
        
        if 'mobilephoneuseforeducation' in df.columns and 'performanceimpact' in df.columns:
            # Converter categorias para valores numéricos
            df['edu_num'] = df['mobilephoneuseforeducation'].map(mapping_edu)
            df['perf_num'] = df['performanceimpact'].map(mapping_perf)
            
            # Calcular contagem para cada combinação
            heat_data = df.groupby(['mobilephoneuseforeducation', 'performanceimpact']).size().reset_index(name='count')
            heat_data['edu_num'] = heat_data['mobilephoneuseforeducation'].map(mapping_edu)
            heat_data['perf_num'] = heat_data['performanceimpact'].map(mapping_perf)
            
            # Converter para matriz para heatmap
            heatmap_data = pd.pivot_table(
                heat_data, 
                values='count', 
                index='mobilephoneuseforeducation',
                columns='performanceimpact',
                aggfunc='sum',
                fill_value=0
            )
            
            fig = px.imshow(
                heatmap_data,
                labels=dict(x="Impacto no Desempenho", y="Uso Educacional", color="Contagem"),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                color_continuous_scale=['#f5f7ff', '#6e8efb'],
                text_auto=True
            )
            
            fig.update_layout(
                title='Correlação: Uso Educacional vs Impacto no Desempenho',
                height=500
            )
            return fig
        
        return go.Figure()
    
    # Gráficos para Saúde e Sintomas
    @output
    @render_plotly
    def grafico_sintomas():
        df = load_data()
        if 'usagesymptoms' in df.columns:
            # Processar sintomas (que podem estar em listas)
            all_symptoms = []
            for symptom_list in df['usagesymptoms']:
                if isinstance(symptom_list, list):
                    all_symptoms.extend(symptom_list)
                elif isinstance(symptom_list, str):
                    all_symptoms.append(symptom_list)
            
            symptom_counts = pd.Series(all_symptoms).value_counts()
            top_symptoms = symptom_counts.sort_values(ascending=True).tail(10)
            
            fig = go.Figure(go.Bar(
                x=top_symptoms.values,
                y=top_symptoms.index,
                orientation='h',
                marker_color='#a777e3',
                text=top_symptoms.values,
                textposition='auto'
            ))
            
            fig.update_layout(
                title='10 Sintomas Mais Relatados',
                xaxis_title='Contagem',
                yaxis_title='Sintoma',
                height=400
            )
            return fig
        
        return go.Figure()
    
    @output
    @render_plotly
    def grafico_saude():
        df = load_data()
        if 'healthrating' in df.columns:
            # Criando uma função para simplificar ratings que possam estar em listas
            def simplify_rating(val):
                if isinstance(val, list):
                    return val[0]
                elif isinstance(val, str) and ";" in val:
                    return val.split(";")[0]
                return val
            
            df['health_simple'] = df['healthrating'].apply(simplify_rating)
            
            health_counts = df['health_simple'].value_counts().sort_index()
            
            # Determinar ordem das categorias (assumindo que são Excellent, Good, Fair, Poor)
            categories = ['Excellent', 'Good', 'Fair', 'Poor']
            categories = [c for c in categories if c in health_counts.index]
            
            # Reorganizar baseado na ordem determinada
            health_counts = health_counts.reindex(categories)
            
            fig = px.bar(
                x=health_counts.index,
                y=health_counts.values,
                color=health_counts.index,
                color_discrete_map={
                    'Excellent': '#4caf50',
                    'Good': '#8bc34a',
                    'Fair': '#ffc107',
                    'Poor': '#f44336'
                },
                labels={'x': 'Classificação', 'y': 'Contagem'},
                title='Autoavaliação da Saúde'
            )
            
            fig.update_layout(
                showlegend=False,
                height=400
            )
            return fig
        
        return go.Figure()
    
    @output
    @render_plotly
    def grafico_precaucao():
        df = load_data()
        if 'healthprecautions' in df.columns:
            precaution_counts = df['healthprecautions'].value_counts()
            
            fig = px.pie(
                values=precaution_counts.values,
                names=precaution_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Bluyl,
                title='Precauções de Saúde Adotadas'
            )
            
            fig.update_layout(
                height=450
            )
            return fig
        
        return go.Figure()
    
    # Gráficos para Correlações
    @output
    @render_plotly
    def grafico_correlacao():
        df = load_data()
        
        # Mapear categorias para valores numéricos para criar correlações
        maps = {
            'mobilephoneuseforeducation': {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1},
            'dailyusages': {'<2hours': 1, '2-4hours': 2, '4-6hours': 3, '>6hours': 4},
            'performanceimpact': {'Stronglyagree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Stronglydisagree': 1},
            'symptomfrequency': {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1},
            'healthrating': {'Excellent': 4, 'Good': 3, 'Fair': 2, 'Poor': 1}
        }
        
        # Aplicar mapeamento para colunas que existem
        for col, mapping in maps.items():
            if col in df.columns:
                df[col + '_num'] = df[col].map(mapping)
        
        # Selecionar colunas numéricas para correlação
        numeric_cols = [col for col in df.columns if col.endswith('_num')]
        
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            
            # Nomes mais amigáveis para o gráfico
            nice_names = {
                'mobilephoneuseforeducation_num': 'Uso Educacional',
                'dailyusages_num': 'Tempo de Uso Diário',
                'performanceimpact_num': 'Impacto no Desempenho',
                'symptomfrequency_num': 'Frequência de Sintomas',
                'healthrating_num': 'Avaliação de Saúde'
            }
            
            corr.index = [nice_names.get(col, col) for col in corr.index]
            corr.columns = [nice_names.get(col, col) for col in corr.columns]
            
            fig = px.imshow(
                corr,
                color_continuous_scale=['#f5f7ff', '#6e8efb'],
                text_auto=True,
                title='Matriz de Correlação entre Variáveis'
            )
            
            fig.update_layout(
                height=500
            )
            return fig
        
        return go.Figure()
    
    @output
    @render_plotly
    def grafico_uso_vs_saude():
        df = load_data()
        
        # Tentar criar um gráfico relacionando tempo de uso e saúde
        if 'dailyusages' in df.columns and 'healthrating' in df.columns:
            # Simplificar health rating
            def simplify_rating(val):
                if isinstance(val, list):
                    return val[0]
                elif isinstance(val, str) and ";" in val:
                    return val.split(";")[0]
                return val
            
            df['health_simple'] = df['healthrating'].apply(simplify_rating)
            
            # Contagem para cada combinação
            health_by_usage = pd.crosstab(
                index=df['dailyusages'],
                columns=df['health_simple'],
                normalize='index'
            ) * 100
            
            # Ordenar índices se necessário
            if all(idx in ['<2hours', '2-4hours', '4-6hours', '>6hours'] for idx in health_by_usage.index):
                health_by_usage = health_by_usage.reindex(['<2hours', '2-4hours', '4-6hours', '>6hours'])
            
            # Converter para formato longo para plotly
            health_long = health_by_usage.reset_index().melt(
                id_vars=['dailyusages'],
                var_name='Health Rating',
                value_name='Percentage'
            )
            
            fig = px.bar(
                health_long,
                x='dailyusages',
                y='Percentage',
                color='Health Rating',
                barmode='stack',
                color_discrete_map={
                    'Excellent': '#4caf50',
                    'Good': '#8bc34a',
                    'Fair': '#ffc107',
                    'Poor': '#f44336'
                },
                labels={'dailyusages': 'Tempo de Uso Diário', 'Percentage': 'Porcentagem (%)'},
                title='Avaliação de Saúde por Tempo de Uso Diário'
            )
            
            fig.update_layout(
                height=400
            )
            return fig
        
        return go.Figure()
    
    @output
    @render_plotly
    def grafico_sintomas_vs_precaucoes():
        df = load_data()
        
        # Tentar criar um gráfico relacionando sintomas e precauções
        if 'usagesymptoms' in df.columns and 'healthprecautions' in df.columns:
            # Simplificar para quantidade de sintomas
            df['symptom_count'] = df['usagesymptoms'].apply(
                lambda x: len(x) if isinstance(x, list) else 1 if isinstance(x, str) else 0
            )
            
            # Agrupar por precauções
            symptom_by_precaution = df.groupby('healthprecautions')['symptom_count'].mean().sort_values()
            
            fig = go.Figure(go.Bar(
                x=symptom_by_precaution.index,
                y=symptom_by_precaution.values,
                marker_color='#a777e3',
                text=symptom_by_precaution.values.round(1),
                textposition='auto'
            ))
            
            fig.update_layout(
                title='Média de Sintomas Reportados por Tipo de Precaução',
                xaxis_title='Precaução',
                yaxis_title='Média de Sintomas',
                height=400
            )
            return fig
        
        return go.Figure()

app = App(app_ui, server) 