# 🔮 Predicción-7

Sistema inteligente de predicción de números basado en **web scraping automático** y **Machine Learning**.

## 📋 Características

- 🕷️ **Web Scraping Automático**: Extrae números de páginas web de forma automática
- 🤖 **Predicción con IA**: Utiliza análisis estadístico y Machine Learning (Random Forest)
- 💾 **Almacenamiento Inteligente**: Base de datos SQLite para mejorar la precisión con datos históricos
- 📊 **Dashboard Analítico**: Visualización completa de estadísticas y patrones
- 🎯 **Múltiples Métodos**: Predicción estadística, ML y combinada
- 🌐 **Interfaz Web Moderna**: Diseño premium con glassmorphism y animaciones

## 🚀 Instalación

### Paso 1: Crear entorno virtual

```bash
python -m venv venv
```

### Paso 2: Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y ajusta la configuración:

```bash
copy .env.example .env
```

### Paso 5: Inicializar la base de datos

```bash
python database.py
```

## 🎮 Uso

### Iniciar el servidor

```bash
python app.py
```

El servidor estará disponible en: `http://127.0.0.1:5000`

### Configurar un Scraper

1. Ve a la sección **Scraper** en el menú
2. Ingresa la URL de la página web
3. (Opcional) Especifica un selector CSS o XPath para extraer números específicos
4. Define el intervalo de scraping
5. Click en "Agregar Configuración"

### Generar Predicciones

1. Asegúrate de tener al menos 50 números en la base de datos
2. Ve al **Dashboard**
3. Las predicciones se generan automáticamente o puedes generarlas manualmente

## 📁 Estructura del Proyecto

```
prediccion-7/
├── app.py                  # Aplicación Flask principal
├── database.py             # Modelos y configuración de BD
├── scraper.py              # Sistema de web scraping
├── predictor.py            # Motor de predicción
├── requirements.txt        # Dependencias
├── .env                    # Configuración (no incluido en git)
├── static/
│   ├── style.css          # Estilos CSS
│   └── main.js            # JavaScript
└── templates/
    ├── base.html          # Template base
    ├── index.html         # Página principal
    ├── dashboard.html     # Dashboard de análisis
    ├── scraper.html       # Configuración de scraper
    └── historial.html     # Historial de predicciones
```

## 🧠 Métodos de Predicción

### 1. Análisis Estadístico
- Frecuencia de aparición
- Análisis de patrones
- Tendencias históricas

### 2. Machine Learning
- Random Forest Classifier
- Features: últimos N números, media, desviación estándar, etc.
- Entrenamiento continuo con nuevos datos

### 3. Método Combinado (Recomendado)
- Combina ambos métodos
- Ponderación por confianza
- Mayor precisión

## 📊 API Endpoints

### Scraper
- `POST /api/scraper/agregar` - Agregar configuración de scraper
- `POST /api/scraper/ejecutar/<id>` - Ejecutar scraper manualmente

### Predicciones
- `POST /api/prediccion/generar` - Generar nueva predicción
- `GET /api/estadisticas` - Obtener estadísticas del sistema

### Datos
- `GET /api/numeros/recientes` - Obtener números recientes

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Flask
- **Scraping**: BeautifulSoup, Selenium
- **ML**: scikit-learn, pandas, numpy
- **Base de Datos**: SQLite, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualización**: matplotlib, seaborn

## 📝 Ejemplos de URLs para Scraping

### Ejemplo 1: Random.org
```
https://www.random.org/integers/?num=10&min=1&max=100&col=1&base=10&format=html&rnd=new
```

### Ejemplo 2: Con selector CSS
- URL: `https://ejemplo.com/numeros`
- Selector CSS: `.numero-resultado`

### Ejemplo 3: Con XPath (JavaScript)
- URL: `https://ejemplo.com/lottery`
- XPath: `//div[@class='ball-number']/span`

## ⚙️ Configuración Avanzada

### Ajustar precisión del modelo

En `predictor.py`, modifica:
```python
self.min_samples = 50  # Mínimo de muestras (default: 50)
```

### Cambiar intervalo de scraping

En la interfaz web o directamente en la base de datos.

### Personalizar el modelo ML

Modifica los hiperparámetros en `predictor.py`:
```python
RandomForestClassifier(
    n_estimators=100,  # Número de árboles
    max_depth=10,      # Profundidad máxima
    random_state=42
)
```

## 🔒 Seguridad

- No compartas tu archivo `.env`
- Usa HTTPS en producción
- Implementa rate limiting para APIs
- Valida todas las URLs de scraping

## 🐛 Solución de Problemas

### Error: "No module named 'selenium'"
```bash
pip install selenium
```

### Error: ChromeDriver not found
El script descarga automáticamente ChromeDriver con `webdriver-manager`.

### Error: "Se necesitan al menos X muestras"
Ejecuta el scraper varias veces para acumular más datos.

### El scraper no encuentra números
- Verifica la URL
- Prueba sin selector (extrae todos los números)
- Usa XPath si la página usa JavaScript

## 📈 Mejoras Futuras

- [ ] Programador de tareas (cron) para scraping automático
- [ ] Envío de notificaciones con predicciones
- [ ] API REST completa
- [ ] Gráficos interactivos con Chart.js
- [ ] Exportar datos a CSV/Excel
- [ ] Múltiples modelos de ML (LSTM, etc.)
- [ ] Sistema de usuarios y autenticación

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para tus propios proyectos.

## 👨‍💻 Autor

Creado con ❤️ usando Python y Flask

---

**⚠️ Disclaimer**: Este sistema es para fines educativos y de investigación. Los resultados de predicción no garantizan resultados futuros reales.
