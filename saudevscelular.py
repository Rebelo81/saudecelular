import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

plt.style.use('ggplot')
sns.set_palette('Set2')

def load_data(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Formato de arquivo não suportado")
        logging.info(f"Dados carregados com sucesso: {df.shape[0]} linhas e {df.shape[1]} colunas")
        logging.info(f"Colunas disponíveis: {df.columns.tolist()}")
        return df
    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        return None

def clean_data(df):
    logging.info("Iniciando limpeza de dados...")
    df_clean = df.copy()
    df_clean.columns = [col.strip().replace('_', '').replace(' ', '').lower() for col in df_clean.columns]

    if 'names' in df_clean.columns:
        df_clean = df_clean[df_clean['names'] != 'Mehvish']

    cat_cols = ['gender', 'mobileoperatingsystem', 'mobilephoneuseforeducation', 
                'mobilephoneactivities', 'helpfulforstudying', 'educationalapps',
                'performanceimpact', 'usagedistraction', 'attentionspan',
                'usefulfeatures', 'healthrisks', 'beneficialsubject',
                'usagesymptoms', 'symptomfrequency', 'healthprecautions', 'healthrating']
    
    for col in cat_cols:
        if col in df_clean.columns:
            df_clean.loc[:, col] = df_clean[col].fillna(df_clean[col].mode()[0])

    if 'age' in df_clean.columns:
        df_clean['age'] = pd.Categorical(df_clean['age'], categories=['16-20', '21-25', '26-30', '31-35'], ordered=True)

    for col in ['mobilephoneactivities', 'usagesymptoms', 'healthrating']:
        if col in df_clean.columns and df_clean[col].dtype == 'object':
            df_clean.loc[:, col] = df_clean[col].str.split(';')

    if 'dailyusages' in df_clean.columns:
        df_clean['dailyusages'] = pd.Categorical(df_clean['dailyusages'], categories=['<2hours', '2-4hours', '4-6hours', '>6hours'], ordered=True)

    logging.info(f"Limpeza concluída. Dimensões finais: {df_clean.shape[0]} linhas e {df_clean.shape[1]} colunas")
    return df_clean

def exploratory_analysis(df):
    logging.info("Iniciando análise exploratória...")

    def simplify_multiple(value):
        if isinstance(value, list):
            if 'All of these' in value:
                return 'All of these'
            elif len(value) > 1:
                return 'Multiple'
            elif len(value) == 1:
                return value[0]
        elif isinstance(value, str):
            if 'All of these' in value:
                return 'All of these'
            elif ';' in value:
                return 'Multiple'
            return value
        return 'Not specified'

    def simplify_rating(value):
        if isinstance(value, list):
            return value[0]
        elif isinstance(value, str) and ';' in value:
            return value.split(';')[0]
        return value

    df['simplified_activities'] = df['mobilephoneactivities'].apply(simplify_multiple)
    df['simplified_symptoms'] = df['usagesymptoms'].apply(simplify_multiple)
    df['simplified_health'] = df['healthrating'].apply(simplify_rating)

    def show(title, series):
        dist = series.value_counts(normalize=True) * 100
        logging.info(f"\n{title}\n{(dist.round(1).astype(str) + '%').to_string()}")

    show("Distribuição por idade", df['age'])
    show("Distribuição por gênero", df['gender'])
    show("Sistema operacional", df['mobileoperatingsystem'])
    show("Tempo de uso diário", df['dailyusages'])
    show("Atividades", df['simplified_activities'])
    show("Uso para educação", df['mobilephoneuseforeducation'])
    show("Apps educacionais", df['educationalapps'])
    show("Utilidade nos estudos", df['helpfulforstudying'])
    show("Impacto no desempenho", df['performanceimpact'])
    show("Distrações", df['usagedistraction'])
    show("Capacidade de atenção", df['attentionspan'])
    show("Sintomas", df['simplified_symptoms'])
    show("Frequência dos sintomas", df['symptomfrequency'])
    show("Precauções de saúde", df['healthprecautions'])
    show("Autoavaliação de saúde", df['simplified_health'])
    show("Recursos úteis", df['usefulfeatures'])
    show("Riscos percebidos", df['healthrisks'])
    show("Áreas beneficiadas", df['beneficialsubject'])

    logging.info("Análise exploratória concluída.")
    return df

def correlation_analysis(df):
    logging.info("Iniciando análise de correlação...")

    maps = {
        'mobilephoneuseforeducation': {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1},
        'dailyusages': {'<2hours': 1, '2-4hours': 2, '4-6hours': 3, '>6hours': 4},
        'performanceimpact': {'Stronglyagree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Stronglydisagree': 1},
        'symptomfrequency': {'Frequently': 4, 'Sometimes': 3, 'Rarely': 2, 'Never': 1},
        'simplified_health': {'Excellent': 4, 'Good': 3, 'Fair': 2, 'Poor': 1}
    }

    for col, mapping in maps.items():
        if col in df.columns:
            df[col + '_num'] = df[col].map(mapping)

    numeric = [col for col in df.columns if col.endswith('_num')]
    corr = df[numeric].corr()

    os.makedirs('plots', exist_ok=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
    plt.title('Matriz de Correlação')
    plt.tight_layout()
    plt.savefig('plots/correlacao_uso_celular.png', dpi=300)
    plt.close()

    logging.info("Matriz de correlação salva em plots/correlacao_uso_celular.png")

    unstacked = corr.unstack()
    unstacked = unstacked[unstacked < 1.0]
    top_pos = unstacked.nlargest(3)
    top_neg = unstacked.nsmallest(3)

    logging.info("Top 3 correlações positivas mais fortes:")
    for (a, b), val in top_pos.items():
        logging.info(f"{a} e {b}: {val:.2f} → quando uma aumenta, a outra também tende a aumentar.")

    logging.info("Top 3 correlações negativas mais fortes:")
    for (a, b), val in top_neg.items():
        logging.info(f"{a} e {b}: {val:.2f} → quando uma aumenta, a outra tende a diminuir.")

def main():
    file_path = "saudevscelular.csv"
    df = load_data(file_path)

    if df is not None:
        df_clean = clean_data(df)
        df_analyzed = exploratory_analysis(df_clean)
        correlation_analysis(df_analyzed)

        os.makedirs('plots', exist_ok=True)
        df_clean.to_csv("dados_uso_celular_limpos.csv", index=False)
        logging.info("Dados limpos salvos em dados_uso_celular_limpos.csv")
        logging.info("Análise finalizada com sucesso.")

if __name__ == "__main__":
    main()

from pathlib import Path


