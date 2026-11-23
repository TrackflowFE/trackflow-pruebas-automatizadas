# language: es
Característica: Ingreso del personal (regresión HU-08, HU-09)
  Como operador de TrackFlow
  Quiero ingresar con mi usuario y clave
  Para usar las pantallas de operación

  Antecedentes:
    Dado que estoy en la pantalla de ingreso

  Escenario: CP-28 Ingreso con credenciales válidas (regresión)
    Cuando ingreso con el usuario "operador" y su clave
    Entonces veo la pantalla "Registrar envío"

  Escenario: CP-33 Clave incorrecta sin revelar qué dato falló
    Cuando ingreso con el usuario "operador" y la clave "clave-equivocada"
    Entonces veo el aviso "El usuario o la clave no coinciden."
