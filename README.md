# ResultadosNBA Bot - Automatización de Resultados de Baloncesto en Telegram

Este proyecto consiste en un bot de Python automatizado que consulta la API de datos de la NBA para una fecha específica (generalmente el día actual), formatea los resultados de los partidos (puntuación, estado: FINALIZADO o EN VIVO) y los publica automáticamente en un canal de Telegram.

El bot está diseñado para ser ejecutado repetidamente mediante el Programador de Tareas de Windows, garantizando que el canal de Telegram esté siempre actualizado con la información más reciente de la jornada.

## Características

* **API Dinámica:** Consulta la API gratuita de RapidAPI para obtener datos en tiempo real de los partidos de la NBA.
* **Formato Limpio:** Los resultados se presentan en formato Markdown de Telegram.
* **Asíncrono:** Utiliza la librería `python-telegram-bot` en modo asíncrono (`async/await`) para garantizar un envío fiable del mensaje.
* **Automatizable:** Configurado para ser ejecutado sin intervención manual mediante el Programador de Tareas de Windows.

## Estructura del Proyecto

ResultadosNBA ├── nba_bot.py # Script principal de Python con la lógica de la API y Telegram. └── ejecutar_bot.bat # Script de comandos de Windows para ejecutar el bot de forma automática.


## Requisitos e Instalación

### 1. Requisitos de Python

Necesitas tener Python instalado (versión 3.10 o superior).

Instala las librerías necesarias mediante `pip`:

```bash
pip install requests python-telegram-bot

2. Configuración de Credenciales
El script nba_bot.py requiere tus credenciales de API y Telegram.

Asegúrate de configurar las siguientes variables en la sección 1. CONFIGURACIÓN del archivo nba_bot.py:
Los siguientes valores están censurados al final del código para no ser modificado por terceros
Variable TELEGRAM_BOT_TOKEN Valor de Ejemplo (Tus valores) 8424595859:AAGLSCUR3DwGStRvvSoZlseX8Y2CPI***** NotasT Token de tu Bot de Telegram.
Variable TELEGRAM_CHAT_ID Valor de Ejemplo -100332079**** Notas  ID de tu canal/chat de Telegram (debe empezar por -100).
Variable RAPIDAPI_KEY Valor de Ejemplo (Tus valores)  db43641f98msh7e84415090d14e7p1c529cjsn7bfa553***** Notas Tu clave de RapidAPI.

Automatización en Windows (Programador de Tareas)
El bot está diseñado para ser ejecutado directamente por el Programador de Tareas (Task Scheduler) de Windows.

1. El Archivo ejecutar_bot.bat
Este archivo contiene la ruta absoluta del ejecutable de Python y del script para evitar cualquier conflicto de rutas. Debe estar ubicado en la carpeta del proyecto.

Contenido del archivo ejecutar_bot.bat:
@echo off
REM Ejecución Directa de Python con Rutas Absolutas
"C:\Users\[TUUSUARIO]\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\[TUUSUARIO]\Documents\proyectos\ResultadosNBA\nba_bot.py"
timeout /t 5 /nobreak

2. Configuración de la Tarea Programada
Para asegurar la ejecución automática cada 15 minutos:

Abre el Programador de Tareas (Task Scheduler).

Haz clic en "Crear Tarea..." (Create Task...).

Pestaña General: Asigna el nombre NBA_Bot_Directo y marca "Ejecutar con los privilegios más altos".

Pestaña Desencadenadores (Triggers):

Crea un nuevo desencadenador Diario.

Configura "Repetir cada" a 15 minutos y "durante" a 12 horas.

Pestaña Acciones (Actions):

Crea una nueva acción: Iniciar un programa.

Programa/script: Introduce la ruta absoluta del archivo .bat: C:\Users\[TUUSUARIO]\Documents\proyectos\ResultadosNBA\ejecutar_bot.bat

Iniciar en (opcional): DEJAR ESTE CAMPO COMPLETAMENTE VACÍO para evitar conflictos de rutas.

Guarda la tarea. El bot se ejecutará automáticamente a la hora programada.
