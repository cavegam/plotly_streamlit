import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.preprocessing import MinMaxScaler


#Configuración inicial
st.set_page_config(page_title="Tablero Estratégico", layout="wide")
st.title("📈 Tablero de ventas y clientes en El Salvador")

#Cargar datos (y cachear)
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1372xhg2BZ19cEA4lkABhjAN_1iyZ9cVv/edit?usp=sharing"
    file_id = url.split('/')[-2]
    dl_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    df = pd.read_excel(dl_url)
    # Filtrar solo El Salvador
    df = df[df['País/Región'] == 'El Salvador']
    return df

df = load_data()

# Prepara copia sin modificar el dataset original
df_raw = df.copy()

# —Construir date a partir del año y el mes de la venta
df_raw['date'] = (df_raw['año_pedido'].astype(str) + '-' + df_raw['mes_pedido'].astype(str).str.zfill(2)+ '-01')
# Convertir a datetime:
df_raw['date'] = pd.to_datetime(df_raw['date'], format='%Y-%m-%d')

#Widgets de filtro en la barra lateral
category_filter = st.sidebar.multiselect(
    "Categoría",
    options=df_raw["Categoría"].unique(),
    default=df_raw["Categoría"].unique()
)

segment_filter = st.sidebar.multiselect(
    "Segmento",
    options=df_raw["Segmento"].unique(),
    default=df_raw["Segmento"].unique()
)

shipping_filter = st.sidebar.multiselect(
    "Método de envío",
    options=df_raw["Método de envío"].unique(),
    default=df_raw["Método de envío"].unique()
)

# Aplicar filtros
df_filtered = df_raw[
    df_raw["Categoría"].isin(category_filter) &
    df_raw["Segmento"].isin(segment_filter) &
    df_raw["Método de envío"].isin(shipping_filter)
]

#KPIs singles values
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🛒 Cantidad de Ventas")
    st.markdown(f"# {len(df_filtered):,}")

with col2:
    total_fact = df_filtered["Ventas"].sum()
    st.markdown("### 🧾 Total Facturación")
    st.markdown(f"# ${total_fact:,.0f}")

with col3:
    total_gain = df_filtered["Ganancia"].sum()
    st.markdown("### 💰 Ganancia Total")
    st.markdown(f"# ${total_gain:,.0f}")

with col4:
    avg_venta = total_fact / len(df_filtered) if len(df_filtered) else 0
    st.markdown("### 🎟️ Venta Promedio")
    st.markdown(f"# ${avg_venta:,.2f}")

# Fila 1: Ventas Totales y Ganancias Totales
col1, col2 = st.columns(2)

with col1:
    ventas_totales = (
        df_filtered
        .groupby('Categoría', as_index=False)['Ventas']
        .sum()
        .sort_values('Ventas', ascending=False)
    )
    ventas_totales['%'] = (
        ventas_totales['Ventas'] / ventas_totales['Ventas'].sum() * 100
    ).round(1)

    fig1 = px.bar(
        ventas_totales,
        x='Categoría',
        y='Ventas',
        text='Ventas',
        title='Ventas totales por categoría de productos',
        color='Ventas',
        color_continuous_scale='Blues'
    )
    fig1.update_traces(
        texttemplate='%{text:,.0f}', 
        textposition='outside'
    )
    fig1.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        xaxis_title='Categoría',
        yaxis_title='Total Ventas'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    ganancias_totales = (
        df_filtered
        .groupby('Categoría', as_index=False)['Ganancia']
        .sum()
        .sort_values('Ganancia', ascending=False)
    )
    ganancias_totales['%'] = (
        ganancias_totales['Ganancia'] / ganancias_totales['Ganancia'].sum() * 100
    ).round(1)

    fig2 = px.bar(
        ganancias_totales,
        x='Categoría',
        y='Ganancia',
        text='Ganancia',
        title='Ganancias totales por categoría',
        color='Ganancia',
        color_continuous_scale='Blues'
    )
    fig2.update_traces(
        texttemplate='%{text:,.0f}', 
        textposition='outside'
    )
    fig2.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        xaxis_title='Categoría',
        yaxis_title='Total Ganancias'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Fila 2: Tendencia Mensual de Ventas y Ganancias

col3, col4 = st.columns(2)

with col3:
    
    ventas_totales_subcat = (
        df_filtered
        .groupby('Subcategoría', as_index=False)['Ventas']
        .sum()
        .sort_values('Ventas', ascending=False)
    )

    # Datos a graficar
    subcats = ventas_totales_subcat['Subcategoría']
    valores = ventas_totales_subcat['Ventas']

    # Creamos figura más compacta
    fig_subcat, ax_subcat = plt.subplots(figsize=(6, 4), dpi=100)

    # Escala de azules
    n = len(subcats)
    cmap = plt.cm.get_cmap('Blues', n)
    colores = [cmap(i) for i in range(n)]

    # Graficamos barras horizontales
    barras = ax_subcat.barh(subcats, valores, color=colores)

    # 6. Etiquetas con separador de miles
    labels = [f"{int(v):,}" for v in valores]
    ax_subcat.bar_label(barras, labels=labels, padding=3)

    # Etiquetas con separador de miles
    labels = [f"{int(v):,}" for v in valores]
    ax_subcat.bar_label(barras, labels=labels, padding=3)

    # Quitar bordes
    for spine in ax_subcat.spines.values():
        spine.set_visible(False)

    # Invertir eje y para que la subcategoría de mayor venta quede arriba
    ax_subcat.invert_yaxis()

    # Ajustar títulos y ejes con mismo tamaño de letra que en los demás gráficos
    ax_subcat.set_title(
        'Ventas totales por subcategoría de producto',
        fontsize=10, pad=10
    )
    ax_subcat.set_xlabel('Total Ventas', fontsize=8)
    ax_subcat.set_ylabel('Subcategoría', fontsize=8)

    # Mostrar en Streamlit
    st.pyplot(fig_subcat)


    # Gráfica 4: Ventas Totales por Segmento de Cliente

with col4:
    ventas_por_segmento = (
        df_filtered
        .groupby('Segmento', as_index=False)['Ventas']
        .sum()
        .sort_values('Ventas', ascending=False)
    )

    fig4 = px.bar(
        ventas_por_segmento,
        x='Segmento',
        y='Ventas',
        text='Ventas',
        title='Ventas totales por segmento de cliente',
        color='Ventas',
        color_continuous_scale='Blues'
    )
    # Etiquetas fuera de la barra y formato con separador de miles
    fig4.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside'
    )
    # Formato de ejes
    fig4.update_layout(
        xaxis_title='Segmento',
        yaxis_title='Total Ventas',
        yaxis_tickformat=',.0f',
        margin=dict(t=50, b=20, l=20, r=20)
    )

    st.plotly_chart(fig4, use_container_width=True)

#Fila 3
col5, col6 = st.columns(2)
col5 = st.columns(1)[0]

with col5:
    #Calculamos totales mensuales
    ventas_mes = (
        df_filtered
        .groupby(pd.Grouper(key='date', freq='M'))['Ventas']
        .sum()
        .reset_index()
    )
    ganancias_mes = (
        df_filtered
        .groupby(pd.Grouper(key='date', freq='M'))['Ganancia']
        .sum()
        .reset_index()
    )

    # Unimos en un mismo DataFrame y ordenamos
    df_trend = ventas_mes.merge(ganancias_mes, on='date', how='outer')
    df_melt = df_trend.melt(
        id_vars='date',
        value_vars=['Ventas','Ganancia'],
        var_name='Tipo',
        value_name='Valor'
    )

    # Gráfico de líneas con colores azules
    fig3 = px.line(
        df_melt,
        x='date',
        y='Valor',
        color='Tipo',
        markers=True,
        title='Evolución mensual de ventas y ganancias',
        color_discrete_map={
            'Ventas':'#023047',   
            'Ganancia': '#219ebc'  
        }
    )

    #Ajustes de diseño del gráfico
    fig3.update_layout(
        xaxis_title='Mes-Año',
        yaxis_title='Valor',
        legend_title_text='', 
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    #Mostrar en Streamlit
    st.plotly_chart(fig3, use_container_width=True)

col6 = st.columns(2)[0]

#Filtramos el dataset con los valores del último año, para el ejercicio es 2021
df_filtered['date'] = pd.to_datetime(df_filtered['date'], format='%Y-%m-%d')
df_2021 = df_filtered[df_filtered['date'].dt.year == 2021]

df_mes_2021 = (
    df_2021
    .groupby(pd.Grouper(key='date', freq='M'))[['Ventas', 'Ganancia']]
    .sum()
    .reset_index()
)

# Creamos un arreglo para ordenar los meses que vamos a presentar en la gráfica
meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
df_mes_2021['Mes'] = df_mes_2021['date'].dt.month.apply(lambda x: meses[x-1])

# Creamos la serie de datos que vamos a graficar
df_melt_2021 = df_mes_2021.melt(
    id_vars='Mes',
    value_vars=['Ventas', 'Ganancia'],
    var_name='Tipo',
    value_name='Valor'
)

# Creamos gráfico
fig = px.bar(
    df_melt_2021,
    x='Mes',
    y='Valor',
    color='Tipo',
    barmode='group',
    text='Valor',
    category_orders={'Mes': meses, 'Tipo': ['Ventas','Ganancia']},
    color_discrete_map={
            'Ventas':'#023047',   
            'Ganancia': '#219ebc'  
    },
    title='📊 Ventas y ganancias del último año (2021)'
)

# Ajustes de formato
fig.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside'
)
fig.update_layout(
    xaxis_title='Mes',
    yaxis_title='Valor',
    legend_title_text='',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=True)


# Realizaddo
st.markdown("*Realizado por Carlos Vega y Rafael Fuentes*")