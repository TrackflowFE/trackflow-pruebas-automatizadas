"""Precondiciones por API (más rápidas y estables que prepararlas por la interfaz)."""
import json
import urllib.request

from .config import CLAVES, URL_ENVIOS


def _post(ruta, cuerpo, token=None):
    req = urllib.request.Request(URL_ENVIOS + ruta, data=json.dumps(cuerpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          **({"Authorization": "Bearer " + token} if token else {})})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read() or b"{}")


def registrar_envio(remitente: str, destinatario: str) -> str:
    token = _post("/api/auth/login", {"username": "operador", "password": CLAVES["operador"]})["token"]
    envio = {"sender": {"fullName": remitente, "documentType": "CC", "documentNumber": "1000000001", "phone": "3001234545",
                        "address": "Calle 1 # 1-1", "cityId": 1},
             "recipient": {"fullName": destinatario, "documentType": "CC", "documentNumber": "2000000002",
                           "phone": "3009876543", "address": "Carrera 2 # 2-2", "cityId": 10},
             "description": "Envío para prueba de interfaz"}
    return _post("/api/shipments", envio, token)["trackingNumber"]
