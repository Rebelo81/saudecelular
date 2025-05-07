# 📱 Impacto do Uso de Celulares na Educação e Saúde

Este projeto analisa o comportamento de estudantes em relação ao uso de celulares, explorando como isso afeta **saúde física/mental** e **desempenho educacional**. A análise combina dados reais, estatísticas descritivas e dashboards interativos construídos com **Shiny para Python** e **Plotly**.

---

## 📊 Visualização

![Matriz de Correlação](plots/correlacao_uso_celular.png)

---

## 📁 Estrutura do Projeto

```
saudecelular/
├── app/                      → Aplicativos com Shiny e Plotly
│   ├── app.py
│   ├── app_deploy.py
│   └── dashboard_executivo.py
├── data/                     → Dados originais e tratados
│   ├── saudevscelular.csv
│   └── dados_uso_celular_limpos.csv
├── scripts/                  → Análise estatística com matplotlib/seaborn
│   └── saudevscelular.py
├── plots/                    → Gráficos gerados
│   └── correlacao_uso_celular.png
├── notebooks/                → Jupyter notebooks (opcional)
│   └── SaudeVsMiniTelas.ipynb
├── requirements.txt          → Dependências
├── README.md                 → Este arquivo
├── .gitignore                → Ignora arquivos temporários
└── como_compartilhar.md      → Guia para divulgar no LinkedIn
```

## 💡 Tecnologias Utilizadas

- Python 3
- Pandas, Numpy, Seaborn, Matplotlib
- Shiny para Python
- Plotly
- ShinyWidgets
- rsconnect-python

---

## 📎 Fonte dos Dados

- [Kaggle - Students Health and Academic Performance](https://www.kaggle.com/datasets/innocentmfa/students-health-and-academic-performance/data)
- Coletados via Google Forms, conforme descrição do autor

---

## 👨‍💻 Autor

Paulo Rebelo – [github.com/Rebelo81](https://github.com/Rebelo81)
