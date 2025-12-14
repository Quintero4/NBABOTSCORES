import telegram
import asyncio

# TUS DATOS DE CONFIGURACIÓN
TOKEN = '8424595859:AAGLSCUR3DwGStRvvSoZlseX8Y2CPIvqDiE'
CHAT_ID = -1003320799916 
MENSAJE = "✅ ¡PRUEBA DE CONEXIÓN EXITOSA! El token y la ID funcionan."

async def enviar_mensaje_prueba():
    try:
        bot = telegram.Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=MENSAJE, parse_mode='Markdown')
        print("Mensaje de prueba enviado con éxito.")
    except Exception as e:
        print(f"ERROR AL ENVIAR MENSAJE DE PRUEBA. REVISA EL TOKEN O LA ID: {e}")

if __name__ == "__main__":
    # La advertencia venía de aquí. Usamos asyncio para ejecutar el await.
    try:
        asyncio.run(enviar_mensaje_prueba())
    except RuntimeError:
        # Esto maneja si ya hay un bucle de eventos corriendo (raro en este caso)
        asyncio.get_event_loop().run_until_complete(enviar_mensaje_prueba())