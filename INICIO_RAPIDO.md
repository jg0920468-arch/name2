# 🚀 Guía de Inicio Rápido - Predicción-7

Esta es una guía rápida para poner en marcha el sistema en menos de 5 minutos.

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Crear Entorno Virtual
```bash
cd c:\Users\USER\Documents\VsCode\prediccion-7
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Inicializar el Proyecto
```bash
python init.py
```
> Cuando te pregunte si quieres datos de ejemplo, escribe `s` y presiona Enter

### 4️⃣ Iniciar el Servidor
```bash
python app.py
```

### 5️⃣ Abrir en el Navegador
Abre tu navegador y ve a: `http://127.0.0.1:5000`

## 🎯 Primeros Pasos

### Configurar tu primer Scraper

1. Click en **"Scraper"** en el menú superior
2. Completa el formulario:
   - **URL**: `https://www.random.org/integers/?num=10&min=1&max=100&col=1&base=10&format=html&rnd=new`
   - Deja los selectores vacíos (extraerá todos los números)
   - **Intervalo**: 60 minutos
3. Click en **"Agregar Configuración"**
4. Click en **"Ejecutar Ahora"** para probar

### Ver tus Predicciones

1. Ejecuta el scraper varias veces para acumular datos
2. Ve al **Dashboard**
3. Verás estadísticas y predicciones automáticas

## 🧪 Probar con Ejemplos

También puedes ejecutar el script de ejemplos:

```bash
python ejemplos.py
```

Selecciona la opción **3** para un pipeline completo automático.

## 📊 URLs de Ejemplo para Scraping

### Random.org (Recomendado para pruebas)
```
https://www.random.org/integers/?num=10&min=1&max=100&col=1&base=10&format=html&rnd=new
```

### Con Selector CSS (ejemplo genérico)
- **URL**: Tu página web
- **Selector CSS**: `.numero, .result, #number`

## ❓ Problemas Comunes

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Se necesitan al menos 50 muestras"
Ejecuta el scraper más veces o usa el script de ejemplos (opción 3).

### El servidor no inicia
- Verifica que el puerto 5000 esté libre
- Cierra otros procesos de Python

## 📚 Recursos

- **Tutorial Completo**: README.md
- **Ejemplos**: ejemplos.py
- **Documentación**: Revisa los comentarios en cada archivo .py

## 🎉 ¡Listo!

Ya tienes todo funcionando. Ahora puedes:
- ✅ Configurar scrapers personalizados
- ✅ Acumular datos históricos
- ✅ Generar predicciones inteligentes
- ✅ Analizar patrones y estadísticas

---

**💡 Tip**: Mientras más datos acumules, más precisas serán las predicciones.
