from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from routes.user import user
from routes.material import material_router
from routes.prestamo import prestamo_router

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="PRESTAMOS S.A. DE C.V",
    description="API para el almacenamiento de información de préstamo de equipo informático",
    version="1.0.0"
)

# Middleware CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Esquema de autenticación con OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuración de seguridad en Swagger (OpenAPI)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Configurar el esquema OpenAPI
app.openapi = custom_openapi

# Registrar las rutas (endpoints) de la API
app.include_router(user)
app.include_router(material_router)
app.include_router(prestamo_router)

# Ruta de prueba para verificar si el servidor está corriendo
@app.get("/")
async def root():
    return {"message": "API de PRESTAMOS S.A. de C.V. funcionando correctamente"}
