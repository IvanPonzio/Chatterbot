import spacy

# Carga del modelo en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
    print("Modelo cargado exitosamente.")
    
    # Probar el modelo con una oración
    doc = nlp("Esto es una prueba.")
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.dep_)
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
