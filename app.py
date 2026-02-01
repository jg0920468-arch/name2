"""
Aplicación web Flask para el sistema de predicción
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import init_db, get_session, NumeroExtraido, Prediccion, ConfiguracionScraper
from scraper import WebScraper, ejecutar_scraping_automatico
from predictor import PredictorNumeros
from datetime import datetime, timedelta
import json
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave-secreta-desarrollo')

# Inicializar base de datos
init_db()

# Configurar logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar Scheduler (opcionalmente integrado para ahorrar recursos en el servidor)
if os.getenv('RUN_SCHEDULER', 'False').lower() == 'true':
    scheduler = BackgroundScheduler()
    @scheduler.scheduled_job('interval', minutes=int(os.getenv('SCRAPER_INTERVAL', 30)))
    def timed_job():
        logger.info("🚀 Ejecutando scraping programado desde el proceso web")
        try:
            ejecutar_scraping_automatico()
            logger.info("✅ Scraping programado completado")
        except Exception as e:
            logger.error(f"❌ Error en scraping programado: {e}")
    
    scheduler.start()
    logger.info("⏰ Scheduler integrado iniciado correctamente")


@app.route('/')
def index():
    """Página principal"""
    session = get_session()
    try:
        # Obtener estadísticas rápidas
        total_numeros = session.query(NumeroExtraido).count()
        total_predicciones = session.query(Prediccion).count()
        
        # Últimos números extraídos
        ultimos_numeros = session.query(NumeroExtraido)\
            .order_by(NumeroExtraido.fecha_extraccion.desc())\
            .limit(10)\
            .all()
        
        # Última predicción
        ultima_prediccion = session.query(Prediccion)\
            .order_by(Prediccion.fecha_prediccion.desc())\
            .first()
        
        return render_template('index.html',
            total_numeros=total_numeros,
            total_predicciones=total_predicciones,
            ultimos_numeros=ultimos_numeros,
            ultima_prediccion=ultima_prediccion
        )
    finally:
        session.close()


@app.route('/dashboard')
def dashboard():
    """Dashboard con análisis completo"""
    session = get_session()
    try:
        predictor = PredictorNumeros()
        numeros, fechas = predictor.obtener_datos_historicos(limite=500)
        
        stats = {}
        predicciones = {}
        
        if len(numeros) >= predictor.min_samples:
            stats = predictor.analisis_estadistico(numeros)
            predicciones = predictor.predecir_proximo_numero(metodo='combinado')
        
        return render_template('dashboard.html',
            numeros=numeros,
            fechas=[f.isoformat() for f in fechas],
            stats=stats,
            predicciones=predicciones
        )
    finally:
        session.close()


@app.route('/scraper')
def scraper_config():
    """Página de configuración del scraper"""
    session = get_session()
    try:
        configuraciones = session.query(ConfiguracionScraper).all()
        return render_template('scraper.html', configuraciones=configuraciones)
    finally:
        session.close()


@app.route('/api/scraper/agregar', methods=['POST'])
def agregar_scraper():
    """Agregar nueva configuración de scraper"""
    data = request.json
    session = get_session()
    
    try:
        nueva_config = ConfiguracionScraper(
            url_objetivo=data['url'],
            selector_css=data.get('selector_css'),
            selector_xpath=data.get('selector_xpath'),
            intervalo_minutos=int(data.get('intervalo', 60)),
            activo=True
        )
        session.add(nueva_config)
        session.commit()
        
        return jsonify({'success': True, 'mensaje': 'Configuración agregada'})
        
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        session.close()


@app.route('/api/scraper/ejecutar/<int:config_id>', methods=['POST'])
def ejecutar_scraper_manual(config_id):
    """Ejecutar scraping manualmente"""
    session = get_session()
    
    try:
        config = session.query(ConfiguracionScraper).get(config_id)
        if not config:
            return jsonify({'success': False, 'error': 'Configuración no encontrada'}), 404
        
        use_selenium = config.selector_xpath is not None
        
        with WebScraper(use_selenium=use_selenium) as scraper:
            if use_selenium:
                numeros = scraper.extraer_numeros_selenium(
                    config.url_objetivo,
                    selector_css=config.selector_css,
                    selector_xpath=config.selector_xpath
                )
            else:
                numeros = scraper.extraer_numeros_simple(
                    config.url_objetivo,
                    selector_css=config.selector_css
                )
            
            if numeros:
                scraper.guardar_numeros(numeros, config.url_objetivo)
                config.ultima_ejecucion = datetime.utcnow()
                session.commit()
                
                return jsonify({
                    'success': True,
                    'numeros_encontrados': len(numeros),
                    'numeros': numeros[:20]  # Primeros 20
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No se encontraron números'
                })
                
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/prediccion/generar', methods=['POST'])
def generar_prediccion():
    """Generar nueva predicción"""
    data = request.json
    metodo = data.get('metodo', 'combinado')
    
    try:
        predictor = PredictorNumeros()
        predicciones = predictor.predecir_proximo_numero(metodo=metodo)
        
        if 'error' in predicciones:
            return jsonify({'success': False, 'error': predicciones['error']})
        
        # Guardar la predicción principal
        pred_principal = predicciones.get(metodo, predicciones.get('combinado'))
        if pred_principal:
            predictor.guardar_prediccion(
                pred_principal['numero'],
                pred_principal['confianza'],
                metodo
            )
        
        return jsonify({
            'success': True,
            'predicciones': predicciones
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/estadisticas')
def obtener_estadisticas():
    """Obtener estadísticas del sistema"""
    try:
        predictor = PredictorNumeros()
        numeros, fechas = predictor.obtener_datos_historicos(limite=500)
        
        if len(numeros) < predictor.min_samples:
            return jsonify({
                'error': 'Datos insuficientes',
                'disponibles': len(numeros),
                'necesarios': predictor.min_samples
            })
        
        stats = predictor.analisis_estadistico(numeros)
        
        return jsonify({
            'success': True,
            'estadisticas': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/numeros/recientes')
def obtener_numeros_recientes():
    """Obtener los números más recientes"""
    limite = request.args.get('limite', 50, type=int)
    session = get_session()
    
    try:
        numeros = session.query(NumeroExtraido)\
            .order_by(NumeroExtraido.fecha_extraccion.desc())\
            .limit(limite)\
            .all()
        
        datos = [
            {
                'id': n.id,
                'numero': n.numero,
                'fecha': n.fecha_extraccion.isoformat(),
                'fuente': n.fuente
            }
            for n in numeros
        ]
        
        return jsonify({'success': True, 'numeros': datos})
        
    finally:
        session.close()


@app.route('/api/numeros/agregar', methods=['POST'])
def agregar_numero_manual():
    """Agregar un número manualmente"""
    data = request.json
    numero = data.get('numero')
    sorteo = data.get('sorteo', 'Manual')
    hora = data.get('hora', datetime.now().strftime('%H:%M'))
    
    if numero is None:
        return jsonify({'success': False, 'error': 'Número no proporcionado'}), 400
        
    session = get_session()
    try:
        nuevo = NumeroExtraido(
            numero=int(numero),
            nombre_sorteo=sorteo,
            hora_sorteo=hora,
            fuente='Entrada Manual',
            fecha_extraccion=datetime.now()
        )
        session.add(nuevo)
        session.commit()
        return jsonify({'success': True, 'mensaje': 'Número agregado correctamente'})
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()


@app.route('/historial')
def historial():
    """Página de historial de predicciones"""
    session = get_session()
    try:
        predicciones = session.query(Prediccion)\
            .order_by(Prediccion.fecha_prediccion.desc())\
            .limit(100)\
            .all()
        
        return render_template('historial.html', predicciones=predicciones)
    finally:
        session.close()


@app.route('/historial-resultados')
def historial_resultados():
    """Página de historial de números extraídos"""
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 50
    session = get_session()
    try:
        total_numeros = session.query(NumeroExtraido).count()
        total_paginas = (total_numeros + por_pagina - 1) // por_pagina
        
        numeros = session.query(NumeroExtraido)\
            .order_by(NumeroExtraido.fecha_extraccion.desc())\
            .offset((pagina - 1) * por_pagina)\
            .limit(por_pagina)\
            .all()
        
        return render_template('historial_resultados.html', 
                             numeros=numeros, 
                             pagina=pagina, 
                             total_paginas=total_paginas,
                             total_numeros=total_numeros)
    finally:
        session.close()


@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_servidor(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Sistema de Predicción - Prediccion-7")
    print("="*50)
    print(f"\n📍 Servidor: http://127.0.0.1:5000")
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
