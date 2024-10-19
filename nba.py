import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')


NBA = pd.read_csv('data/nba.csv')
NBA_NUM = NBA[['age', 'player_height', 'player_weight', 'gp', 'pts', 'reb', 'ast', 'net_rating',
               'oreb_pct', 'dreb_pct', 'usg_pct', 'ts_pct', 'ast_pct']]
NBA_NUM.replace('Undrafted', 0, inplace=True)

NBA_score = NBA[['player_name','age', 'player_height', 'player_weight', 'gp', 'pts', 'reb', 'ast', 'net_rating', 'season']]
NBA_score['season_score'] = (NBA_score['pts'] + NBA_score['reb'] + NBA_score['ast'])
NBA_score['game_score'] = NBA_score['season_score'] / NBA_score['gp']


def mapa_de_calor():
    st.subheader("Mapa de Calor das Correlações")
    corr = NBA_NUM.corr(numeric_only=True)

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='Viridis'))

    fig.update_layout(title='Mapa de Calor das Correlações', xaxis_nticks=36)
    st.plotly_chart(fig)


def histograma_pontos_idade():
    st.subheader("Distribuição de Pontos por Idade")
    fig = px.histogram(NBA_NUM, x='age', nbins=10, color='pts', marginal="box", hover_data=NBA_NUM.columns)
    fig.update_layout(title="Distribuição de Pontos por Idade")
    st.plotly_chart(fig)


def jogadores_mais_30_pontos():
    st.subheader("Jogadores com +30 Pontos por Faixa Etária")
    
    mais_30 = NBA[(NBA['age'] >= 30) & (NBA['pts'] >= 30)]
    menos_30 = NBA[(NBA['age'] > 25) & (NBA['age'] < 30) & (NBA['pts'] >= 30)]
    menos_25 = NBA[(NBA['age'] <= 25) & (NBA['pts'] >= 30)]

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=mais_30['player_name'],
        y=mais_30['pts'],
        name='> 30 anos',
        marker_color='red'
    ))

    fig.add_trace(go.Bar(
        x=menos_30['player_name'],
        y=menos_30['pts'],
        name='25-30 anos',
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=menos_25['player_name'],
        y=menos_25['pts'],
        name='< 25 anos',
        marker_color='green'
    ))

    fig.update_layout(barmode='group', title='Jogadores com +30 Pontos por Faixa Etária')
    st.plotly_chart(fig)


def comparacao_estrelas():
    st.subheader("Comparação de Game Score entre Estrelas da NBA")
    
    tabela_lebron = NBA_score[NBA_score['player_name'] == 'LeBron James']
    game_score_mean_lebron = tabela_lebron['game_score'].mean()

    giannis = NBA_score[NBA_score['player_name'] == 'Giannis Antetokounmpo']
    media_giannis = giannis['game_score'].mean()

    doncic = NBA_score[NBA_score['player_name'] == 'Luka Doncic']
    medi_doncic = doncic['game_score'].mean()

    kobe = NBA_score[NBA_score['player_name'] == 'Kobe Bryant']
    media_kobe = kobe['game_score'].mean()

    embiid = NBA_score[NBA_score['player_name'] == 'Joel Embiid']
    media_embiid = embiid['game_score'].mean()

    stars = pd.DataFrame({
        'Jogador': ['LeBron James', 'Luka Doncic', 'Giannis Antetokounmpo', 'Kobe Bryant', 'Joel Embiid'],
        'Média Game Score': [game_score_mean_lebron, medi_doncic, media_giannis, media_kobe, media_embiid]
    })

    fig = px.line(stars, x='Jogador', y='Média Game Score', markers=True, title='Comparação de Game Score entre Estrelas')
    st.plotly_chart(fig)


def tendencia_game_score_idade():
    st.subheader("Tendência do Game Score com a Idade")
    
    age_mean_game_score = NBA_score.groupby('age')['game_score'].mean().reset_index()

    fig = px.line(age_mean_game_score, x='age', y='game_score', title='Tendência do Game Score com a Idade')
    st.plotly_chart(fig)


st.title("Análise de Desempenho de Jogadores da NBA")


st.sidebar.title("Selecione a visualização:")
option = st.sidebar.selectbox(
    'Escolha o gráfico:',
    ['Mapa de Calor', 'Distribuição de Pontos por Idade', 'Jogadores com +30 Pontos por Idade',
     'Comparação entre Estrelas', 'Tendência de Game Score por Idade']
)

if option == 'Mapa de Calor':
    mapa_de_calor()
elif option == 'Distribuição de Pontos por Idade':
    histograma_pontos_idade()
elif option == 'Jogadores com +30 Pontos por Idade':
    jogadores_mais_30_pontos()
elif option == 'Comparação entre Estrelas':
    comparacao_estrelas()
elif option == 'Tendência de Game Score por Idade':
    tendencia_game_score_idade()

