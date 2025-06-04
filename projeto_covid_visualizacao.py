import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import networkx as nx

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)

brasil = df[df['location'] == 'Brazil']

brasil['date'] = pd.to_datetime(brasil['date'])


brasil['month'] = brasil['date'].dt.to_period('M')
vacinas_por_mes = brasil.groupby('month')['new_vaccinations'].sum().reset_index()

plt.figure(figsize=(10,6))
sns.barplot(x='month', y='new_vaccinations', data=vacinas_por_mes, color='skyblue')
plt.title('Doses de Vacinas Aplicadas por Mês no Brasil')
plt.ylabel('Doses Aplicadas')
plt.xlabel('Mês')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


plt.figure(figsize=(12,6))
sns.lineplot(x='date', y='people_vaccinated', data=brasil, label='Pessoas Vacinadas')
sns.lineplot(x='date', y='people_fully_vaccinated', data=brasil, label='Totalmente Vacinadas')
plt.title('Evolução da Vacinação no Brasil')
plt.xlabel('Data')
plt.ylabel('Número de Pessoas')
plt.legend()
plt.grid(alpha=0.3)
plt.show()


dados = {
    'estado': ['SP', 'RJ', 'MG', 'RS', 'BA', 'PR', 'SC', 'PE', 'CE', 'PA'],
    'percentual_vacinado': [85, 80, 78, 83, 75, 82, 84, 77, 76, 70]
}

df_estado = pd.DataFrame(dados)

fig = px.choropleth(
    df_estado,
    locations='estado',
    locationmode='ISO-3166-2:BR',
    color='percentual_vacinado',
    color_continuous_scale="Viridis",
    scope="south america",
    title='Porcentagem da População Vacinada por Estado'
)
fig.show()


fabricantes = {
    'fabricante': ['Pfizer', 'AstraZeneca', 'CoronaVac', 'Janssen'],
    'doses': [120000000, 100000000, 90000000, 20000000]
}

df_fabricantes = pd.DataFrame(fabricantes)

fig = px.treemap(
    df_fabricantes,
    path=['fabricante'],
    values='doses',
    title='Distribuição de Doses por Fabricante no Brasil'
)
fig.show()


G = nx.Graph()

estados = ['SP', 'RJ', 'MG', 'RS', 'BA']
fabricantes = ['Pfizer', 'AstraZeneca', 'CoronaVac', 'Janssen']

G.add_nodes_from(estados, bipartite=0)
G.add_nodes_from(fabricantes, bipartite=1)

edges = [
    ('SP', 'Pfizer'), ('SP', 'AstraZeneca'),
    ('RJ', 'CoronaVac'), ('RJ', 'Pfizer'),
    ('MG', 'AstraZeneca'), ('MG', 'Janssen'),
    ('RS', 'CoronaVac'), ('RS', 'Pfizer'),
    ('BA', 'AstraZeneca'), ('BA', 'Janssen')
]

G.add_edges_from(edges)

plt.figure(figsize=(8,8))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx(G, pos, with_labels=True, node_size=700, node_color='lightblue')
plt.title('Rede de Estados e Fabricantes de Vacinas')
plt.axis('off')
plt.show()
