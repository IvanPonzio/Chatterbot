from difflib import get_close_matches

def sugerir_correccion(pregunta, corpus_conocido):
    palabras_pregunta = pregunta.split()
    sugerencias = []
    for palabra in palabras_pregunta:
        similitudes = get_close_matches(palabra, corpus_conocido, n=1, cutoff=0.9)
        if similitudes and palabra != similitudes[0]:
            sugerencias.append((palabra, similitudes[0]))
    return sugerencias
