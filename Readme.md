---------------------English version ---------------------------

# link de la pagina de modelos https://www.sktime.net/models/

Quant Time-Series Engine: — Quantitative Forecasting & Analytics Platform📊 Executive OverviewQuant Time-Series Engine is a high-performance quantitative analytics and sales forecasting web application built for financial analysts, data scientists, and enterprise planners. Designed to mitigate structural market volatility and temporal uncertainty, this engine bridges classical statistical forecasting with state-of-the-art Machine Learning models.The platform features an immersive cinematic landing cinematic experience (Star Wars: Duel Ingress) leading into a robust, multi-threaded analytics dashboard capable of handling rigorous time-series preprocessing, parallelized model training, backtesting evaluation, probabilistic confidence intervals, and metadata-aware model serialization.

Project Architecture & Directory Structurequant-timeseries-engine/
│
├── .streamlit/                   # Streamlit UI/UX and runtime configurations
│   └── config.toml                  
├── data/                         # Secure repository for historical financial datasets
│   └── db-data.xlsx  
├── icons/                        # UI assets, custom icons, and media elements
├── modelos entrenados/           # Serialized model packages (.joblib) with embedded metadata
├── pages/                        # Core multi-page application modules
│   └── app.py   
├── main.py                       # Cinematic landing interface (Star Wars crawl & telemetry sync)
├── requirements.txt              # Core dependency manifest
├── README.md                     # Project technical specification and documentation
└── LICENSE                       # Open-source licensing agreement

Core Features & Quantitative Modules1. Cinematic Entry & Telemetry Gateway (main.py)Immersive Design: Implements a custom CSS Star Wars crawl animation, dark-mode styling (#050505), typography tuning (Courier New, Century Gothic), and an embedded responsive loop video.State Transition: Directs user sessions smoothly from the tactical gateway into the core quantitative engine (pages/app.py).2. Advanced Preprocessing & Temporal Imputation (pages/app.py)Robust Parsing: Automated error-coerced parsing for dates and numeric values, aggregating duplicate timestamps via summation to ensure strict chronological integrity.Gap Imputation: Offers granular strategies for handling missing business periods or temporal baches:Linear InterpolationForward Fill (ffill)Zero Imputation (0.0)Spline Smoothing (Order 2)Frequency Mapping: Native support for Daily (D), Weekly (W), Monthly End (ME), Quarterly End (QE), and Annual (YS) business frequencies.3. Dual Statistical & Machine Learning Model ZooThe platform benchmarks multiple algorithms concurrently via parallel processing (joblib.Parallel):Classical & Statistical Models:Naive Baseline: Assumes persistence of the last observed value (sp-aware).Polynomial Trend Forecaster: Captures macroscopic deterministic growth/decay paths.Exponential Smoothing & Auto ETS: Adapts dynamically to error, trend, and seasonality components.Auto ARIMA: Statistically rigorous autoregressive integrated moving average modeling.Theta Forecaster: Proven high performance in corporate sales and financial time-series benchmarking.Machine Learning Reduction Models (sktime.forecasting.compose.make_reduction):Random Forest Regressor: Non-linear feature interaction capture.Gradient Boosting Regressor: High-accuracy ensemble trees optimized for retail and financial volatility.XGBoost Regressor: Cutting-edge gradient boosting architecture for tabular temporal structures.4. Rigorous Evaluation Metrics & BacktestingPerformance Criteria: Evaluates models out-of-sample using MAPE (%) (Primary KPI for leaderboard ranking), RMSE (Root Mean Squared Error), and MAE (Mean Absolute Error).Quantitative Rigor Note: Incorporates hold-out split evaluation with extensible design for Rolling/Expanding Window Cross-Validation to eliminate look-ahead bias in high-stakes financial environments.5. Probabilistic Forecasting & SerializationConfidence Intervals: Generates 95% predictive probability bands ($\alpha = 0.05$) to quantify volatility risk and downside/upside exposure.Metadata-Aware Serialization (.joblib): Exports trained model bundles containing the core estimator alongside vital context metadata (freq_code, last_date, model_name), enabling seamless re-hydration and future projection scoring in Tab 2.🛠️ Technology StackLanguage: Python 3.9+Framework: Streamlit (Reactive Web UI)Time-Series Framework: sktime, statsmodelsMachine Learning: scikit-learn, xgboostData Manipulation & Compute: pandas, numpy, joblibVisualization: Plotly (Interactive charting, hover toolkits, confidence bounds)Spreadsheet Integration: openpyxl

Installation & SetupClone the Repository:git clone (https://github.com/wgekko/quant-time-series-engine.git)
cd quant-timeseries-engine

Create and Activate a Virtual Environment:python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies:pip install -r requirements.txt
Run the Application:streamlit run main.py

Usage WorkflowLaunch the application and click "Sincronizarte con la Fuerza" from the cinematic landing interface.Tab 1 (Train, Evaluate & Project):Upload your historical dataset (.csv or .xlsx).Configure date columns, sales value columns, business frequency, and gap imputation methods.Select your model zoo and execute parallel training.Analyze evaluation metrics, inspect confidence intervals, download Excel projections, or save the metadata-infused model package (.joblib).Tab 2 (Load Saved Model):Upload a previously exported .joblib package.Define your new forecasting horizon and start date to generate instant production-ready forward projections. 

LicenseDistributed under the MIT License. See LICENSE for more information.

#---------------Versión en Español ---------------------

# link de la pagina de modelos https://www.sktime.net/models/

Quant Time-Series Engine — Plataforma de Analítica Cuantitativa y Pronóstico de Series Temporales
Resumen EjecutivoQuant Time-Series Engine es una aplicación web de alto rendimiento orientada a la analítica cuantitativa y la proyección de ventas, diseñada para analistas financieros, científicos de datos y planificadores corporativos. Desarrollada para mitigar la volatilidad de mercado y la incertidumbre temporal, esta plataforma integra modelos estadísticos clásicos con algoritmos avanzados de Machine Learning.El sistema cuenta con una interfaz cinematográfica de bienvenida (Star Wars: Duel Ingress) que da paso a un panel analítico multihilo. Soporta preprocesamiento riguroso de series de tiempo, entrenamiento en paralelo, evaluación con métricas de backtesting, cálculo de intervalos de confianza probabilísticos y serialización de modelos con metadatos contextuales.
Arquitectura del Proyecto y Estructura de Directoriosquant-timeseries-engine/
│
├── .streamlit/                   # Configuración del entorno de ejecución e interfaz de Streamlit
│   └── config.toml                  
├── data/                         # Repositorio seguro de datasets históricos financieros
│   └── db-data.xlsx  
├── icons/                        # Recursos visuales, íconos y elementos multimedia
├── modelos entrenados/           # Paquetes de modelos serializados (.joblib) con metadatos
├── pages/                        # Módulos analíticos de la aplicación
│   └── app.py   
├── main.py                       # Interfaz cinematográfica de acceso y sincronización
├── requirements.txt              # Manifiesto de dependencias del proyecto
├── README.md                     # Documentación técnica y especificaciones del proyecto
└── LICENSE                       # Licencia de software libre / comercial

Módulos Cuantitativos y Funcionalidades Clave1. Portal Cinematográfico y Gateway de Telemetría (main.py)Diseño Inmersivo: Implementación de animación CSS personalizada (Star Wars crawl), tema oscuro (#050505), tipografía estilizada (Courier New, Century Gothic) y reproducción de video en bucle.Transición de Estado: Flujo directo y seguro desde la portada hacia el motor analítico cuantitativo (pages/app.py).2. Preprocesamiento Avanzado e Imputación Temporal (pages/app.py)Parseo Robusto: Conversión e inspección de datos con coerción de errores (coerce), agrupando registros duplicados mediante suma para mantener la integridad cronológica.Estrategias de Imputación: Tratamiento personalizable de baches o lagunas temporales en las series:Interpolación LinealForward Fill (ffill - último valor conocido)Imputación por Ceros (0.0)Suavizado por Spline (Segundo Orden)Frecuencia Operativa: Soporte nativo para frecuencias Diaria (D), Semanal (W), Mensual a fin de mes (ME), Trimestral (QE) y Anual (YS).3. Zoo de Modelos: Estadística Clásica y Machine LearningComparación concurrente de modelos mediante procesamiento en paralelo (joblib.Parallel):Modelos Estadísticos Clásicos:Ingenuo (Naive): Línea base basada en la persistencia del último valor observando la estacionalidad (sp).Tendencia Polinómica: Captura trayectorias macroscópicas deterministas de crecimiento o decrecimiento.Suavización Exponencial y Auto ETS: Adaptación dinámica ante componentes de error, tendencia y estacionalidad.Auto ARIMA: Modelado estadístico autorregresivo integrado de media móvil.Theta Forecaster: Algoritmo de alto rendimiento en competencias internacionales de pronóstico financiero.Modelos de Machine Learning por Reducción (sktime.forecasting.compose.make_reduction):Random Forest Regressor: Captura de interacciones complejas no lineales.Gradient Boosting Regressor: Ensamble de árboles de alta precisión optimizado para entornos de alta volatilidad.XGBoost Regressor: Algoritmo de ensamble por gradiente de última generación para series temporales tabulares.4. Evaluación de Métricas y Rigor CuantitativoCriterios de Desempeño: Evaluación fuera de muestra (out-of-sample) utilizando MAPE (%) (KPI principal de selección), RMSE (Error Cuadrático Medio) y MAE (Error Absoluto Medio).Validación Cruzada: Metodología basada en división temporal (hold-out split), extensible a esquemas de Backtesting de Ventana Deslizante / Expansiva para prevenir el sesgo de anticipación (look-ahead bias).5. Proyecciones Probabilísticas y Serialización de ModelosIntervalos de Confianza: Generación de bandas de predicción probabilística al 95% ($\alpha = 0.05$) para medir el riesgo de cola y la exposición a la volatilidad.Empaquetado de Modelos (.joblib): Exportación del modelo entrenado integrado con sus metadatos contextuales (freq_code, last_date, model_name), permitiendo su recarga inmediata para proyecciones futuras en la Pestaña 2.🛠️ Stack TecnológicoLenguaje: Python 3.9+Framework Web: StreamlitModelado de Series Temporales: sktime, statsmodelsMachine Learning: scikit-learn, xgboostProcesamiento de Datos y Cómputo: pandas, numpy, joblibVisualización Interactiva: PlotlyExportación de Reportes: openpyxl

Instalación y ConfiguraciónClonar el repositorio:git clone https://github.com/wgekko/quant-time-series-engine.git
cd quant-timeseries-engine

Crear y activar un entorno virtual:python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
Instalar dependencias:pip install -r requirements.txt
Ejecutar la aplicación:streamlit run main.py

Flujo de Trabajo (Uso)Inicie la aplicación y presione el botón "Presiona el botón para sincronizarte con la Fuerza" en la pantalla de bienvenida.Pestaña 1 (Entrenar, Evaluar y Proyectar):Cargue su archivo histórico (.csv o .xlsx).Seleccione las columnas de fecha, valor de ventas, frecuencia de negocio y método de imputación.Elija los modelos a comparar y ejecute el entrenamiento en paralelo.Analice los resultados en la tabla de métricas, inspeccione las bandas de confianza, descargue las proyecciones en Excel o guarde el paquete del modelo ganador (.joblib).Pestaña 2 (Cargar Modelo Guardado):Suba un archivo .joblib generado previamente.Defina el nuevo horizonte de proyección y la fecha de inicio para obtener predicciones inmediatas.


LicenciaEste proyecto está bajo la Licencia MIT. Consúltese el archivo LICENSE para más detalles.


## 🎨 Personalización de Estilos (`.streamlit/config.toml`)

Para aplicar el tema visual profesional en modo oscuro, crea el archivo `.streamlit/config.toml`:

```toml
[theme]
# Define el tema base como oscuro
base = "dark"

# Color primario (Azul corporativo profesional para botones y elementos activos)
primaryColor = "#2563eb"

# Fondo principal de la aplicación (Tono pizarra oscuro y suave)
backgroundColor = "#0b0f19"

# Fondo secundario para contenedores, tarjetas, selectbox y barras laterales
secondaryBackgroundColor = "#111827"

# Color de las letras y textos para máxima nitidez y lectura cómoda
textColor = "#f8fafc"

# Tipo de fuente limpia y moderna
font = "sans serif"

[client]
showSidebarNavigation = false
```



video demo

