import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial
st.set_page_config(page_title="Strategic Dashboard", layout="wide")
st.title("📱 Strategic Dashboard - Mobile App User Segments")

# Cargar datos
@st.cache_data
def load_data():
    url = "hhttps://drive.google.com/file/d/1xOl3nNCsIChPjWH6E75J5O5FpCczi_dQ/view?usp=sharing"
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    #path = 'user_behavior_dataset.csv'
    df = pd.read_csv(path)
    return df

df = load_data()

# Filtros en fila superior
#colf1, colf2, colf3 = st.columns(3)
#with colf1:
#    os_filter = st.multiselect(
#        "Sistema operativo",
#        options=df["Operating System"].unique(),
#        default=df["Operating System"].unique()
#    )
#
#with colf2:
#    gender_filter = st.multiselect(
#        "Género",
#        options=df["Gender"].unique(),
#        default=df["Gender"].unique()
#    )
#
#with colf3:
#    behavior_filter = st.multiselect(
#        "Clase de comportamiento",
#        options=sorted(df["User Behavior Class"].unique()),
#        default=sorted(df["User Behavior Class"].unique())
#    )

os_filter = st.sidebar.multiselect(
    "Sistema operativo",
    options=df["Operating System"].unique(),
    default=df["Operating System"].unique()
)

gender_filter = st.sidebar.multiselect(
    "Género",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

behavior_filter = st.sidebar.multiselect(
    "Clase de comportamiento",
    options=sorted(df["User Behavior Class"].unique()),
    default=sorted(df["User Behavior Class"].unique())
)

# Filtrar el dataframe
df_filtered = df[
    (df["Operating System"].isin(os_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["User Behavior Class"].isin(behavior_filter))
]

# KPIs (compacto)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Usuarios analizados", len(df_filtered))
with col2:
    st.metric("⏱️ Uso promedio (min)", round(df_filtered["App Usage Time (min/day)"].mean(), 1))
with col3:
    st.metric("🔋 Batería promedio (mAh)", round(df_filtered["Battery Drain (mAh/day)"].mean(), 1))
with col4:
    st.metric("📱 Apps instaladas (prom)", round(df_filtered["Number of Apps Installed"].mean(), 1))

# Fila 1
colv1, colv2, colv3 = st.columns(3)

with colv1:
    fig1 = px.box(
        df_filtered,
        x="User Behavior Class",
        y="App Usage Time (min/day)",
        title="Uso por clase de usuario",
        points="all"
    )
    st.plotly_chart(fig1, use_container_width=True)

with colv2:
    avg_data = df_filtered.groupby("Operating System")["Data Usage (MB/day)"].mean().reset_index()
    fig2 = px.bar(avg_data, x="Operating System", y="Data Usage (MB/day)", title="Uso de datos por OS")
    st.plotly_chart(fig2, use_container_width=True)

with colv3:
    fig3 = px.violin(
        df_filtered,
        x="Gender",
        y="Screen On Time (hours/day)",
        box=True,
        title="Tiempo de pantalla por género"
    )
    st.plotly_chart(fig3, use_container_width=True)

# Fila 2
colv4, colv5 = st.columns(2)

with colv4:
    fig4 = px.histogram(
        df_filtered,
        x="Number of Apps Installed",
        nbins=20,
        title="Distribución de apps instaladas"
    )
    st.plotly_chart(fig4, use_container_width=True)

with colv5:
    gender_df = df_filtered.groupby(["Gender", "User Behavior Class"]).size().reset_index(name="count")
    fig6 = px.bar(
        gender_df,
        x="User Behavior Class",
        y="count",
        color="Gender",
        barmode="group",
        title="Clase de usuario por género"
    )
    st.plotly_chart(fig6, use_container_width=True)

# Conclusiones
st.markdown("*Realizado por Sharon Camacho*")

