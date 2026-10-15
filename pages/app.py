import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import io
from joblib import Parallel, delayed

# =========================================================
# IMPORTACIÓN DE LIBRERÍAS DE SKTIME Y MACHINE LEARNING
# =========================================================
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.ets import AutoETS
from sktime.forecasting.arima import AutoARIMA
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.trend import PolynomialTrendForecaster
from sktime.forecasting.compose import make_reduction

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

from sktime.performance_metrics.forecasting import mean_absolute_percentage_error, mean_squared_error, mean_absolute_error

import warnings
warnings.filterwarnings("ignore")


# link de la pagina de modelos https://www.sktime.net/models/

# =========================================================
# CONFIGURACIÓN DE LA PÁGINA (STREAMLIT)
# =========================================================
st.set_page_config(page_title="Pronóstico Avanzado de Ventas - Sktime", layout="wide", page_icon=":material/query_stats:")

st.subheader(":material/query_stats: Aplicación Avanzada: Pronóstico y Optimización de Ventas")

st.markdown(
    """
    <style>
    /* Ocultar completamente la barra lateral y su espacio reservado */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Ocultar el botón flotante de colapsar/expandir sidebar */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

MODEL_DESCRIPTIONS = {
    "Ingenuo (Naive)": "Útil como línea base (baseline). Asume que el futuro será igual al último valor observado.",
    "Tendencia Polinómica": "Modela la tendencia general (crecimiento o decrecimiento) mediante una línea matemática suave.",
    "Suavización Exponencial": "Da mayor peso a los datos recientes. Excelente para cambios graduales donde el pasado lejano importa menos.",
    "Auto ETS": "Busca automáticamente la combinación óptima de Error, Tendencia y Estacionalidad. Estándar robusto en negocios.",
    "Auto ARIMA": "Modelo estadístico basado en la autocorrelación de los datos a lo largo del tiempo.",
    "Theta": "Modelo rápido y eficiente con excelente desempeño en competencias de pronóstico financiero y de ventas.",
    "Bosques Aleatorios (ML)": "Random Forest adaptado a series temporales. Captura relaciones no lineales complejas.",
    "Gradient Boosting (ML)": "Árboles potenciados por gradiente. Altamente preciso para retail al capturar interacciones complejas.",
}

if HAS_XGB:
    MODEL_DESCRIPTIONS["XGBoost (ML)"] = "Algoritmo de vanguardia en Machine Learning tabular y de series temporales por su gran potencia predictiva."

tab1, tab2 = st.tabs([":material/model_training: Entrenar, Evaluar y Proyectar", ":material/upload_file: Cargar Modelo Guardado"])

# =========================================================
# FUNCIÓN AUXILIAR PARA ENTRENAMIENTO EN PARALELO
# =========================================================
def train_single_model(name, model, y_train, y_full, fh, horizon):
    """Entrena y evalúa un modelo de forma aislada para permitir paralelización."""
    try:
        model_eval = model.clone() if hasattr(model, 'clone') else model
        model_eval.fit(y_train)
        y_pred = model_eval.predict(fh=fh)
        
        mape = mean_absolute_percentage_error(y_test_global, y_pred) # type: ignore
        rmse = np.sqrt(mean_squared_error(y_test_global, y_pred)) # type: ignore
        mae = mean_absolute_error(y_test_global, y_pred) # type: ignore
        
        metrics = {"Modelo": name, "MAPE (%)": mape * 100, "RMSE": rmse, "MAE": mae}
        
        model_full = model.clone() if hasattr(model, 'clone') else model
        model_full.fit(y_full)
        y_future = model_full.predict(fh=fh)
        
        return name, metrics, y_future, model_full, None
    except Exception as e:
        return name, None, None, None, str(e)


with tab1:
    st.markdown("""
    **Paso 1:** Carga tu histórico de ventas, configura la frecuencia de negocio, el método de imputación de baches y selecciona los algoritmos a comparar.  
    **Paso 2:** Analiza las métricas, exporta las proyecciones en Excel y descarga el paquete del modelo ganador con metadatos.
    """)

    uploaded_file = st.file_uploader("Carga tu archivo Excel o CSV de ventas", type=['csv', 'xlsx'], key="train_file")

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            st.write("### Vista previa de los datos")
            st.dataframe(df.head(), width='stretch')
            
            st.write("### 1. Configuración de la Serie de Tiempo y Limpieza")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                date_col = st.selectbox("Columna de Fecha", df.columns, key="train_date")
            with col2:
                val_col = st.selectbox("Columna de Valor (Ventas)", df.columns, key="train_val")
            with col3:
                freq_map = {"Diaria": "D", "Semanal": "W", "Mensual (Fin de mes)": "ME", "Trimestral": "QE", "Anual": "YS"}
                freq_label = st.selectbox("Frecuencia del Negocio", list(freq_map.keys()), index=2)
                freq_code = freq_map[freq_label]
            with col4:
                sp = st.number_input(
                    "Estacionalidad (sp)", 
                    min_value=1, max_value=365, value=12,
                    help="Ciclos completos por año (Ej: 12 para mensual, 7 para diario)."
                )
                
            # MEJORA 2: Selector para el método de imputación de baches temporales
            impute_method = st.selectbox(
                "Método de Imputación de Baches Temporales",
                options=["Linear (Interpolación)", "Forward Fill (ffill - Último valor conocido)", "Ceros (0)", "Spline (Suave)"],
                index=0,
                help="Define cómo rellenar huecos si faltan periodos en tu histórico para evitar distorsionar la estacionalidad real."
            )
                
            horizon = st.number_input("Horizonte de predicción (Periodos a futuro)", min_value=1, max_value=365, value=12)
            
            st.write("### 2. Selección de Modelos")
            with st.expander(":material/menu_book: Descripción de Modelos Disponibles", expanded=False):
                for m_name, desc in MODEL_DESCRIPTIONS.items():
                    st.markdown(f"- **{m_name}:** {desc}")
                    
            selected_models_names = st.multiselect(
                "Modelos a entrenar en paralelo:",
                options=list(MODEL_DESCRIPTIONS.keys()),
                default=["Auto ETS", "Auto ARIMA", "Theta", "Gradient Boosting (ML)"]
            )
            
            if st.button(":material/play_arrow: Entrenar y Proyectar en Paralelo", type="primary"):
                if not selected_models_names:
                    st.error(":material/error: Selecciona al menos un modelo.")
                else:
                    with st.spinner("Procesando datos con parseo robusto y entrenando modelos en paralelo..."):
                        
                        df_ts = df.copy()
                        
                        # MEJORA 1: Robustez en el parseo de datos usando errors='coerce'
                        df_ts[date_col] = pd.to_datetime(df_ts[date_col], errors='coerce')
                        df_ts[val_col] = pd.to_numeric(df_ts[val_col], errors='coerce')
                        df_ts = df_ts.dropna(subset=[date_col, val_col])
                        
                        # Agrupar por fecha para evitar duplicados en el índice sumando ventas
                        df_ts = df_ts.groupby(date_col, as_index=False)[val_col].sum()
                        df_ts = df_ts.sort_values(date_col)
                        df_ts.set_index(date_col, inplace=True)
                        
                        # Reindexar a la frecuencia seleccionada
                        df_ts = df_ts.asfreq(freq_code)
                        
                        # MEJORA 2: Aplicar imputación de baches según la elección del usuario
                        if "Linear" in impute_method:
                            df_ts[val_col] = df_ts[val_col].interpolate(method='linear')
                        elif "Forward Fill" in impute_method:
                            df_ts[val_col] = df_ts[val_col].ffill().bfill()
                        elif "Ceros" in impute_method:
                            df_ts[val_col] = df_ts[val_col].fillna(0.0)
                        elif "Spline" in impute_method:
                            df_ts[val_col] = df_ts[val_col].interpolate(method='spline', order=2)
                        
                        y = df_ts[val_col]
                        
                        if len(y) <= horizon * 2:
                            st.error(f":material/error: Datos insuficientes. Tienes {len(y)} registros limpios y se recomiendan al menos {horizon * 2} para evaluar con seguridad.")
                        else:
                            y_train = y.iloc[:-horizon]
                            global y_test_global
                            y_test_global = y.iloc[-horizon:]
                            
                            available_models = {
                                "Ingenuo (Naive)": NaiveForecaster(strategy="last", sp=sp),
                                "Tendencia Polinómica": PolynomialTrendForecaster(degree=1),
                                "Suavización Exponencial": ExponentialSmoothing(sp=sp) if sp > 1 else ExponentialSmoothing(),
                                "Auto ETS": AutoETS(auto=True, sp=sp, n_jobs=-1),
                                "Auto ARIMA": AutoARIMA(sp=sp, suppress_warnings=True),
                                "Theta": ThetaForecaster(sp=sp if sp > 1 else 1),
                                "Bosques Aleatorios (Machine Learning)": make_reduction(RandomForestRegressor(n_estimators=100, random_state=42), window_length=sp if sp > 1 else 3, strategy="recursive"),
                                "Gradient Boosting (ML)": make_reduction(GradientBoostingRegressor(n_estimators=100, random_state=42), window_length=sp if sp > 1 else 3, strategy="recursive")
                            }
                            
                            if HAS_XGB:
                                available_models["XGBoost (ML)"] = make_reduction(XGBRegressor(n_estimators=100, random_state=42), window_length=sp if sp > 1 else 3, strategy="recursive")
                            
                            models_to_train = {k: available_models[k] for k in selected_models_names if k in available_models}
                            fh = np.arange(1, horizon + 1)
                            
                            parallel_results = Parallel(n_jobs=-1)(
                                delayed(train_single_model)(name, model, y_train, y, fh, horizon)
                                for name, model in models_to_train.items()
                            )
                            
                            results = []
                            projections = {}
                            trained_models = {}
                            failed_models = []
                            
                            for name, metrics, y_future, model_full, err in parallel_results:
                                if err:
                                    failed_models.append((name, err))
                                else:
                                    results.append(metrics)
                                    projections[name] = y_future
                                    trained_models[name] = model_full
                            
                            if results:
                                st.session_state['trained_models'] = trained_models
                                st.session_state['results_df'] = pd.DataFrame(results).sort_values(by="MAPE (%)")
                                st.session_state['projections'] = projections
                                st.session_state['historical_y'] = y
                                st.session_state['horizon'] = horizon
                                st.session_state['best_model_name'] = st.session_state['results_df'].iloc[0]['Modelo']
                                st.session_state['failed_models'] = failed_models
                                st.session_state['freq_code'] = freq_code
                                st.session_state['last_date'] = y.index[-1]

            if 'results_df' in st.session_state and not st.session_state['results_df'].empty:
                st.write("---")
                st.write("### :material/bar_chart: Métricas de Evaluación de Modelos")
                
                # MEJORA 3: Nota metodológica de Backtesting y Rigor Cuantitativo
                with st.expander(":material/psychology: Nota Metodológica y Rigor Cuantitativo (Backtesting)", expanded=False):
                    st.markdown("""
                    - **MAPE (%):** Error porcentual medio. ¡La aplicación selecciona al ganador basándose en el menor MAPE!
                    - **MAE / RMSE:** Errores absolutos y cuadráticos medios.
                    - **Rigor de Validación (Backtesting):** Actualmente se utiliza un corte de prueba temporal simple (*hold-out split* en la cola). En proyectos financieros corporativos de misión crítica, se recomienda complementar esto con **Backtesting de Ventana Deslizante (*Expanding/Rolling Window Cross-Validation*)** para mitigar sesgos temporales (*look-ahead bias*) ante cambios estructurales de mercado.
                    """)

                st.dataframe(st.session_state['results_df'].style.highlight_min(subset=['MAPE (%)', 'RMSE', 'MAE'], color='#c1f0c1'), width='stretch')
                
                if st.session_state.get('failed_models'):
                    with st.expander(":material/warning: Modelos que no pudieron ejecutarse", expanded=False):
                        for fm_name, fm_err in st.session_state['failed_models']:
                            st.warning(f"- **{fm_name}**: {fm_err}")

                best_model_name = st.session_state['best_model_name']
                st.success(f":material/emoji_events: **Modelo Recomendado (Ganador): {best_model_name}**")
                
                # ==========================================
                # GRÁFICO COMPARATIVO GENERAL
                # ==========================================
                st.write("### :material/show_chart: Comparativa de Proyecciones")
                fig_comp = go.Figure()
                
                y_hist = st.session_state['historical_y']
                idx_hist = y_hist.index.to_timestamp() if hasattr(y_hist.index, "to_timestamp") else y_hist.index
                
                fig_comp.add_trace(go.Scatter(x=idx_hist, y=y_hist.values, mode='lines', name='Histórico Real', line=dict(color='#1E293B', width=2)))
                
                for name, y_fut in st.session_state['projections'].items():
                    idx_fut = y_fut.index.to_timestamp() if hasattr(y_fut.index, "to_timestamp") else y_fut.index
                    fig_comp.add_trace(go.Scatter(x=idx_fut, y=y_fut.values, mode='lines', name=f'{name}'))
                    
                fig_comp.update_layout(title="Proyecciones a Futuro por Modelo", xaxis_title="Fecha", yaxis_title="Ventas", hovermode="x unified", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_comp, width='stretch')

                # ==========================================
                # DETALLE E INTERVALOS DE CONFIANZA
                # ==========================================
                st.write("---")
                st.write("### :material/manage_search: Detalle e Intervalos de Confianza")
                
                selected_detail_model = st.selectbox("Selecciona un modelo para inspeccionar a fondo:", list(st.session_state['trained_models'].keys()), index=list(st.session_state['trained_models'].keys()).index(best_model_name))
                
                model_full = st.session_state['trained_models'][selected_detail_model]
                fh_full = np.arange(1, st.session_state['horizon'] + 1)
                y_future_detail = st.session_state['projections'][selected_detail_model]
                idx_fut_detail = y_future_detail.index.to_timestamp() if hasattr(y_future_detail.index, "to_timestamp") else y_future_detail.index
                
                fig_detail = go.Figure()
                fig_detail.add_trace(go.Scatter(x=idx_hist, y=y_hist.values, mode='lines', name='Histórico Real', line=dict(color='#1E293B')))
                fig_detail.add_trace(go.Scatter(x=idx_fut_detail, y=y_future_detail.values, mode='lines', name=f'Proyección ({selected_detail_model})', line=dict(color='#2563EB', width=2)))
                
                try:
                    pred_int = model_full.predict_interval(fh=fh_full, coverage=0.95)
                    lower_col = [c for c in pred_int.columns if 'lower' in str(c).lower()][0]
                    upper_col = [c for c in pred_int.columns if 'upper' in str(c).lower()][0]
                    y_lower = pred_int[lower_col]
                    y_upper = pred_int[upper_col]
                    
                    fig_detail.add_trace(go.Scatter(
                        x=np.concatenate([idx_fut_detail, idx_fut_detail[::-1]]),
                        y=np.concatenate([y_upper.values, y_lower.values[::-1]]),
                        fill='toself',
                        fillcolor='rgba(37,99,235,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='Intervalo de Confianza (95%)'
                    ))
                except:
                    st.info(f"El modelo '{selected_detail_model}' no soporta intervalos de confianza probabilísticos nativos.")
                
                fig_detail.update_layout(title=f"Proyección con Banda del 95%: {selected_detail_model}", xaxis_title="Fecha", yaxis_title="Ventas", hovermode="x unified", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_detail, width='stretch')

                # ==========================================
                # EXPORTACIÓN DE PROYECCIONES (EXCEL) Y MODELO CON METADATOS
                # ==========================================
                st.write("### :material/download: Exportar Resultados y Paquete de Modelo")
                
                df_export = pd.DataFrame({
                    "Fecha": idx_fut_detail.strftime('%Y-%m-%d') if hasattr(idx_fut_detail, 'strftime') else idx_fut_detail,
                    "Valor_Proyectado": y_future_detail.values
                })
                
                col_exp1, col_exp2 = st.columns(2)
                
                with col_exp1:
                    buffer_excel = io.BytesIO()
                    with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
                        df_export.to_excel(writer, index=False, sheet_name='Proyeccion')
                    excel_data = buffer_excel.getvalue()
                    
                    st.download_button(
                        label=f":material/file_download: Descargar Proyección (Excel)",
                        data=excel_data,
                        file_name=f"proyeccion_{selected_detail_model.replace(' ', '_').lower()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                with col_exp2:
                    # MEJORA 4: Serialización avanzada empaquetando modelo y metadatos contextuales en un dict
                    try:
                        model_package = {
                            "model": model_full,
                            "freq_code": st.session_state.get('freq_code', 'ME'),
                            "last_date": st.session_state.get('last_date', None),
                            "model_name": selected_detail_model
                        }
                        buffer = io.BytesIO()
                        joblib.dump(model_package, buffer)
                        buffer.seek(0)
                        
                        st.download_button(
                            label=f":material/save: Descargar Paquete con Metadatos (.joblib)",
                            data=buffer.getvalue(),
                            file_name=f"paquete_modelo_{selected_detail_model.replace(' ', '_').lower()}.joblib",
                            mime="application/octet-stream",
                            key="btn_download_trained_model"
                        )
                    except Exception as e:
                        st.error(f":material/error: No se pudo empaquetar el modelo '{selected_detail_model}': {e}")
                        st.info(":material/info: Nota: Algunos algoritmos estadísticos avanzados tienen dependencias internas de C que impiden su exportación directa. Prueba seleccionando otro modelo ganador.")
        except Exception as e:
            st.error(f":material/error: Ocurrió un error en el procesamiento: {e}")

# =========================================================
# PESTAÑA 2: CARGAR MODELO GUARDADO (CON METADATOS)
# =========================================================
with tab2:
    st.markdown("""
    Carga un archivo de paquete con metadatos previamente exportado (`.joblib`) para generar nuevas proyecciones de ventas de manera inmediata y sincronizada.
    """)
    uploaded_model = st.file_uploader("Sube tu archivo de paquete de modelo (.joblib)", type=['joblib'])
    
    if uploaded_model is not None:
        try:
            loaded_data = joblib.load(uploaded_model)
            
            # Compatibilidad: verificar si es un diccionario con metadatos (Mejora 4) o un modelo crudo legacy
            if isinstance(loaded_data, dict) and "model" in loaded_data:
                loaded_model = loaded_data["model"]
                saved_freq = loaded_data.get("freq_code", "ME")
                saved_last_date = loaded_data.get("last_date", None)
                model_label = loaded_data.get("model_name", "Modelo Cargado")
                st.success(f":material/check_circle: ¡Paquete de '{model_label}' cargado exitosamente con metadatos contextuales!")
            else:
                loaded_model = loaded_data
                saved_freq = "ME"
                saved_last_date = None
                st.success(":material/check_circle: ¡Modelo legacy cargado exitosamente en memoria!")
            
            st.write("### Configuración de la Nueva Proyección")
            colA, colB, colC = st.columns(3)
            with colA:
                new_horizon = st.number_input("Horizonte a futuro", min_value=1, max_value=365, value=12, key="load_horizon")
            with colB:
                # Sugerir automáticamente el siguiente periodo basándose en la última fecha histórica guardada
                default_start = pd.to_datetime(saved_last_date) + pd.tseries.frequencies.to_offset(saved_freq) if saved_last_date else pd.to_datetime("2027-01-01")
                if pd.isna(default_start):
                    default_start = pd.to_datetime("2027-01-01")
                start_date = st.date_input("Fecha de inicio de proyección", value=default_start)
            with colC:
                freq_options = {"Diaria": "D", "Semanal": "W", "Mensual (Fin de mes)": "ME", "Trimestral": "QE", "Anual": "YS"}
                default_idx = 2
                for idx, (k, v) in enumerate(freq_options.items()):
                    if v == saved_freq:
                        default_idx = idx
                        break
                freq_selection = st.selectbox("Frecuencia del Periodo", list(freq_options.keys()), index=default_idx)
                freq_code = freq_options[freq_selection]
            
            if st.button(":material/play_arrow: Generar Proyección con Modelo Cargado", type="primary"):
                fh = np.arange(1, new_horizon + 1)
                y_pred_new = loaded_model.predict(fh=fh)
                
                future_dates = pd.date_range(start=start_date, periods=new_horizon, freq=freq_code)
                y_pred_new.index = future_dates
                
                fig2 = go.Figure()
                idx_new = y_pred_new.index
                fig2.add_trace(go.Scatter(x=idx_new, y=y_pred_new.values, mode='lines+markers', name='Proyección Futura', line=dict(color='#2563EB', width=2)))
                
                try:
                    pred_int = loaded_model.predict_interval(fh=fh, coverage=0.95)
                    pred_int.index = future_dates
                    lower_col = [c for c in pred_int.columns if 'lower' in str(c).lower()][0]
                    upper_col = [c for c in pred_int.columns if 'upper' in str(c).lower()][0]
                    y_lower = pred_int[lower_col]
                    y_upper = pred_int[upper_col]
                    
                    fig2.add_trace(go.Scatter(
                        x=np.concatenate([idx_new, idx_new[::-1]]),
                        y=np.concatenate([y_upper.values, y_lower.values[::-1]]),
                        fill='toself',
                        fillcolor='rgba(37,99,235,0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='Intervalo de Confianza (95%)'
                    ))
                except:
                    pass

                fig2.update_layout(title="Proyección Comercial del Modelo Cargado", xaxis_title="Fecha", yaxis_title="Ventas", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, width='stretch')
                
                df_results = pd.DataFrame({"Fecha": idx_new.strftime('%Y-%m-%d'), "Ventas Proyectadas": y_pred_new.values})
                st.dataframe(df_results, hide_index=True, width='stretch')
                
                buffer_excel_loaded = io.BytesIO()
                with pd.ExcelWriter(buffer_excel_loaded, engine='openpyxl') as writer:
                    df_results.to_excel(writer, index=False, sheet_name='Proyeccion_Cargada')
                excel_loaded_data = buffer_excel_loaded.getvalue()

                st.download_button(
                    label=":material/file_download: Descargar esta Proyección en Excel",
                    data=excel_loaded_data,
                    file_name="proyeccion_modelo_cargado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
        except Exception as e:
            st.error(f":material/error: Error al cargar o procesar el modelo: {e}")