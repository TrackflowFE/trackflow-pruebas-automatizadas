# language: es
Característica: Comprobante del envío (HU-14)
  Como operador
  Quiero obtener el comprobante al registrar un envío
  Para entregárselo al remitente con su número de guía

  Escenario: CP-47 Registrar un envío muestra el comprobante
    Dado que ingresé como operador
    Cuando registro un envío de "MEDELLÍN - ANTIOQUIA" a "BOGOTÁ - CUNDINAMARCA"
    Entonces veo un número de guía con formato TF y doce caracteres
    Y puedo imprimir el comprobante
