"""Datos de prueba y configuración del ambiente. Se cambian por variables de entorno."""
import os

URL_FRONT = os.getenv("TF_URL_FRONT", "http://localhost:5173")
URL_ENVIOS = os.getenv("TF_URL_ENVIOS", "http://localhost:18080")
NAVEGADOR = os.getenv("TF_NAVEGADOR", "chromium")
VISIBLE = os.getenv("TF_VISIBLE") == "1"
CLAVES = {
    "operador": os.getenv("TF_CLAVE_OPERADOR", "Operador-Local-2026"),
    "supervisor": os.getenv("TF_CLAVE_SUPERVISOR", "Supervisor-Local-2026"),
    "admin": os.getenv("TF_CLAVE_ADMIN", "Admin-Local-2026"),
}
