import json
import html

# Cargar los datos desde el archivo JSON
with open('datos_utf8.json', 'r', encoding='latin1') as file:
    data = json.load(file)

# Función para decodificar entidades HTML y convertir a UTF-8
def decode_html_entities(data):
    if isinstance(data, dict):
        return {key: decode_html_entities(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_html_entities(item) for item in data]
    elif isinstance(data, str):
        return html.unescape(data)  # Decodifica las entidades HTML
    return data

# Decodificar los datos
decoded_data = decode_html_entities(data)

# Guardar los datos decodificados en un nuevo archivo JSON
with open('2datos_utf8.json', 'w', encoding='utf-8') as file:
    json.dump(decoded_data, file, ensure_ascii=False, indent=4)