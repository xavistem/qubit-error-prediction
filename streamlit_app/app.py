import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd
import pydeck as pdk
import altair as alt
import numpy as np
import datetime
import zipfile
import base64
import time
import io
import os

# Para ejecutar, primero en la terminal: pip install -r requirements.txt
# Después: streamlit run app.py

# Configuración de la Página
st.set_page_config(
    layout="wide",       
    initial_sidebar_state="expanded",
    page_title="Qubit Error Prediction", # Escribe el título de la web, ahora por defecto saldría una X
    page_icon="📈", # Escribe el icono que quieres que salga, ahora mismo por defecto saldría este icono: 📈      
)

# CONTENIDO DE LA SIDEBAR
with st.sidebar:
    # 1. Logo (en style='width y height' se puede ajustar), cambiar el logo de la carpeta de assets y que tenga el título de logo
    # Es mejor usar el logo con el fondo transparente
    logo_path = "assets/logo.png"
    try:
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 40px;">
                <img src="data:image/png;base64,{encoded_logo}" alt="Vanguard Logo" style="width: 140px; height: 140px;">
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 40px;
                        width: 70px; height: 70px; background-color: #DDD; border-radius: 10px;
                        align-items: center; font-size: 28px; color: #555; font-weight: bold;">
                L
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
    """
    <style>
        /* Aplica el fondo, ancho y quita scroll */
        section[data-testid="stSidebar"] {
            background-color: #e7f5ff;
            width: 180px;
            overflow: hidden !important;
        }

        /* Fuerza que el contenido interno tampoco tenga scroll */
        section[data-testid="stSidebar"] > div:first-child {
            overflow: hidden !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

# Reemplaza el apartado anterior por este si quieres que haya un scroll vertical en la side bar:
# Copia y pega desde st.markdown hasta el paréntesis de cierre y quitale los comentarios
# st.markdown(
#     """
#     <style>
#         section[data-testid="stSidebar"] {
#             background-color: #e7f5ff;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

    # 2. Menú de Opciones
    option_titles_en = [
        "Overview",
        "Interactive Analysis",
        "Statistics",
        "ML/DP",
        "Conclusions",
        "Downloads & Resources",
        "Load & Quick EDA",
        "Settings"
    ]
    
    icons_list = [
        "house-door-fill",
        "bar-chart-line-fill",
        "percent",
        "cpu-fill",
        "clipboard-data-fill",
        "download",
        "folder-fill",
        "gear-fill"
    ]

    selected_title_en = option_menu(
        menu_title=None,
        options=option_titles_en,
        icons=icons_list,
        menu_icon="list", 
        default_index=0,
        orientation="vertical",
        styles={
            "container": { 
                           
                "padding": "5px !important",
                "background-color": "#e7f5ff", # Hacemos que coincida con el fondo de st.sidebar
            },
            "icon": {
                "color": "#0d6efd", 
                "font-size": "24px",
            },
            "nav-link": {
                "font-size": "0px",
                "text-align": "center",
                "margin": "8px 0px",
                "--hover-color": "rgba(13, 110, 253, 0.1)", # Hover sutil sobre el fondo azul claro
                "height": "55px",
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "border-radius": "5px",
            },
            "nav-link span": {
                "display": "none !important"
            },
            "nav-link-selected": {
                "background-color": "rgba(13, 110, 253, 0.15)", # Fondo ligeramente más oscuro para seleccionado
            },
             "nav-link-selected .icon": { 
                "color": "#0a58ca !important", # Icono un poco más oscuro en selección
            }
        }
    )

# CONTENIDO PRINCIPAL DE LA PÁGINA
if 'current_page_key' not in st.session_state:
    st.session_state.current_page_key = selected_title_en

if selected_title_en != st.session_state.current_page_key:
    st.session_state.current_page_key = selected_title_en


if st.session_state.current_page_key == "Overview":
    # Título fijo arriba
    st.title("Overview")

    # Inicializamos el slide actual y lo ponemos en la primera slide (0) por defecto
    if "ov_page" not in st.session_state:
        st.session_state.ov_page = 0

    # Botones de navegación
    nav_col1, _, nav_col3 = st.columns([1, 6, 1])
    with nav_col1:
        if st.button("←", disabled=(st.session_state.ov_page == 0)):
            st.session_state.ov_page -= 1
    with nav_col3:
        if st.button("→", disabled=(st.session_state.ov_page == 2)):
            st.session_state.ov_page += 1

    # SLIDE 0: Who Are We?
    if st.session_state.ov_page == 0:
        st.markdown("### ¿IBM?")
        st.markdown("""
- **Fundación y evolución**:  
  IBM se fundó en 1911 como una empresa de máquinas tabuladoras y ha evolucionado hasta convertirse en líder en tecnología y servicios de nube.

- **Enfoque actual en computación cuántica**:  
  Hoy, IBM lidera la investigación en computación cuántica, ofreciendo plataformas como IBM Quantum Experience para acceso a procesadores reales y simuladores.

- **Sherbrooke**:  
  Sherbrooke es una ciudad en Québec (Canadá) conocida por sus universidades y centros de investigación. Aquí se ubica nuestro estudio de calibración de qubits.
""")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("assets/image2.png", caption="Quantum Computer", width=375)

        st.subheader("¿Sheerbrooke?")
        df = pd.DataFrame([
            {"city": "Sherbrooke", "lat": 45.4001, "lon": -71.8991}
        ])

        # Usamos un ScatterplotLayer con puntas rojas tipo chincheta
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_fill_color=[255, 0, 0, 200],  # rojo
            get_radius=20000
        )

        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=45.0,
                longitude=-100.0,
                zoom=3,
                pitch=0
            ),
            layers=[layer]
        )
        st.pydeck_chart(deck, use_container_width=True)

    # SLIDE 1: Data Sources & Timeline
    elif st.session_state.ov_page == 1:
        st.subheader("📑 Data Sources & Project Timeline")
        left, right = st.columns(2)
        with left:  # Modificar el apartado siguiente, con los df utilizados en tu proyecto
            st.markdown("""
**Data Sources Used**  
- `df_sherbrooke`  
- `Others df`  
""")
        with right:  # Modificar este apartado poniendo un calendario solo y marcando el inicio y el final
            st.markdown("**Project Active Dates**")
            col_a, col_b = st.columns(2)
            with col_a:
                # Phase 1
                st.date_input(
                    "Phase 1: May 19–23, 2025",
                    value=(datetime.date(2025, 6, 2), datetime.date(2025, 6, 6)),
                    min_value=datetime.date(2025, 6, 1),
                    max_value=datetime.date(2025, 6, 30),
                    key="phase1",
                    label_visibility="collapsed"
                )

    # SLIDE 2: Texto e imagen
    else:
        left_col, right_col = st.columns([2, 1])
        with left_col:
            st.markdown("""
### 🎯 Objetivo del proyecto
 
Nuestro objetivo: **predecir el error de lectura (readout assignment error) de cada qubit**, usando datos de calibración históricos y métodos de Machine Learning.

**¿Qué hicimos?**  
- Recopilamos y limpiamos datos de calibración de qubits de Sherbrooke (T1, T2, frecuencia, anharmonicidad, fechas, etc.).  
- Creamos nuevas variables: transformaciones de T1/T2, interacciones polinomiales, e indicadores de tiempo y qubit.  
- Probamos varias técnicas de regresión (KNN, regresiones lineales, árboles, ensambles) y afinamos el mejor modelo con XGBoost.  
- Complementamos con un ensamble (stacking) que combina XGBoost y RandomForest para mejorar la precisión.

**📊 Métricas Clave**  
- MAE final: 0.0106  
- R² final: 0.8120  

**🎯 Criterio de Éxito**  
> Lograr un R² ≥ 0.70 en la predicción del error de lectura de qubits.

---

👉 Únete a este análisis para descubrir cómo optimizar calibraciones y mejorar la fidelidad en computación cuántica.
            """)
        with right_col:
            st.image("assets/image1.png", use_container_width=True)


elif st.session_state.current_page_key == "Interactive Analysis":
    st.title("Interactive Analysis")

    # Pestañas principales: Statistics and Outliers vs Graphics
    stats_tab, graphs_tab = st.tabs(["Statistics and Outliers", "Graphics"])

    # 1️⃣ Statistics and Outliers: mostramos la tabla CSV centrada
    with stats_tab:
        st.subheader("Statistics and Outliers")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            df_csv = pd.read_csv("assets/image3.csv")
            st.dataframe(df_csv)
            # Leyenda centrada debajo de la tabla
            st.markdown(
                """
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-top: 15px;
                ">
                    <div style="
                        background-color: #f0f2f6;
                        padding: 10px 20px;
                        border-radius: 8px;
                        text-align: left;
                        font-family: monospace;
                        line-height: 1.6;
                        box-shadow: 0 0 5px rgba(0,0,0,0.1);
                    ">
                        <strong>Filas</strong><br>
                        0:  count<br>
                        1:  mean<br>
                        2:  std<br>
                        3:  min<br>
                        4:  25%<br>
                        5:  50%<br>
                        6:  75%<br>
                        7:  max
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # 2️⃣ Graphics: sub-pestañas para cada una de las tres visualizaciones
    with graphs_tab:
        st.subheader("Graphics")
        graph_subtabs = graphs_tab.tabs([
            "Boxplot/Histogram",
            "Normalization vs Standardization",
            "Correlation Heatmap"
        ])

        # Boxplot/Histogram
        with graph_subtabs[0]:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("assets/image4.png", width=700)

        # Normalization vs Standardization
        with graph_subtabs[1]:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("assets/image5.png", width=700)

        # Correlation Heatmap
        with graph_subtabs[2]:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("assets/image6.png", width=700)

            st.markdown("#### Data Table for Correlation Heatmap")
            df_corr = pd.read_csv("assets/image7.csv")
            st.dataframe(df_corr)
            # Leyenda centrada debajo de la tabla
            st.markdown(
                """
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-top: 15px;
                ">
                    <div style="
                        background-color: #f0f2f6;
                        padding: 10px 20px;
                        border-radius: 8px;
                        text-align: left;
                        font-family: monospace;
                        line-height: 1.6;
                        box-shadow: 0 0 5px rgba(0,0,0,0.1);
                    ">
                        <strong>Filas</strong><br>
                        0:  T1 (us)<br>
                        1:  T2 (us)<br>
                        2:  Frequency (GHz)<br>
                        3:  Anharmonicity (GHz)<br>
                        4:  Readout length (ns)<br>
                        5:  Readout assignment error<br>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


elif st.session_state.current_page_key == "Statistics":
    st.title("Statistics")

elif st.session_state.current_page_key == "ML/DP":  # Si solo hay ML, quitar DP
    st.title("ML / Deep Learning")

    # Tabs principales
    model_tab, final_tab = st.tabs(["All Tested Models", "Final Results"])

    # 1️⃣ Tab de modelos probados
    with model_tab:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            df_models = pd.read_csv("assets/image8.csv")
            st.dataframe(df_models)

    # 2️⃣ Tab de resultado final
    with final_tab:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown("""
            <div style="background-color:#f9f9f9;padding:25px;border-radius:15px;border:1px solid #ccc;text-align:center">
                <h3 style="color:#333;">Fitting 3 folds for each of 8 candidates,<br>totalling 24 fits</h3>
                <p style="font-size:18px;margin-top:15px;">
                <strong>Mejores parámetros:</strong><br>
                {'subsample': 0.7, 'reg_lambda': 1, 'reg_alpha': 0.01, 'n_estimators': 400,<br>
                'max_depth': 5, 'learning_rate': 0.03, 'gamma': 0, 'colsample_bytree': 0.7}
                </p>
                <p style="font-size:18px;">
                <strong>Validación cruzada:</strong><br>
                R² = <span style="color:#008000;"><strong>0.7625</strong></span>
                </p>
                <p style="font-size:18px;">
                <strong>Resultados en test:</strong><br>
                MAE = <strong>0.0117</strong> &nbsp;&nbsp;|&nbsp;&nbsp; R² = <strong>0.7919</strong>
                </p>
                <p style="font-size:18px;">
                <strong>Stacking XGBoost + RandomForest:</strong><br>
                MAE = <strong>0.0106</strong> &nbsp;&nbsp;|&nbsp;&nbsp; R² = <strong>0.8120</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)


elif st.session_state.current_page_key == "Conclusions":
    st.title("🔍 Conclusions")

    with st.expander("Show Summary of Findings", expanded=False):
        st.markdown("""
### 🧠 Contexto General

Este proyecto tuvo como objetivo predecir el **error de lectura de un qubit**, es decir, la probabilidad de que al medirlo devuelva un valor incorrecto. Aunque el problema puede parecer técnico, lo abordamos paso a paso combinando modelos clásicos y avanzados de Machine Learning.

---

### ✅ Avances Clave del Modelo Final

- Se pasó de explicar solo un **56 % del comportamiento real** (modelo inicial) a **superar el 81 %** con modelos avanzados.
- El mejor modelo combinado (XGBoost + RandomForest) logró un error medio (MAE) muy bajo: **0.0106**.
- Se incorporó información temporal (fecha) y específica de cada qubit, lo que **mejoró mucho la precisión**.
- Se aplicaron técnicas de ajuste inteligente de parámetros para sacar el máximo provecho del modelo.

---

### ⚠️ Limitaciones Actuales

- El modelo **aún no llega al 100 %** de precisión: sigue habiendo un ~19 % de variabilidad no explicada.
- Los datos podrían tener **ruido o inconsistencias** en algunas calibraciones antiguas.
- Solo se usaron ciertos parámetros físicos; hay otros (temperatura, entorno, etc.) que no se incluyeron y podrían ser relevantes.

---

### 🧪 Posibles Mejoras Futuras

- **Agregar más variables físicas** o del entorno del experimento (temperatura, tipo de hardware, etc.).
- Incluir **más datos históricos**, para capturar patrones a largo plazo.
- Probar modelos de series temporales o redes neuronales recurrentes (RNNs), si hay suficiente secuencia de datos.
- Implementar validación continua del modelo para adaptarse a cambios futuros en el sistema cuántico.

---

### 🧭 Recomendación Final

> - El modelo actual es **robusto y útil para predecir el error de lectura** en condiciones similares a las del conjunto de entrenamiento.  
> - Se puede utilizar como **herramienta de diagnóstico y monitoreo** para detectar qubits que empiezan a degradarse.  
> - Recomendamos **seguir actualizando el modelo regularmente** y explorar nuevas fuentes de información.

Con este enfoque progresivo, el sistema pasó de un análisis básico a un **modelo predictivo sólido**, listo para incorporarse en aplicaciones reales de computación cuántica.
        """)


elif st.session_state.current_page_key == "Downloads & Resources": 

# Este apartado es para quien no haya asistido o quiera más información, se pueda descargar un resumen y todos los datos limpios y procesados
# En este caso, el código está preparado para descargar lo que hay a modo de ejemplo dentro de la carpeta de data, la subcarpeta de reports (hay 2 pdfs) y las subcarpetas de raw y processed (con df a modo de ejemplo)
# Hay que ir las subcarpetas de reports, processed y raw, cambiar esos archivos por los nuevos (en los reports manenter el mismo nombre, en los de data processed/raw adatpar el código al nuevo nombre)
# Ahora mismo hay dos pdf, 3 archivos en processed y 4 en raw, son de otro proyecto a modo de ejemplo, pero habría que reemplzarlo todo

    st.title("📂 Downloads & Resources")

    # 1️⃣ Executive Summary Reports
    st.markdown("### 📄 Executive Summary Reports")
    st.markdown(
        """
        For those who couldn't attend the live presentation—or anyone who wants a quick, formal
        overview—please select your preferred language and download the concise executive summary.
        """
    )

    # Language selector
    lang = st.selectbox("Choose report language", ["English", "Español"])

    # Base path para los reports
    report_base = os.path.join("data", "reports")

    if lang == "English":
        report_path = os.path.join(report_base, "Executive_Summary_EN.pdf")
        with open(report_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download Executive Summary (English)",
            data=pdf_bytes,
            file_name="Vanguard_Digital_Redesign_Summary_EN.pdf",
            mime="application/pdf",
        )
    else:
        report_path = os.path.join(report_base, "Executive_Summary_ES.pdf")
        with open(report_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Descargar Resumen Ejecutivo (Español)",
            data=pdf_bytes,
            file_name="Vanguard_Digital_Redesign_Resumen_ES.pdf",
            mime="application/pdf",
        )

    st.markdown("---")

    # 2️⃣ Data Downloads
    st.markdown("### 🗄️ Data Downloads")
    st.markdown(
        """
        You can download the raw and processed datasets used in our analysis.  
        - **Raw**: Original exported tables, before any cleaning.  
        - **Processed**: Final cleaned and joined tables ready for analysis.
        """
    )

    # Helper para comprimir cualquier carpeta en memoria
    def zip_folder_to_bytes(folder_path):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    z.write(file_path, arcname=arcname)
        buffer.seek(0)
        return buffer.read()

    # Raw data
    raw_zip = zip_folder_to_bytes(os.path.join("data", "raw"))
    st.download_button(
        label="📥 Download Raw Data (ZIP)",
        data=raw_zip,
        file_name="vanguard_raw_data.zip",
        mime="application/zip",
    )

    # Processed data
    processed_zip = zip_folder_to_bytes(os.path.join("data", "processed"))
    st.download_button(
        label="📥 Download Processed Data (ZIP)",
        data=processed_zip,
        file_name="vanguard_processed_data.zip",
        mime="application/zip",
    )

    st.markdown( # Cambiar este apartado y poner, si se quiere, el nombre de la nueva empresa en vez del nombre que viene por defecto que es X
        """
        ---
        *These datasets are provided under internal IBM use, please do not redistribute.*
        """
    )


elif st.session_state.current_page_key == "Load & Quick EDA":
    st.title("Load & Quick EDA")


elif st.session_state.current_page_key == "Settings":
    st.title("Settings")


else:
    st.write("Welcome to Vanguard Analytics. Please select an option.")
