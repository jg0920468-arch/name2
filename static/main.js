// JavaScript principal para la aplicación
console.log('🚀 Predicción-7 - Sistema de Predicción Inteligente');

// Funciones globales de utilidad
function formatearFecha(fecha) {
    const d = new Date(fecha);
    return d.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatearPorcentaje(valor) {
    return (valor * 100).toFixed(1) + '%';
}

// Auto-refresh para estadísticas en tiempo real (opcional)
let autoRefreshInterval = null;

function habilitarAutoRefresh(intervaloSegundos = 60) {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }

    autoRefreshInterval = setInterval(() => {
        console.log('🔄 Auto-refresh...');
        // Aquí se pueden actualizar partes específicas de la página sin recargar todo
    }, intervaloSegundos * 1000);
}

// Animaciones de entrada
document.addEventListener('DOMContentLoaded', () => {
    // Animar cards al entrar
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
