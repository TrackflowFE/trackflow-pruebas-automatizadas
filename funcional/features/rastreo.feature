# language: es
Característica: Rastreo público con datos mínimos (HU-13)
  Como cliente sin cuenta
  Quiero rastrear mi envío con el número de guía
  Para saber dónde está sin exponer datos personales

  Escenario: CP-46 El rastreo anónimo enmascara los nombres
    Dado que existe un envío registrado de "Ana Torres" para "Luis Gómez"
    Cuando rastreo ese envío sin iniciar sesión
    Entonces veo el estado "REGISTRADO"
    Y veo los nombres "A*** T***" y "L*** G***"
    Y no veo los nombres completos
