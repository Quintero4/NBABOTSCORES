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
        response.raise_for_status() # Lanza error si el estado no es 2xx
        data = response.json()
        return data.get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"ERROR DE CONEXIÓN A LA API: {e}")
        return None
    except Exception as e:
        print(f"ERROR INESPERADO AL PROCESAR DATOS DE LA API: {e}")
        return None

# --- 3. FUNCIÓN DE ENVIAR MENSAJE (Asíncrona) ---

async def formatear_y_enviar_resultados(datos):
    """
    Formatea la información de los partidos y la envía a Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("ERROR: Tokens de Telegram no configurados.")
        return

    # Inicializa el bot (debe ser asíncrono para el envío)
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    mensaje = "🏀 **RESULTADOS NBA** 🏀\n\n"
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
                f"{ganador_visita} **{visita}** ({puntos_visita})\n"
                f"{ganador_casa} **{casa}** ({puntos_casa})\n"
                "--------------------\n"
            )
            partidos_encontrados = True

    if not partidos_encontrados:
        mensaje += "No se encontraron partidos finalizados para la fecha de hoy."

    try:
        # Enviar el mensaje
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text=mensaje, 
            parse_mode=telegram.constants.ParseMode.HTML
        )
        print("Mensaje enviado con éxito a Telegram.")
    except telegram.error.TelegramError as e:
        print(f"ERROR DE TELEGRAM: {e}")
    except Exception as e:
        print(f"ERROR INESPERADO al enviar mensaje: {e}")


# --- 4. FUNCIÓN PRINCIPAL DE EJECUCIÓN (Bucle Asíncrono 24/7) ---

# --- 4. FUNCIÓN PRINCIPAL DE EJECUCIÓN (Modo Prueba) ---

async def main():
    """
    Función principal asíncrona en MODO PRUEBA para verificar la conexión a Telegram.
    Se ejecutará una sola vez y enviará un mensaje.
    """
    try:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("ERROR: Tokens de Telegram no configurados. Verifica las variables.")
            return

        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        
        mensaje_prueba = (
            "✅ **BOT NBA - PRUEBA EXITOSA** ✅\n\n"
            "¡El bot está en línea en Railway y la conexión a Telegram funciona!\n\n"
            "El error 403 es por la clave de RapidAPI o límites de llamadas.\n\n"
            "➡️ Por favor, reemplaza el código con la versión completa y revisa la clave RAPIDAPI_KEY."
        )

        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text=mensaje_prueba, 
            parse_mode=telegram.constants.ParseMode.MARKDOWN
        )
        print("Mensaje de prueba enviado con éxito a Telegram.")
        
    except telegram.error.TelegramError as e:
        print(f"ERROR DE TELEGRAM EN PRUEBA: {e}")
    except Exception as e:
        print(f"ERROR INESPERADO EN PRUEBA: {e}")
        
    # Salir después de la prueba
    print("Modo de prueba completado. El proceso se detendrá.")
    # NO PONEMOS BUCLE WHILE TRUE NI SLEEP PARA QUE SE CIERRE Y NO GASTE RECURSOS

# --- 5. PUNTO DE ENTRADA ---
# (Esta sección debe seguir igual que antes)

if __name__ == "__main__":
    
    print("Iniciando Worker Asíncrono en MODO PRUEBA.")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker detenido.")


# --- 5. PUNTO DE ENTRADA ---

if __name__ == "__main__":
    
    print("Iniciando Worker Asíncrono 24/7.")
    # Ejecutamos la función principal con el bucle infinito.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker detenido.")


