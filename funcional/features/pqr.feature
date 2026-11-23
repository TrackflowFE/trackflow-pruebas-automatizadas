# language: es
Característica: Peticiones, quejas y reclamos (HU-19)
  Como cliente
  Quiero radicar y consultar una PQR
  Para que atiendan mi caso y saber en qué va

  Antecedentes:
    Dado que estoy en la pantalla "PQR"

  Escenario: CP-53 Radicar una queja
    Cuando radico una "Queja" con la descripción "El paquete llegó con la caja rota y mojada."
    Entonces veo un radicado con formato "PQR-AAAA-NNNNN"
    Y veo el estado "Recibida"

  Escenario: CP-55 Consultar con un correo distinto al registrado
    Dado que radiqué una "Petición" con la descripción "Necesito cambiar la dirección de entrega."
    Cuando consulto el radicado con el correo "otra.persona@trackflow.test"
    Entonces veo el aviso "No encontramos una PQR con esos datos"
