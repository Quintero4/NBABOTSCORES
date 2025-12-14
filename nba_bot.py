import requests
import telegram
import asyncio # Necesario para ejecutar el envío asíncrono
from datetime import datetime

# --- 1. CONFIGURACIÓN (TUS DATOS) ---

# Datos de Telegram
TELEGRAM_BOT_TOKEN = '8424595859:AAGLSCUR3DwGStRvvSoZlseX8Y2CPIvqDiE'
# ID de Chat (el número que empieza con -100...)
TELEGRAM_CHAT_ID = -1003320799916 

# Datos de RapidAPI
RAPIDAPI_HOST = 'nba-api-free-data.p.rapidapi.com'
RAPIDAPI_KEY = 'db43641f98msh7e84415090d14e7p1c529cjsn7bfa5538b221'
API_URL = 'https://nba-api-free-data.p.rapidapi.com/nba-scoreboard-by-date'

# --- 2. FUNCIONES DEL BOT ---

def obtener_resultados_nba(fecha_str):
    """
    Se conecta a RapidAPI para obtener los resultados de la NBA para una fecha dada.
    """
    
    # 2.1. Definir los encabezados (headers) con tu clave secreta
    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    
    # 2.2. Definir los parámetros de la petición (la fecha)
    querystring = {"date": fecha_str}
    
    try:
        # 2.3. Hacer la petición GET a la API (esta es síncrona y funciona)
        response = requests.get(API_URL, headers=headers, params=querystring, timeout=10)
        response.raise_for_status() # Lanza un error si la petición falla
        datos = response.json()
        return datos

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de la NBA: {e}")
        return None

# Convertimos esta función en asíncrona usando 'async'
async def formatear_y_enviar_resultados(datos_api):
    """
    Procesa los datos de la API y envía el mensaje a Telegram usando async/await.
    """
    
    # 1. Verificar la estructura JSON (busca 'response' y luego 'Events')
    if not datos_api or 'response' not in datos_api or 'Events' not in datos_api['response']:
        return "No se pudieron obtener resultados o la estructura de la API ha cambiado."
    
    # 2. Asignar la lista de partidos
    partidos = datos_api['response']['Events']

    if not partidos:
        return "No hay partidos de la NBA programados para la fecha seleccionada."
    
    mensaje = "🏀 **RESULTADOS DE LA NBA** 🏀\n\n"
    
    for partido in partidos:
        try:
            # --- CÓDIGO DEL PARSE (lógica ya revisada y correcta) ---
            competicion = partido.get('competitions', {})
            competidores = competicion.get('competitors', [])
            estado_detalle = partido.get('status', {}).get('type', {}).get('shortDetail', 'N/A')
            
            equipo_local = None
            equipo_visitante = None
            
            for comp in competidores:
                if comp.get('homeAway') == 'home':
                    equipo_local = comp
                elif comp.get('homeAway') == 'away':
                    equipo_visitante = comp
            
            if not equipo_local or not equipo_visitante:
                continue 
                
            abrev_local = equipo_local.get('team', {}).get('abbreviation', 'Local')
            puntuacion_local = equipo_local.get('score', '0')
            abrev_visitante = equipo_visitante.get('team', {}).get('abbreviation', 'Visitante')
            puntuacion_visitante = equipo_visitante.get('score', '0')

            if estado_detalle == 'Final' or estado_detalle == 'FT':
                estado_texto = "✅ **FINALIZADO**"
            elif estado_detalle in ['1st', '2nd', '3rd', '4th', 'OT', 'Halftime']:
                estado_texto = f"▶️ {estado_detalle} Cuarto" 
            else:
                estado_texto = "🕔 *Por empezar*"


            linea_partido = (
                f"{estado_texto}\n"
                f"**{abrev_visitante}** {puntuacion_visitante} - **{abrev_local}** {puntuacion_local}\n"
                "---"
            )
            mensaje += linea_partido + "\n"
        
        except Exception as e:
            print(f"ERROR EN EL PARSE DE UN PARTIDO: {e}") 
            continue 

    # 3. VERIFICACIÓN DEL MENSAJE ANTES DE ENVIAR
    if len(mensaje) < 25: 
        print("ADVERTENCIA: El mensaje está casi vacío. No hay resultados válidos para enviar.")
        return 

    # Enviar el mensaje
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        # Usamos 'await' para que funcione el envío
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje, parse_mode='Markdown')
        print("Mensaje enviado con éxito a Telegram.")
        return mensaje
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")
        return None

# --- 3. FUNCIÓN PRINCIPAL DE EJECUCIÓN ---

async def main():
    """Función principal asíncrona para orquestar la ejecución."""
    # Mantener la fecha conocida para una prueba de éxito garantizada
    #fecha_actual = '20250120
    # OBTIENE LA FECHA DE ACTUALIZADA DIARIA (11 de diciembre de 2025)
    fecha_actual = datetime.now().strftime('%Y%m%d')
    
    print(f"Buscando resultados para la fecha: {fecha_actual}")
    
    # 1. Obtener los datos (esta función es síncrona y no cambia)
    datos_partidos = obtener_resultados_nba(fecha_actual)
    
    # 2. Formatear y enviar (llamamos a la función asíncrona con 'await')
    if datos_partidos:
        await formatear_y_enviar_resultados(datos_partidos)
    else:
        print("Fallo: La API de la NBA no devolvió datos o hubo un error de conexión.")


if __name__ == "__main__":
    # Ejecutamos la función principal asíncrona
    asyncio.run(main())
