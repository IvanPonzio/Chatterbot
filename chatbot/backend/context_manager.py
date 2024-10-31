# context_manager.py
import spacy

class ContextManager:
    def __init__(self):
        self.contexto = {}
        self.nlp = spacy.load("es_core_news_sm")  # Cargar el modelo de spaCy

    def agregar_persona(self, texto):
        doc = self.nlp(texto)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                self.contexto['persona'] = ent.text  # Guardamos la persona mencionada

    def obtener_persona(self):
        return self.contexto.get('persona', None)

    def limpiar_contexto(self):
        self.contexto.clear()  # Limpiar el contexto si es necesario
