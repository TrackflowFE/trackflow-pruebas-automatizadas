# language: es
Característica: Asistente de preguntas frecuentes (HU-21)
  Como cliente
  Quiero resolver dudas comunes en un chat
  Para no tener que llamar ni radicar una PQR

  Antecedentes:
    Dado que abrí el asistente

  Escenario: CP-64 Pregunta frecuente
    Cuando pregunto "¿Cómo rastreo mi envío?"
    Entonces el asistente responde con un texto que contiene "escribe el número de guía"
    Y me ofrece el botón "Rastrear mi envío"

  Escenario: CP-65 Pregunta fuera de tema
    Cuando pregunto "¿Cuál es la capital de Francia?"
    Entonces el asistente responde con un texto que contiene "fuera de lo que puedo responder"
    Y me ofrece el botón "Radicar una PQR"

  Escenario: CP-66 Un número de guía no se consulta en el chat
    Cuando pregunto "TF4A2A12FEA4FB"
    Entonces el asistente responde con un texto que contiene "no consulto ni muestro información de envíos"
