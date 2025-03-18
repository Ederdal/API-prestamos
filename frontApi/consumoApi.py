import requests

# URL base de la API
BASE_URL = "http://localhost:8000"

# Endpoint para obtener el token de autenticación
def obtener_token():
    url = f"{BASE_URL}/login"
    payload = {
        "userName": "tu_usuario",
        "password": "tu_contraseña"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Error al obtener el token:", response.json())
        return None

# Endpoint para obtener todos los usuarios
def obtener_usuarios(token):
    url = f"{BASE_URL}/users/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener los usuarios:", response.json())
        return None

# Obtener el token
token = obtener_token()
if token:
    # Obtener los usuarios
    usuarios = obtener_usuarios(token)
    if usuarios:
        print("Usuarios:", usuarios)