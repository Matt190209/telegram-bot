import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from scraper import obtener_noticias  # Importar la función desde scraper.py

# Cargar variables de entorno
load_dotenv()

# Configuración de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /start"""
    await update.message.reply_text('¡Bienvenido! Usa /noticias para obtener las noticias más recientes.')

# Comando /noticias
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /noticias mostrando las noticias obtenidas"""
    await update.message.reply_text("Buscando las noticias más recientes...")
    
    # Obtener las noticias
    noticias = obtener_noticias()
    
    if noticias:
        for noticia in noticias:
            # Enviar imagen si está disponible
            if noticia.get('imagen'):
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=noticia['imagen'],
                    caption=f"📰 *{noticia['titulo']}*\n\n{noticia['descripcion']}\n\n[Leer más]({noticia['enlace']})",
                    parse_mode='Markdown',
                )
            else:
                # Enviar solo texto si no hay imagen
                await update.message.reply_text(
                    f"📰 *{noticia['titulo']}*\n\n{noticia['descripcion']}\n\n[Leer más]({noticia['enlace']})",
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
    else:
        await update.message.reply_text('Lo siento, no pude obtener las noticias en este momento.')

# Función principal que inicia el bot
def main():
    """Función principal que inicia el bot"""
    # Crear la aplicación y pasar el token de tu bot
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("No se encontró el token del bot en las variables de entorno.")
        return

    application = Application.builder().token(token).build()

    # Registrar los manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("noticias", noticias))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()