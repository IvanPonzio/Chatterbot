import unicodedata

def normalizar_texto(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def agregar_signos_apertura(texto):
    texto = texto.strip()
    if texto.endswith("?") and not texto.startswith("¿"):
        if len(texto) > 1:
            texto = "¿" + texto
    if texto.endswith("!") and not texto.startswith("¡"):
        if len(texto) > 1:
            texto = "¡" + texto
    return texto
