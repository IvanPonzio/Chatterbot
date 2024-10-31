from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from .preprocessor import normalizar_texto, agregar_signos_apertura
from .corrector import sugerir_correccion
from .context_manager import ContextManager

# Cargar el modelo de spaCy en español
context_manager = ContextManager()

# Crear el chatbot
chatbot = ChatBot(
    'MiChatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.90
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    database_uri='sqlite:///database.sqlite3',
)

# Entrenar el chatbot
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.spanish")

# Función para obtener respuesta del chatbot con manejo de errores y sugerencias
def obtener_respuesta(texto):
    # Normalizar entrada para quitar acentos
    entrada_normalizada = normalizar_texto(texto)
    # Agregar signos de apertura
    entrada_con_signos = agregar_signos_apertura(entrada_normalizada)
    
    # Obtener el corpus de palabras conocidas
    corpus_conocido = ["Messi", "Cristiano", "fútbol", "jugador", "Barcelona"]
    
    # Verificar si hay errores tipográficos y sugerir correcciones
    sugerencias = sugerir_correccion(entrada_con_signos, corpus_conocido)
    
    # Si se encuentra una sugerencia, preguntar si el usuario quiso decir otra palabra
    if sugerencias:
        correccion = f"¿Quisiste decir {sugerencias[0][1]} en lugar de {sugerencias[0][0]}?"
        return correccion

    try:
        # Obtener respuesta del chatbot
        respuesta = chatbot.get_response(entrada_con_signos)

        # Si la confianza en la respuesta es baja, activar alerta
        if float(respuesta.confidence) < 0.5:
            logging.info(f"Pregunta: {entrada_con_signos} - Confianza baja ({respuesta.confidence})")
            return "No encontré la respuesta correcta. Estoy aprendiendo, pronto tendré una mejor respuesta."

        # Lógica para recordar información
        if "quien es" in entrada_con_signos.lower():
            context_manager.agregar_persona(entrada_con_signos)

        # Chequeamos el contexto para una respuesta más personalizada
        persona = context_manager.obtener_persona()
        if "quien es" in entrada_con_signos.lower() and persona:
            return f"{respuesta} ¿Te refieres a {persona}?"

        return str(respuesta)

    except Exception as e:
        # Registrar errores inesperados en el log
        logging.error(f"Error al obtener respuesta: {str(e)}")
        return "Hubo un problema técnico. Por favor, intenta de nuevo más tarde."

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() in ['salir', 'exit']:
            break
        respuesta = obtener_respuesta(pregunta)
        print(f"Chatbot: {respuesta}")
