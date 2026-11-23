"""Genera la colección Postman (v2.1) de pruebas de API del Sprint 3 de TrackFlow.

Cada petición lleva el ID del caso automatizado (AT-xx) y valida código de estado, contenido de
la respuesta y tiempo de respuesta. Uso: python generar_coleccion.py  ->  trackflow-sprint3.postman_collection.json
"""
import json
from pathlib import Path

AQUI = Path(__file__).parent
LIMITE_MS = 1500  # tiempo máximo aceptado por petición en local


def js(*lineas):
    return [l for l in "\n".join(lineas).split("\n")]


def req(id_, nombre, metodo, url, body=None, token=None, headers=None, tests=(), pre=()):
    h = [{"key": "Content-Type", "value": "application/json"}] if body is not None else []
    if token:
        h.append({"key": "Authorization", "value": "Bearer {{" + token + "}}"})
    for k, v in (headers or {}).items():
        h.append({"key": k, "value": v})
    item = {
        "name": f"{id_} · {nombre}",
        "request": {"method": metodo, "header": h, "url": url},
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": js(
            f"pm.test('{id_} tiempo de respuesta < {LIMITE_MS} ms', () => pm.expect(pm.response.responseTime).to.be.below({LIMITE_MS}));",
            *tests)}}],
    }
    if pre:
        item["event"].append({"listen": "prerequest", "script": {"type": "text/javascript", "exec": js(*pre)}})
    if body is not None:
        item["request"]["body"] = {"mode": "raw", "raw": body if isinstance(body, str) else json.dumps(body, ensure_ascii=False, indent=2)}
    return item


def estado(id_, codigo):
    return f"pm.test('{id_} responde {codigo}', () => pm.response.to.have.status({codigo}));"


def sin_clases_java(id_):
    return (f"pm.test('{id_} el error no expone clases Java', () => "
            "pm.expect(pm.response.text()).to.not.match(/java\\.|com\\.trackflow|Cannot deserialize/));")


def espera(ms):
    return f"setTimeout(() => {{}}, {ms});"


E, R, L = "{{baseEnvios}}", "{{baseReportes}}", "{{baseLogistica}}"
ENVIO = {
    "sender": {"fullName": "Ana Torres", "documentType": "CC", "documentNumber": "1000000001",
               "phone": "3001234545", "address": "Calle 1 # 1-1", "cityId": 1},
    "recipient": {"fullName": "Luis Gómez", "documentType": "CC", "documentNumber": "2000000002",
                  "phone": "3009876543", "address": "Carrera 2 # 2-2", "cityId": 10},
    "description": "Documentos de prueba automatizada",
}
RECOGIDA = {"address": "Calle 45 # 12-30, apto 201", "cityId": 1, "contactName": "Ana Torres",
            "contactPhone": "3001234567", "scheduledDate": "{{fechaRecogida}}", "timeSlot": "08:00-10:00",
            "packageSize": "MEDIUM", "weightKg": 5.5}
PQR = {"tipo": "QUEJA", "descripcion": "El paquete llegó con la caja rota y mojada.", "contactoNombre": "Ana Torres",
       "contactoEmail": "{{correoPqr}}", "contactoTelefono": "3001234567", "aceptaTratamientoDatos": True}

carpetas = []

# ---------------------------------------------------------------- 0. sesión de cada rol
carpetas.append(("00 · Preparación: ingreso de los tres roles", [
    req("AT-00", f"Ingreso {rol}", "POST", E + "/api/auth/login",
        {"username": rol, "password": "{{clave_" + rol + "}}"},
        tests=[estado("AT-00", 200),
               f"pm.environment.set('tk_{rol}', pm.response.json().token);",
               "pm.test('AT-00 el token es de tipo Bearer', () => pm.expect(pm.response.json().type).to.eql('Bearer'));"],
        pre=["pm.environment.set('usuarioQa', 'qa' + Date.now().toString(36));",
             "pm.environment.set('correoPqr', 'qa' + Date.now() + '@trackflow.test');",
             "// Fechas en hora de Colombia (UTC-5), como las cuenta la API",
             "const hoy = new Date(Date.now() - 5*3600000);",
             "const d = new Date(hoy.getTime() + 2*86400000); if (d.getUTCDay() === 0) d.setUTCDate(d.getUTCDate() + 1);",
             "pm.environment.set('fechaRecogida', d.toISOString().slice(0, 10));",
             "const s = new Date(hoy.getTime()); s.setUTCDate(s.getUTCDate() + ((7 - s.getUTCDay()) % 7 || 7));",
             "pm.environment.set('proximoDomingo', s.toISOString().slice(0, 10));"] if rol == "admin" else ())
    for rol in ("admin", "operador", "supervisor")]))

# ---------------------------------------------------------------- HU-11 usuarios
carpetas.append(("HU-11 · Gestión de usuarios, roles y permisos", [
    req("AT-01", "El administrador crea un usuario", "POST", E + "/api/admin/usuarios",
        {"username": "{{usuarioQa}}", "clave": "Temporal-12345", "roles": "OPERADOR", "email": "{{usuarioQa}}@trackflow.test"},
        token="tk_admin", tests=[estado("AT-01", 201),
                                 "const u = pm.response.json();",
                                 "pm.test('AT-01 nace activo, sin bloqueo y con su rol', () => { pm.expect(u.activo).to.be.true; pm.expect(u.bloqueado).to.be.false; pm.expect(u.roles).to.eql('OPERADOR'); });"]),
    req("AT-02", "Un operador no puede crear usuarios", "POST", E + "/api/admin/usuarios",
        {"username": "intruso1", "clave": "Temporal-12345", "roles": "ADMIN"}, token="tk_operador",
        tests=[estado("AT-02", 403)]),
    req("AT-03", "Rol desconocido", "POST", E + "/api/admin/usuarios",
        {"username": "rolraro", "clave": "Temporal-12345", "roles": "JEFE"}, token="tk_admin",
        tests=[estado("AT-03", 400), "pm.test('AT-03 dice qué roles existen', () => pm.expect(pm.response.json().detail).to.include('OPERADOR, SUPERVISOR o ADMIN'));"]),
    req("AT-04", "Usuario duplicado", "POST", E + "/api/admin/usuarios",
        {"username": "{{usuarioQa}}", "clave": "Temporal-12345", "roles": "OPERADOR"}, token="tk_admin",
        tests=[estado("AT-04", 409)]),
    req("AT-05", "El último administrador no puede perder su rol", "PUT", E + "/api/admin/usuarios/admin/roles",
        {"roles": "OPERADOR"}, token="tk_admin", tests=[estado("AT-05", 409)]),
]))

# ---------------------------------------------------------------- HU-10 contraseñas
carpetas.append(("HU-10 · Contraseña temporal, cambio y recuperación", [
    req("AT-06", "Ingreso con la clave temporal: token sin roles", "POST", E + "/api/auth/login",
        {"username": "{{usuarioQa}}", "password": "Temporal-12345"},
        tests=[estado("AT-06", 200), "pm.environment.set('tk_qa', pm.response.json().token);",
               "const p = JSON.parse(atob(pm.response.json().token.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));",
               "pm.test('AT-06 el token no trae roles y exige cambio', () => { pm.expect(p.roles).to.eql(''); pm.expect(p.mustChangePassword).to.be.true; });"]),
    req("AT-07", "Con la clave temporal no se registran envíos", "POST", E + "/api/shipments", ENVIO, token="tk_qa",
        tests=[estado("AT-07", 403)]),
    req("AT-08", "Clave nueva de menos de 10 caracteres", "POST", E + "/api/auth/clave/cambiar",
        {"actual": "Temporal-12345", "nueva": "corta"}, token="tk_qa",
        tests=[estado("AT-08", 400), "pm.test('AT-08 dice qué regla incumple', () => pm.expect(pm.response.json().detail).to.include('10 caracteres'));"]),
    req("AT-09", "Clave nueva igual a la anterior", "POST", E + "/api/auth/clave/cambiar",
        {"actual": "Temporal-12345", "nueva": "Temporal-12345"}, token="tk_qa",
        tests=[estado("AT-09", 400), "pm.test('AT-09 exige que sea distinta', () => pm.expect(pm.response.json().detail).to.include('distinta'));"]),
    req("AT-10", "Cambio de clave válido", "POST", E + "/api/auth/clave/cambiar",
        {"actual": "Temporal-12345", "nueva": "Nueva-Clave-2026"}, token="tk_qa", tests=[estado("AT-10", 204)]),
    req("AT-11", "Ingreso con la clave nueva recupera el rol", "POST", E + "/api/auth/login",
        {"username": "{{usuarioQa}}", "password": "Nueva-Clave-2026"},
        tests=[estado("AT-11", 200), "pm.environment.set('tk_qa', pm.response.json().token);",
               "const p = JSON.parse(atob(pm.response.json().token.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));",
               "pm.test('AT-11 el token ya trae OPERADOR', () => pm.expect(p.roles).to.eql('OPERADOR'));"]),
    req("AT-12", "Recuperar con un correo que no existe da la misma respuesta", "POST", E + "/api/auth/clave/recuperar",
        {"email": "nadie-{{usuarioQa}}@trackflow.test"},
        tests=[estado("AT-12", 202),
               "pm.test('AT-12 respuesta uniforme (no revela si la cuenta existe)', () => pm.expect(pm.response.json().mensaje).to.include('Si el correo corresponde a una cuenta'));"]),
]))

# ---------------------------------------------------------------- HU-09 bloqueo
carpetas.append(("HU-09 · Bloqueo por intentos fallidos", [
    req("AT-13", "Cinco intentos fallidos bloquean la cuenta", "POST", E + "/api/auth/login",
        {"username": "{{usuarioQa}}", "password": "clave-equivocada"},
        pre=["if (!pm.environment.get('intentos')) pm.environment.set('intentos', 0);"],
        tests=[estado("AT-13", 401),
               "const n = Number(pm.environment.get('intentos')) + 1; pm.environment.set('intentos', n);",
               "if (n < 5) { pm.execution.setNextRequest(pm.info.requestName); } else { pm.environment.unset('intentos'); }"]),
    req("AT-14", "Bloqueada, ni la clave correcta entra", "POST", E + "/api/auth/login",
        {"username": "{{usuarioQa}}", "password": "Nueva-Clave-2026"},
        tests=[estado("AT-14", 401),
               "pm.test('AT-14 el mensaje no revela el bloqueo', () => pm.expect(pm.response.json().detail).to.eql('Usuario o clave incorrectos'));"]),
    req("AT-15", "La auditoría registra el bloqueo", "GET", E + "/api/admin/usuarios/auditoria?cuantos=20", token="tk_admin",
        tests=[estado("AT-15", 200),
               "pm.test('AT-15 hay un CUENTA_BLOQUEADA del usuario', () => pm.expect(pm.response.json().some(a => a.accion === 'CUENTA_BLOQUEADA' && a.objetivo === pm.environment.get('usuarioQa'))).to.be.true);"]),
    req("AT-16", "El administrador desbloquea", "POST", E + "/api/admin/usuarios/{{usuarioQa}}/desbloquear", token="tk_admin",
        tests=[estado("AT-16", 200), "pm.test('AT-16 queda sin bloqueo y contador en 0', () => { const u = pm.response.json(); pm.expect(u.bloqueado).to.be.false; pm.expect(u.intentosFallidos).to.eql(0); });"]),
    req("AT-17", "Tras el desbloqueo entra de inmediato", "POST", E + "/api/auth/login",
        {"username": "{{usuarioQa}}", "password": "Nueva-Clave-2026"},
        tests=[estado("AT-17", 200), "pm.environment.set('tk_qa', pm.response.json().token);"]),
    req("AT-18", "Desactivar al usuario cierra su sesión", "PUT", E + "/api/admin/usuarios/{{usuarioQa}}/activo?valor=false", token="tk_admin",
        tests=[estado("AT-18", 200)]),
    req("AT-19", "El token del usuario desactivado ya no sirve", "GET", E + "/api/auth/sesion", token="tk_qa",
        tests=[estado("AT-19", 401)]),
]))

# ---------------------------------------------------------------- HU-14 y HU-13
carpetas.append(("HU-14 / HU-13 · Comprobante y datos personales", [
    req("AT-20", "Registrar un envío devuelve el comprobante", "POST", E + "/api/shipments", ENVIO, token="tk_operador",
        tests=[estado("AT-20", 202), "const j = pm.response.json(); pm.environment.set('guia', j.trackingNumber);",
               "pm.test('AT-20 guía con formato TF + 12', () => pm.expect(j.trackingNumber).to.match(/^TF[0-9A-Z]{12}$/));",
               "pm.test('AT-20 comprobante con seis campos', () => pm.expect(Object.keys(j.receipt)).to.have.members(['trackingNumber','registeredAt','senderName','originCity','recipientName','destinationCity']));"]),
    req("AT-21", "Reimprimir el comprobante", "GET", E + "/api/shipments/{{guia}}/receipt", token="tk_operador",
        pre=[espera(2500)],
        tests=[estado("AT-21", 200),
               "pm.test('AT-21 sin teléfonos ni direcciones', () => pm.expect(pm.response.text()).to.not.match(/3001234545|Calle 1/));",
               "pm.test('AT-21 no se guarda en caché', () => pm.expect(pm.response.headers.get('Cache-Control')).to.include('no-store'));"]),
    req("AT-22", "Comprobante sin sesión", "GET", E + "/api/shipments/{{guia}}/receipt", tests=[estado("AT-22", 401)]),
    req("AT-23", "Comprobante de una guía inexistente", "GET", E + "/api/shipments/TF000000000000/receipt", token="tk_operador",
        tests=[estado("AT-23", 404)]),
    req("AT-24", "El operador ve la ficha enmascarada", "GET", E + "/api/shipments/{{guia}}/ficha", token="tk_operador",
        tests=[estado("AT-24", 200), "const s = pm.response.json().sender;",
               "pm.test('AT-24 teléfono y documento enmascarados', () => { pm.expect(s.phone).to.eql('300 *** **45'); pm.expect(s.documentNumber).to.not.eql('1000000001'); });"]),
    req("AT-25", "El operador no ve la ficha completa", "GET", E + "/api/shipments/{{guia}}/ficha/completa", token="tk_operador",
        tests=[estado("AT-25", 403)]),
    req("AT-26", "El administrador ve la ficha completa", "GET", E + "/api/shipments/{{guia}}/ficha/completa", token="tk_admin",
        tests=[estado("AT-26", 200), "pm.test('AT-26 datos sin enmascarar', () => pm.expect(pm.response.json().sender.phone).to.eql('3001234545'));"]),
    req("AT-27", "Rastreo anónimo con datos mínimos", "GET", R + "/api/tracking/{{guia}}",
        tests=[estado("AT-27", 200), "const j = pm.response.json();",
               "pm.test('AT-27 nombres enmascarados, sin dirección y marcado restricted', () => { pm.expect(j.senderName).to.eql('A*** T***'); pm.expect(j.recipientAddress == null).to.be.true; pm.expect(j.restricted).to.be.true; });"]),
]))

# ---------------------------------------------------------------- HU-11 en reportes
q = "?from=2026-11-01&to=2026-11-20"
carpetas.append(("HU-11 · Reportes solo para supervisión", [
    req("AT-28", "El operador ya no ve los reportes", "GET", R + "/api/reports/transit-times" + q, token="tk_operador",
        tests=[estado("AT-28", 403)]),
    req("AT-29", "El supervisor ve los tiempos de tránsito", "GET", R + "/api/reports/transit-times" + q, token="tk_supervisor",
        tests=[estado("AT-29", 200), "pm.test('AT-29 trae el periodo pedido', () => { pm.expect(pm.response.json().from).to.eql('2026-11-01'); });"]),
    req("AT-30", "Periodo anterior al inicio de la operación", "GET", R + "/api/reports/shipment-volume?from=1939-01-01&to=1939-02-01", token="tk_supervisor",
        tests=[estado("AT-30", 400), "pm.test('AT-30 explica el límite', () => pm.expect(pm.response.json().detail).to.include('2026-01-01'));"]),
    req("AT-31", "Reporte sin sesión", "GET", R + "/api/reports/delayed-shipments", tests=[estado("AT-31", 401)]),
]))

# ---------------------------------------------------------------- HU-16 excepciones
carpetas.append(("HU-16 · Excepciones logísticas", [
    req("AT-32", "Excepción sobre un envío sin movimientos", "POST", L + "/api/shipments/{{guia}}/events",
        {"type": "EXCEPTION", "centerId": 1, "exceptionReason": "RECIPIENT_ABSENT"}, token="tk_operador",
        tests=[estado("AT-32", 422)]),
    req("AT-33", "Recibir el envío en el centro de origen", "POST", L + "/api/shipments/{{guia}}/events",
        {"type": "RECEIVED_AT_CENTER", "centerId": 1}, token="tk_operador", tests=[estado("AT-33", 202)]),
    req("AT-34", "Excepción sin motivo", "POST", L + "/api/shipments/{{guia}}/events",
        {"type": "EXCEPTION", "centerId": 1}, token="tk_operador", pre=[espera(2500)],
        tests=[estado("AT-34", 400), "pm.test('AT-34 lista los motivos válidos', () => pm.expect(pm.response.text()).to.include('RECIPIENT_ABSENT'));"]),
    req("AT-35", "Excepción con un motivo que no existe", "POST", L + "/api/shipments/{{guia}}/events",
        {"type": "EXCEPTION", "centerId": 1, "exceptionReason": "LLUVIA"}, token="tk_operador",
        tests=[estado("AT-35", 400), sin_clases_java("AT-35")]),
    req("AT-36", "Registrar la excepción con motivo y nota", "POST", L + "/api/shipments/{{guia}}/events",
        {"type": "EXCEPTION", "centerId": 1, "exceptionReason": "DAMAGED", "notes": "Caja mojada"}, token="tk_operador",
        tests=[estado("AT-36", 202)]),
    req("AT-37", "El historial muestra la excepción y el estado no retrocede", "GET", L + "/api/shipments/{{guia}}/events",
        pre=[espera(2500)],
        tests=[estado("AT-37", 200), "const m = pm.response.json().movements;",
               "pm.test('AT-37 hay dos movimientos y el último es la excepción', () => { pm.expect(m.length).to.eql(2); pm.expect(m[1].type).to.eql('EXCEPTION'); });",
               "pm.test('AT-37 el estado sigue en centro de distribución', () => pm.expect(m[1].resultingStatus).to.eql('AT_DISTRIBUTION_CENTER'));"]),
    req("AT-38", "El supervisor no registra movimientos", "POST", L + "/api/shipments/{{guia}}/events",
        {"type": "EXCEPTION", "centerId": 1, "exceptionReason": "HELD"}, token="tk_supervisor", tests=[estado("AT-38", 403)]),
]))

# ---------------------------------------------------------------- HU-20 recogidas
carpetas.append(("HU-20 · Recogidas a domicilio", [
    req("AT-39", "Horario de atención público", "GET", E + "/api/pickups/operating-hours",
        tests=[estado("AT-39", 200), "pm.test('AT-39 cinco franjas de 08:00 a 18:00', () => pm.expect(pm.response.json().slots).to.have.lengthOf(5));"]),
    req("AT-40", "Autoservicio: solicitar una recogida", "POST", E + "/api/pickups/self-service", RECOGIDA,
        tests=[estado("AT-40", 202), "const j = pm.response.json(); pm.environment.set('recogidaAuto', j.pickupNumber); pm.environment.set('codigoGestion', j.managementCode);",
               "pm.test('AT-40 número RC y código de 8 caracteres', () => { pm.expect(j.pickupNumber).to.match(/^RC/); pm.expect(j.managementCode).to.have.lengthOf(8); });"]),
    req("AT-41", "Consultar la recogida con el código de gestión", "GET", E + "/api/pickups/self-service/{{recogidaAuto}}",
        headers={"X-Codigo-Gestion": "{{codigoGestion}}"}, pre=[espera(2500)],
        tests=[estado("AT-41", 200), "pm.test('AT-41 queda solicitada', () => pm.expect(pm.response.json().status).to.eql('REQUESTED'));"]),
    req("AT-42", "Un código equivocado responde igual que una recogida inexistente", "GET", E + "/api/pickups/self-service/{{recogidaAuto}}",
        headers={"X-Codigo-Gestion": "AAAAAAAA"},
        tests=[estado("AT-42", 404), "pm.test('AT-42 mensaje que no revela cuál falló', () => pm.expect(pm.response.json().detail).to.eql('Recogida o código de gestión incorrectos'));"]),
    req("AT-43", "No se recoge los domingos", "POST", E + "/api/pickups/self-service", {**RECOGIDA, "scheduledDate": "{{proximoDomingo}}"},
        tests=[estado("AT-43", 422)]),
    req("AT-44", "Peso por encima de 100 kg", "POST", E + "/api/pickups/self-service", {**RECOGIDA, "weightKg": 100.5},
        tests=[estado("AT-44", 400)]),
    req("AT-45", "El autoservicio no puede vincular una guía", "POST", E + "/api/pickups/self-service", {**RECOGIDA, "shipmentTrackingNumber": "{{guia}}"},
        tests=[estado("AT-45", 400)]),
    req("AT-46", "Cancelar por autoservicio", "POST", E + "/api/pickups/self-service/{{recogidaAuto}}/cancel", {"reason": "Ya no lo necesito"},
        headers={"X-Codigo-Gestion": "{{codigoGestion}}"}, tests=[estado("AT-46", 202)]),
    req("AT-47", "Registrar el envío que se va a recoger", "POST", E + "/api/shipments", ENVIO, token="tk_operador",
        tests=[estado("AT-47", 202), "pm.environment.set('guiaRecogida', pm.response.json().trackingNumber);"]),
    req("AT-48", "El operador pide la recogida con la guía", "POST", E + "/api/pickups", {**RECOGIDA, "shipmentTrackingNumber": "{{guiaRecogida}}"},
        token="tk_operador", pre=[espera(2500)],
        tests=[estado("AT-48", 202), "pm.environment.set('recogida', pm.response.json().pickupNumber);"]),
    req("AT-49", "La misma guía no admite otra recogida activa", "POST", E + "/api/pickups", {**RECOGIDA, "shipmentTrackingNumber": "{{guiaRecogida}}"},
        token="tk_operador", pre=[espera(2000)], tests=[estado("AT-49", 409)]),
    req("AT-50", "Asignar la recogida al operador", "PUT", E + "/api/pickups/{{recogida}}/schedule",
        {"scheduledDate": "{{fechaRecogida}}", "timeSlot": "08:00-10:00", "assignedUsername": "operador"}, token="tk_operador",
        tests=[estado("AT-50", 202)]),
    req("AT-51", "Despachar", "POST", E + "/api/pickups/{{recogida}}/dispatch", token="tk_operador", pre=[espera(2000)],
        tests=[estado("AT-51", 202)]),
    req("AT-52", "Completar", "POST", E + "/api/pickups/{{recogida}}/complete", token="tk_operador", pre=[espera(2000)],
        tests=[estado("AT-52", 202)]),
    req("AT-53", "El envío recogido queda en custodia", "GET", R + "/api/tracking/{{guiaRecogida}}", token="tk_operador",
        pre=[espera(1500)],
        tests=[estado("AT-53", 200),
               "// El estado llega por eventos (recogidas -> logística -> reportes): se consulta hasta 15 veces",
               "const n = Number(pm.environment.get('sondeos') || 0) + 1;",
               "if (pm.response.json().status !== 'IN_CUSTODY' && n < 15) { pm.environment.set('sondeos', n); pm.execution.setNextRequest(pm.info.requestName); return; }",
               "pm.environment.unset('sondeos');",
               "pm.test('AT-53 estado IN_CUSTODY (tras ' + n + ' consultas)', () => pm.expect(pm.response.json().status).to.eql('IN_CUSTODY'));"]),
]))

# ---------------------------------------------------------------- HU-19 PQR
carpetas.append(("HU-19 · Peticiones, quejas y reclamos", [
    req("AT-54", "Radicar una queja", "POST", E + "/api/pqr", PQR,
        tests=[estado("AT-54", 201), "const j = pm.response.json(); pm.environment.set('radicado', j.radicado);",
               "pm.test('AT-54 radicado PQR-AAAA-NNNNN en estado RECIBIDA', () => { pm.expect(j.radicado).to.match(/^PQR-\\d{4}-\\d{5}$/); pm.expect(j.estado).to.eql('RECIBIDA'); });"]),
    req("AT-55", "Descripción de 19 caracteres (límite inferior)", "POST", E + "/api/pqr", {**PQR, "descripcion": "x" * 19},
        tests=[estado("AT-55", 400), "pm.test('AT-55 indica el rango 20 a 2000', () => pm.expect(pm.response.text()).to.include('entre 20 y 2000'));"]),
    req("AT-56", "Consultar con radicado y correo", "POST", E + "/api/pqr/consulta", {"radicado": "{{radicado}}", "email": "{{correoPqr}}"},
        tests=[estado("AT-56", 200), "pm.test('AT-56 sin respuesta mientras no se resuelva', () => pm.expect(pm.response.json().respuesta).to.be.null);"]),
    req("AT-57", "Consultar con un correo ajeno", "POST", E + "/api/pqr/consulta", {"radicado": "{{radicado}}", "email": "otro@trackflow.test"},
        tests=[estado("AT-57", 404)]),
    req("AT-58", "El operador no gestiona PQR", "GET", E + "/api/pqr", token="tk_operador", tests=[estado("AT-58", 403)]),
    req("AT-59", "No se salta de RECIBIDA a RESUELTA", "POST", E + "/api/pqr/{{radicado}}/estado", {"estado": "RESUELTA", "respuesta": "Respuesta de prueba"},
        token="tk_supervisor", tests=[estado("AT-59", 409)]),
    req("AT-60", "Pasar a EN_TRAMITE", "POST", E + "/api/pqr/{{radicado}}/estado", {"estado": "EN_TRAMITE"},
        token="tk_supervisor", tests=[estado("AT-60", 200)]),
    req("AT-61", "Resolver sin respuesta", "POST", E + "/api/pqr/{{radicado}}/estado", {"estado": "RESUELTA"},
        token="tk_supervisor", tests=[estado("AT-61", 400)]),
    req("AT-62", "Resolver con respuesta", "POST", E + "/api/pqr/{{radicado}}/estado", {"estado": "RESUELTA", "respuesta": "Le reponemos el envío sin costo."},
        token="tk_supervisor", tests=[estado("AT-62", 200)]),
    req("AT-63", "El solicitante ve la respuesta", "POST", E + "/api/pqr/consulta", {"radicado": "{{radicado}}", "email": "{{correoPqr}}"},
        tests=[estado("AT-63", 200), "const j = pm.response.json();",
               "pm.test('AT-63 estado RESUELTA con respuesta e historial de 3 pasos', () => { pm.expect(j.estado).to.eql('RESUELTA'); pm.expect(j.respuesta).to.include('reponemos'); pm.expect(j.historial).to.have.lengthOf(3); });"]),
]))

# ---------------------------------------------------------------- HU-21 chatbot
carpetas.append(("HU-21 · Chatbot de preguntas frecuentes", [
    req("AT-64", "Abrir una conversación", "POST", E + "/api/chatbot/sesiones",
        tests=[estado("AT-64", 201), "pm.environment.set('sesionChat', pm.response.json().sesionId);"]),
    req("AT-65", "Pregunta frecuente", "POST", E + "/api/chatbot/mensajes", {"sesionId": "{{sesionChat}}", "texto": "¿Cómo rastreo mi envío?"},
        tests=[estado("AT-65", 200), "const j = pm.response.json();",
               "pm.test('AT-65 responde la intención como_rastrear', () => { pm.expect(j.resultado).to.eql('RESPUESTA'); pm.expect(j.intencion).to.eql('como_rastrear'); });"]),
    req("AT-66", "Pregunta fuera de tema ofrece radicar una PQR", "POST", E + "/api/chatbot/mensajes", {"sesionId": "{{sesionChat}}", "texto": "¿Cuál es la capital de Francia?"},
        tests=[estado("AT-66", 200), "pm.test('AT-66 FUERA_DE_TEMA con acción ABRIR_PQR', () => { const j = pm.response.json(); pm.expect(j.resultado).to.eql('FUERA_DE_TEMA'); pm.expect(j.acciones[0].tipo).to.eql('ABRIR_PQR'); });"]),
    req("AT-67", "Un número de guía no consulta datos del envío", "POST", E + "/api/chatbot/mensajes", {"sesionId": "{{sesionChat}}", "texto": "{{guia}}"},
        tests=[estado("AT-67", 200), "pm.test('AT-67 manda a la página de rastreo sin mostrar datos', () => { pm.expect(pm.response.json().resultado).to.eql('NUMERO_DE_SEGUIMIENTO'); pm.expect(pm.response.text()).to.not.include('Luis'); });"]),
    req("AT-68", "Mensaje de 301 caracteres", "POST", E + "/api/chatbot/mensajes", {"sesionId": "{{sesionChat}}", "texto": "a" * 301},
        tests=[estado("AT-68", 400)]),
    req("AT-69", "Sesión inexistente", "POST", E + "/api/chatbot/mensajes", {"sesionId": "00000000-0000-0000-0000-000000000000", "texto": "hola"},
        tests=[estado("AT-69", 400), "pm.test('AT-69 pide crear otra sesión', () => pm.expect(pm.response.json().detail).to.include('Crea una nueva'));"]),
    req("AT-70", "Identificador de sesión mal formado", "POST", E + "/api/chatbot/mensajes", {"sesionId": "abc", "texto": "hola"},
        tests=[estado("AT-70", 400), sin_clases_java("AT-70")]),
]))

coleccion = {
    "info": {"name": "TrackFlow · Sprint 3 · Pruebas de API",
             "description": "Pruebas automatizadas de las historias del Sprint 3 (HU-09, 10, 11, 13, 14, 16, 19, 20 y 21) "
                            "sobre las tres APIs. Calidad de Software, EAV01.",
             "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
    "item": [{"name": n, "item": items} for n, items in carpetas],
}
(AQUI / "trackflow-sprint3.postman_collection.json").write_text(json.dumps(coleccion, ensure_ascii=False, indent=2), encoding="utf-8")
print(sum(len(i) for _, i in carpetas), "peticiones en", len(carpetas), "carpetas")
