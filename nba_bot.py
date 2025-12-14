import requests
import telegram
import asyncio
from datetime import datetime, timedelta
import os

# --- 1. CONFIGURACIÓN DE VARIABLES DE ENTORNO ---
# El bot obtiene estos valores de la pestaña Variables en Railway
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')

# Configuración de la API (NBA RapidAPI)
API_URL = "https://api-nba-v1.p.rapidapi.com/games"
HEADERS = {
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
    "X-RapidAPI-Key": RAPIDAPI_KEY
}

# --- 2. FUNCIÓN DE OBTENER DATOS (Síncrona) ---

def obtener_resultados_nba(fecha):
    """
    Obtiene los resultados de los partidos de la NBA para una fecha específica.
    La fecha debe estar en formato YYYYMMDD.
    """
    if not RAPIDAPI_KEY:
        print("ERROR: RAPIDAPI_KEY no está configurada.")
        return None

    # Ajusta la fecha al formato que espera la API (YYYY-MM-DD)
    try:
        fecha_formato_api = datetime.strptime(fecha, '%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
        print(f"Error: Formato de fecha inválido: {fecha}")
        return None

    querystring = {"date": fecha_formato_api}

    try:
        response = requests.get(API_URL, headers=HEADERS, params=querystring, timeout=15)
        response.raise_for_status() # Lanza error si el estado no es 2xx (incluyendo 403 Forbidden)
        data = response.json()
        return data.get('response', [])
    except requests.exceptions.RequestException as e:
        # Aquí capturamos el 403 Forbidden
        print(f"ERROR DE CONEXIÓN A LA API: {e}")
        return None
    except Exception as e:
        print(f"ERROR INESPERADO AL PROCESAR DATOS DE LA API: {e}")
        return None

# --- 3. FUNCIÓN DE ENVIAR MENSAJE (Asíncrona) ---

async def formatear_y_enviar_resultados(datos):
    """
    Formatea la información de los partidos y la envía a Telegram.
    Usa ParseMode.HTML para evitar errores de formato.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("ERROR: Tokens de Telegram no configurados.")
        return

    # Inicializa el bot (debe ser asíncrono para el envío)
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    mensaje = "🏀 <b>RESULTADOS NBA</b> 🏀\n\n" # Usamos <b> para HTML
    partidos_encontrados = False

    for partido in datos:
        # Solo mostrar partidos que han terminado (Status: 3 - Final)
        if partido.get('status', {}).get('code') == 3:
            
            # Obtener nombres y puntuaciones
            casa = partido['teams']['home']['name']
            visita = partido['teams']['visitors']['name']
            
            puntos_casa = partido['scores']['home']['points']
            puntos_visita = partido['scores']['visitors']['points']
            
            # Determinar el ganador
            ganador_casa = "🟢" if puntos_casa > puntos_visita else ""
            ganador_visita = "🟢" if puntos_visita > puntos_casa else ""

            mensaje += (
                f"{ganador_visita} <b>{visita}</b> ({puntos_visita})\n"
                f"{ganador_casa} <b>{casa}</b> ({puntos_casa})\n"
                "--------------------\n"
            )
            partidos_encontrados = True

    if not partidos_encontrados:
        mensaje += "No se encontraron partidos finalizados para la fecha de ayer."

    try:
        # Enviar el mensaje
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text=mensaje, 
            parse_mode=telegram.constants.ParseMode.HTML # <--- USAMOS HTML
        )
        print("Mensaje enviado con éxito a Telegram.")
    except telegram.error.TelegramError as e:
        print(f"ERROR DE TELEGRAM: {e}")
    except Exception as e:
        print(f"ERROR INESPERADO al enviar mensaje: {e}")


# --- 4. FUNCIÓN PRINCIPAL DE EJECUCIÓN (Bucle Asíncrono 24/7) ---

async def main():
    """Función principal asíncrona que gestiona el bucle 24/7."""
    
    # Bucle infinito para que el servicio se mantenga activo
    while True:
        try:
            # Usamos la fecha de ayer para obtener resultados completados
            fecha_revision = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            
            print(f"--- NUEVO CICLO: Buscando resultados para la fecha: {fecha_revision} ---")
            
            # Llama a la función síncrona
            datos_partidos = obtener_resultados_nba(fecha_revision)
            
            if datos_partidos:
                # Llama a la función asíncrona de envío
                await formatear_y_enviar_resultados(datos_partidos)
            else:
                print("Fallo: No se encontraron datos o hubo error en la API.")
        
        except Exception as e:
            # En caso de error crítico general
            print(f"ERROR CRÍTICO GENERAL: {e}. Intentando reiniciar en 60 segundos...")
            await asyncio.sleep(60)
            continue
        
        # Pausa de 15 minutos (900 segundos) de forma asíncrona
        print("Ciclo completado. Esperando 15 minutos (900s) para la siguiente actualización.")
        await asyncio.sleep(900) # Esto es lo que mantiene vivo al worker


# --- 5. PUNTO DE ENTRADA ---

if __name__ == "__main__":
    
    print("Iniciando Worker Asíncrono 24/7.")
    # Ejecutamos la función principal con el bucle infinito.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker detenido.")
