# 📘 Introducción a Streamlit

[Streamlit](https://streamlit.io) es una herramienta de código abierto que permite convertir scripts de Python en aplicaciones web interactivas, sin necesidad de conocimientos en HTML, CSS o JavaScript.

Es muy útil para:
- Crear dashboards de análisis de datos
- Prototipar interfaces para modelos de machine learning
- Visualizar datos y compartir resultados rápidamente

---

## 🧰 Comandos esenciales de `st.` en Streamlit

### ✍️ Texto y títulos

| Comando | Descripción |
|--------|-------------|
| `st.title("Mi app")` | Título principal |
| `st.header("Sección")` | Encabezado grande |
| `st.subheader("Subsección")` | Encabezado más pequeño |
| `st.write("Texto o variable")` | Escribe texto, listas, DataFrames, etc. |
| `st.markdown("**Negrita**")` | Permite usar sintaxis Markdown |
| `st.code("print('Hola')", language='python')` | Muestra código con formato |
| `st.latex(r"E=mc^2")` | Renderiza fórmulas matemáticas en LaTeX |

---

### 📊 Datos y gráficos

| Comando | Descripción |
|--------|-------------|
| `st.dataframe(df)` | Muestra un DataFrame interactivo |
| `st.table(df)` | Muestra una tabla estática |
| `st.metric(label, value, delta)` | Muestra un KPI numérico |
| `st.plotly_chart(fig)` | Muestra gráficos de Plotly |
| `st.pyplot(fig)` | Muestra gráficos de Matplotlib |
| `st.line_chart(df)` / `st.bar_chart(df)` | Gráficas rápidas con pandas |

---

### 🎛️ Widgets (interactividad)

| Comando | Descripción |
|--------|-------------|
| `st.button("Haz clic")` | Botón interactivo |
| `st.selectbox("Elige uno", opciones)` | Menú desplegable |
| `st.multiselect("Elige varios", opciones)` | Selección múltiple |
| `st.slider("Rango", min, max, valor)` | Deslizador numérico |
| `st.checkbox("Aceptar")` | Casilla de verificación |
| `st.radio("Selecciona", opciones)` | Botones de opción |
| `st.text_input("Nombre")` | Campo de texto |
| `st.number_input("Edad", min_value=0)` | Campo numérico |
| `st.date_input("Fecha")` | Calendario |
| `st.file_uploader("Sube un archivo")` | Subir archivos |

---

### 🧠 Control de flujo

| Comando | Descripción |
|--------|-------------|
| `if st.button("..."):` | Ejecuta acciones al hacer clic |
| `with st.expander("Ver más"):` | Muestra contenido desplegable |
| `st.stop()` | Detiene la ejecución del script |
| `st.warning("¡Cuidado!")` | Mensaje de advertencia |
| `st.error("Error")` | Mensaje de error |
| `st.success("Éxito")` | Mensaje de éxito |

---

### 🎨 Diseño y estructura

| Comando | Descripción |
|--------|-------------|
| `st.sidebar.selectbox(...)` | Widget en barra lateral |
| `st.columns(n)` | Divide la pantalla en columnas |
| `st.container()` | Agrupa elementos |
| `st.empty()` | Espacio dinámico para contenido |
| `st.set_page_config(layout="wide")` | Usa el ancho completo (ideal para dashboards) |

---

## ✅ Recomendaciones para dashboards

- Usa `st.columns()` para mostrar varias gráficas sin scroll.
- Agrega filtros con `selectbox`, `slider` o `multiselect`.
- Usa `st.set_page_config(layout="wide")` al inicio del script para aprovechar toda la pantalla.

---

🎯 ¡Listo! Con estos comandos puedes construir dashboards operativos y estratégicos interactivos con solo Python.
