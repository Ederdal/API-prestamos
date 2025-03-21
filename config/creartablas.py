from config.db import Base, engine
import models  # Importa todos los modelos

print("📌 Eliminando tablas existentes y volviendo a crearlas...")
Base.metadata.drop_all(bind=engine)  # Elimina todas las tablas primero
Base.metadata.create_all(bind=engine)  # Vuelve a crear las tablas
print("✅ Tablas creadas exitosamente.")
