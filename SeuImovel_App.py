import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk


st.set_page_config(page_title= 'App Your Property', layout="wide")


with st.container():
    st.subheader('App Your Property')
    st.title('Análise de Imóveis')
    st.write('Saiba mais informações sobre os imóveis da região de sua escolha!')

@st.cache_data
def dados():
    dataframe = pd.read_csv('houses_to_rent_v2.csv', encoding='latin-1')
    return dataframe

def formatar_valor_brasileiro(valor):
    valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f'R$ {valor_formatado}'

with st.container():
    st.write("---")
    df = dados()
    coluna_unica = df['city'].drop_duplicates()
    itens_unicos = coluna_unica.nunique()
    print(coluna_unica)

    opcoes_city = sorted(df['city'].unique())
    cidade_selecionada = st.selectbox('Selecione a cidade que deseja:', opcoes_city)
    df_filtrado = df[df['city'] == cidade_selecionada]
    #st.dataframe(df_filtrado) #depois lembra de ocultar isso

with st.container():

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)



    custo_total_medio = df_filtrado['total (R$)'].mean()
    custo_hoa = df_filtrado['hoa (R$)'].mean()
    custo_rent = df_filtrado['rent amount (R$)'].mean()
    custo_tax = df_filtrado['property tax (R$)'].mean()
    custo_fire = df_filtrado['fire insurance (R$)'].mean()
    num_imoveis = df_filtrado.shape[0]


    custo_total_medio_formatado = formatar_valor_brasileiro(custo_total_medio)
    custo_hoa_formatado = formatar_valor_brasileiro(custo_hoa)
    custo_rent_formatado = formatar_valor_brasileiro(custo_rent)
    custo_tax_formatado = formatar_valor_brasileiro(custo_tax)
    custo_fire_formatado = formatar_valor_brasileiro(custo_fire)



    col1.metric(label = f"**Número de Imóveis Analisados:**", value = f'{num_imoveis}')
    col2.metric(label = f"**Custo Total Médio na região:**", value = f'{custo_total_medio_formatado:}')
    col3.metric(label = f"**Custo Médio da taxa para Manutenção e Administração na região:**", value = f' {custo_hoa_formatado:}')
    col4.metric(label= f"**Custo Médio do Aluguel na região:**", value = f' {custo_rent_formatado:}')
    col5.metric(label= f"**Custo Médio do IPTU na região:**", value = f' {custo_tax_formatado:}')
    col6.metric(label= f"**Custo Médio do Seguro contra incêndio na região:**", value = f' {custo_fire_formatado:}')



col7, col8, col9 = st.columns(3)

with col7:
    with st.container():

        Categorias=['Taxa de Manutenção e Serviço', 'Aluguel', 'IPTU', 'Seguro contra Incêndio']
        Valores=[custo_hoa,custo_rent,custo_tax,custo_fire]

        fig = px.pie(
            names=Categorias,
            values=Valores,
            title="Composição do Custo Total Médio de um Imóvel na Região.",
        )
        valores_formatados=[formatar_valor_brasileiro(v) for v in Valores]
        fig.update_traces(
            text=valores_formatados,
            textinfo='label+percent',
            hovertemplate='%{label}<br>Valor: %{text}<br>Porcentagem: %{percent}<extra></extra>'
        )
        fig.update_layout(
            margin=dict(l=1, r=200, t=70, b=30),
            showlegend=False)
        st.plotly_chart(fig)

with col8:
    with st.container():

        contagem_pet = df_filtrado['animal'].value_counts()

        aceitam_pet = contagem_pet.get('acept',0)
        nao_aceitam_pet = contagem_pet.get('not acept',0)

        Categorias = ['Pet Friendly', 'Não aceitam pet']
        Valores = [aceitam_pet, nao_aceitam_pet]

        fig = px.pie(
            names=Categorias,
            values=Valores,
            title="Quantidade de imóveis que aceitam animais."

        )

        fig.update_traces(
            textinfo='label+percent',
            hovertemplate='%{label}<br>Valor: %{value}<br>Porcentagem: %{percent}<extra></extra>'
        )
        fig.update_layout(
            margin=dict(l=1, r=200, t=70, b=30),
            showlegend=False)
        st.plotly_chart(fig)

with col9:
    with st.container():
        contagem_mobiliado = df_filtrado['furniture'].value_counts()
        mobiliado = contagem_mobiliado.get('furnished',0)
        nao_mobiliado = contagem_mobiliado.get('not furnished',0)

        Categorias = ['Mobiliado', 'Não mobiliado']
        Valores = [mobiliado, nao_mobiliado]

        fig = px.pie(
            names=Categorias,
            values=Valores,
            title="Quantidade de imóveis mobiliados."
        )
        fig.update_traces(
            textinfo='label+percent',
            hovertemplate='%{label}<br>Valor: %{value}<br>Porcentagem: %{percent}<extra></extra>'
        )
        fig.update_layout(
            margin=dict(l=1, r=200, t=70, b=30),
            showlegend=False)
        st.plotly_chart(fig)

col10, col11 = st.columns(2)
with col10:
    with st.container():

        #areas = df_filtrado['area'].unique()
        #areas_ordenadas = sorted(areas)
        #print(areas_ordenadas)
        bins = [0, 50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, float('inf')]
        labels = ['0-50 m²', '51-100 m²', '101-150 m²', '151-200 m²', '201-250 m²',
          '251-300 m²', '301-400 m²', '401-500 m²', '501-600 m²', '601-700 m²',
          '701-800 m²', '801-900 m²', '901-1000 m²', 'Acima de 1000 m²']

        df_filtrado['Intervalo de área'] = pd.cut(df_filtrado['area'], bins=bins, labels=labels, right=False)
        contagem_area = df_filtrado.groupby('Intervalo de área').size().reset_index(name='Número de Imóveis')
        contagem_area['Intervalo de área'] = pd.Categorical(contagem_area['Intervalo de área'], categories=labels, ordered=True)
        contagem_area=contagem_area.sort_values('Intervalo de área')

        fig = px.bar(contagem_area,
                     x='Intervalo de área',
                     y='Número de Imóveis',
                     title='Número de Imóveis por Intervalo de Área',
                     labels={'Número de Imóveis': 'Número de Imóveis', 'Intervalo de área': 'Intervalo de Área'},
                     color='Número de Imóveis',
                     color_continuous_scale=px.colors.sequential.Viridis
                     )

        st.plotly_chart(fig)

with col11:
    with st.container():
        #quartos = df_filtrado['rooms'].unique()
        #quartos_ordenados = sorted(quartos)
        #print(quartos_ordenados)
        contagem_quartos = df_filtrado['rooms'].value_counts().reset_index()
        contagem_quartos.columns = ['Quartos', 'Número de imóveis']
        fig = px.bar(contagem_quartos,
             x='Quartos',
             y='Número de imóveis',
             title='Número de Quartos por Imóvel',
             labels={'Número de imóveis': 'Número de imóveis', 'Quartos': 'Quartos'},
             color='Número de imóveis',
             color_continuous_scale=px.colors.sequential.Viridis

        )
        st.plotly_chart(fig)
col12, col13 = st.columns(2)
with col12:
    with st.container():

        contagem_banheiros = df_filtrado['bathroom'].value_counts().reset_index()
        contagem_banheiros.columns = ['Banheiros', 'Número de imóveis']
        fig = px.bar(contagem_banheiros,
             x='Banheiros',
             y='Número de imóveis',
             title='Número de Banheiros por Imóvel',
             labels={'Número de imóveis': 'Número de imóveis', 'Banheiros': 'Banheiros'},
             color='Número de imóveis',
             color_continuous_scale=px.colors.sequential.Viridis
        )

        st.plotly_chart(fig)

with col13:
    with st.container():
        contagem_estacionamento = df_filtrado['parking spaces'].value_counts().reset_index()
        contagem_estacionamento.columns = ['Estacionamento', 'Número de imóveis']
        fig = px.bar(contagem_estacionamento,
                     x='Estacionamento',
                     y='Número de imóveis',
                     title='Número de Vagas de Estacionamento por Imóvel',
                     labels={'Número de imóveis': 'Número de imóveis', 'Estacionamento': 'Estacionamento'},
                     color='Número de imóveis',
                     color_continuous_scale=px.colors.sequential.Viridis
                     )

        st.plotly_chart(fig)
col13, col14 = st.columns(2)
with col13:
    with st.container():
        contagem_floor = df_filtrado['floor'].value_counts().reset_index()
        contagem_floor.columns = ['Andar', 'Número de imóveis']

        fig = px.bar(contagem_floor,
                     x='Andar',
                     y='Número de imóveis',
                     title='Número de Imóveis por Intervalo de andares',
                     labels={'Número de Imóveis': 'Número de Imóveis', 'Intervalo de andares': 'Intervalo de andares'},
                     color='Número de imóveis',
                     color_continuous_scale=px.colors.sequential.Viridis
                     )
        fig.update_layout(
            xaxis=dict(range=[0,40]),
            yaxis=dict(range=[0, max(contagem_floor['Número de imóveis']) + 10])

        )

        st.plotly_chart(fig)

with col14:
    with st.container():
        fig = px.scatter(df_filtrado,
                        x='area',
                        y='total (R$)',
                        title='Relação entre Área e Valor do Imóvel',
                        labels={'area': 'Área (m²)', 'total (R$)': 'Valor do Imóvel (R$)'},
                        color='total (R$)',
                        color_continuous_scale=px.colors.sequential.Viridis
                        )

        fig.update_layout(
            xaxis=dict(range=[0, 3000]),
            yaxis=dict(range=[0, max(df_filtrado['total (R$)']) + 20])

        )
        st.plotly_chart(fig)

col15, col16 = st.columns(2)
with col15:
    with st.container():
        fig = px.scatter(df_filtrado,
                        x='rooms',
                        y='total (R$)',
                        title='Relação entre Quantidade de Quartos e Valor do Imóvel',
                        labels={'rooms': 'Quantidade de quartos', 'total (R$)': 'Valor do Imóvel (R$)'},
                        color='total (R$)',
                        color_continuous_scale=px.colors.sequential.Viridis
                        )

        fig.update_layout(
            xaxis=dict(range=[0, 15]),
            yaxis=dict(range=[0, max(df_filtrado['total (R$)']) + 20])

        )
        st.plotly_chart(fig)

with col16:
    with st.container():
        fig = px.scatter(df_filtrado,
                         x='bathroom',
                         y='total (R$)',
                         title='Relação entre Quantidade de Banheiros e Valor do Imóvel',
                         labels={'bathroom': 'Quantidade de Banheiros', 'total (R$)': 'Valor do Imóvel (R$)'},
                         color='total (R$)',
                         color_continuous_scale=px.colors.sequential.Viridis
                         )

        fig.update_layout(
            xaxis=dict(range=[0, 15]),
            yaxis=dict(range=[0, max(df_filtrado['total (R$)']) + 20])

        )
        st.plotly_chart(fig)

col17, col18 = st.columns(2)

with col17:
    with st.container():
        fig = px.scatter(df_filtrado,
                         x='parking spaces',
                         y='total (R$)',
                         title='Relação entre Quantidade de Vagas de Estacionamento e Valor do Imóvel',
                         labels={'parking spaces': 'Vagas de Estacionamento', 'total (R$)': 'Valor do Imóvel (R$)'},
                         color='total (R$)',
                         color_continuous_scale=px.colors.sequential.Viridis
                         )

        fig.update_layout(
            xaxis=dict(range=[0, 15]),
            yaxis=dict(range=[0, max(df_filtrado['total (R$)']) + 20])

        )
        st.plotly_chart(fig)

with col18:
    with st.container():
        fig = px.scatter(df_filtrado,
                         x='floor',
                         y='total (R$)',
                         title='Relação entre Número de Andares e Valor do Imóvel',
                         labels={'floor': 'Quantidade de Número de Andares', 'total (R$)': 'Valor do Imóvel (R$)'},
                         color='total (R$)',
                         color_continuous_scale=px.colors.sequential.Viridis
                         )

        fig.update_layout(
            xaxis=dict(range=[0, 15]),
            yaxis=dict(range=[0, max(df_filtrado['total (R$)']) + 20])

        )
        st.plotly_chart(fig)


with st.container():
    st.write("---")
    st.title("Mapa do Brasil dos Imóveis")

    media_imoveis = df.groupby('city')['total (R$)'].mean().reset_index()
    coordenadas = {
        "Belo Horizonte": (-19.9191, -43.9386),
        "Rio de Janeiro": (-22.9068, -43.1729),
        "São Paulo": (-23.5505, -46.6333),
        "Porto Alegre": (-30.0346, -51.2177),
        "Campinas": (-22.9056, -47.0608),
    }

    media_imoveis['latitude'] = media_imoveis['city'].map(lambda x: coordenadas[x][0] if x in coordenadas else None)
    media_imoveis['longitude'] = media_imoveis['city'].map(lambda x: coordenadas[x][1] if x in coordenadas else None)

    media_imoveis['valor_normalizado'] = (media_imoveis['total (R$)'] - media_imoveis['total (R$)'].min()) / (
                media_imoveis['total (R$)'].max() - media_imoveis['total (R$)'].min())


    def calcular_cor(valor_normalizado):
        r = int(255 * valor_normalizado)
        g = int(255 * (1 - valor_normalizado))
        b = 0
        return [r, g, b, 180]


    media_imoveis['cor'] = media_imoveis['valor_normalizado'].apply(calcular_cor)

    layer = pdk.Layer(
        'ScatterplotLayer',
        media_imoveis.dropna(subset=['latitude', 'longitude']),
        get_position='[longitude, latitude]',
        get_color='cor',
        get_radius=30000,
        pickable=True,
    )
    view_state = pdk.ViewState(
        latitude=media_imoveis['latitude'].mean(),
        longitude=media_imoveis['longitude'].mean(),
        zoom=5,
        pitch=0,
    )

    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    st.pydeck_chart(deck)
    st.subheader("Legenda:")
    st.write("""
    - **Verde**: Valor médio mais baixo
    - **Amarelo**: Valor médio moderado
    - **Laranja**: Valor médio alto
    - **Vermelho**: Valor médio muito alto
    """)

    st.subheader("Média do Valor dos Imóveis por Cidade")
    media_imoveis_sorted = media_imoveis.sort_values(by='total (R$)', ascending=False)
    fig = px.bar(media_imoveis_sorted,
                 x='total (R$)',
                 y='city',
                 orientation='h',
                 title='Média do Valor dos Imóveis por Cidade',
                 labels={'total (R$)': 'Valor Médio (R$)', 'city': 'Cidade'},
                 color='total (R$)',
                 color_continuous_scale='Blues')

    st.plotly_chart(fig)