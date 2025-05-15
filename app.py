import streamlit as st
import pandas as pd
import plotly.express as px

# Título
st.title("🌎 World Happiness Dashboard (Datos simulados)")

# Dataset simulado
data = {
    "Country": [
        "Noruega", "Canadá", "Colombia", "Argentina", "Brasil",
        "Japón", "Corea del Sur", "India", "Nigeria", "Sudáfrica"
    ],
    "Region": [
        "Europa", "América", "América", "América", "América",
        "Asia", "Asia", "Asia", "África", "África"
    ],
    "Score": [7.7, 7.6, 6.2, 6.0, 6.3, 5.9, 6.1, 4.2, 5.0, 4.8],
    "GDP per capita": [1.6, 1.5, 1.1, 1.2, 1.3, 1.4, 1.5, 0.9, 0.8, 0.85],
    "Freedom": [0.9, 0.92, 0.8, 0.7, 0.75, 0.6, 0.65, 0.5, 0.55, 0.58]
}

df = pd.DataFrame(data)

# Filtro en la parte superior
region = st.selectbox("🎯 Selecciona una región:", options=df["Region"].unique())
#st.sidebar.header("🎯 Filtros")
#region = st.sidebar.selectbox("Selecciona una región:", options=df["Region"].unique())


# Filtrar datos
filtered_df = df[df["Region"] == region]

# Mostrar tabla
st.subheader(f"📋 Países en la región: {region}")
st.dataframe(filtered_df)

# Gráfico de barras
st.subheader("🏆 Score de felicidad")
fig1 = px.bar(filtered_df.sort_values(by="Score", ascending=False),
              x="Country", y="Score", color="Score",
              title="Ranking de felicidad en la región")
st.plotly_chart(fig1)

# Gráfico de dispersión
st.subheader("📊 PIB per cápita vs Score de felicidad")
fig2 = px.scatter(filtered_df, x="GDP per capita", y="Score",
                  color="Country", size="Score",
                  title="Relación entre PIB y Felicidad")
st.plotly_chart(fig2)
