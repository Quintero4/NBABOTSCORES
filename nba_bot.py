import requests
import telegram
import asyncio # USAMOS ESTA LIBRERÍA PARA PAUSAS ASÍNCRONAS
from datetime import datetime
# import time # <<< ELIMINADO: Ya no usaremos time.sleep
import os

# --- (1, 2, 3: CONFIGURACIÓN Y FUNCIONES PRINCIPALES DEL BOT — SIN CAMBIOS) ---

# ... (El código de las funciones obtener_resultados_nba y formatear_y_enviar_resultados sigue igual) ...

# --- 4. FUNCIÓN PRINCIPAL DE EJECUCIÓN (Ahora usando loop asíncrono) ---

async def main():
    """Función principal asíncrona que gestiona el bucle 24/7."""
    
    # Bucle infinito para que el servicio se mantenga activo
    while True:
        try:
            fecha_actual = datetime.now().strftime('%Y%m%d')
            
            print(f"--- NUEVO CICLO: Buscando resultados para la fecha: {fecha_actual} ---")
            
            datos_partidos = obtener_resultados_nba(fecha_actual)
            
            if datos_partidos:
                await formatear_y_enviar_resultados(datos_partidos)
            else:
                print("Fallo: La API de la NBA no devolvió datos o hubo un error de conexión.")
        
        except Exception as e:
            # En caso de error crítico
            print(f"ERROR CRÍTICO: {e}. Intentando reiniciar en 60 segundos...")
            await asyncio.sleep(60) # Pausa asíncrona de 1 minuto antes de reintentar
            continue
        
        # Pausa de 15 minutos (900 segundos) de forma asíncrona
        print("Ciclo completado. Esperando 15 minutos (900s) para la siguiente actualización.")
        await asyncio.sleep(900) # <<< ESTO ES LO QUE MANTIENE VIVO AL WORKER
        
# --- 5. PUNTO DE ENTRADA ---

if __name__ == "__main__":
    
    print("Iniciando Worker Asíncrono 24/7.")
    # Ejecutamos la función principal con el bucle infinito.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker detenido.")
