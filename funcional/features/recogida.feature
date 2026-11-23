# language: es
Característica: Recogida a domicilio por autoservicio (HU-20)
  Como remitente
  Quiero pedir que recojan mi paquete
  Para no tener que llevarlo a un centro

  Escenario: CP-59 Solicitar una recogida entrega número y código de gestión
    Dado que estoy en la pantalla "Pedir recogida"
    Cuando solicito una recogida en "MEDELLÍN - ANTIOQUIA" para dentro de dos días hábiles
    Entonces veo un número de recogida que empieza por "RC"
    Y veo un código de gestión de ocho caracteres
