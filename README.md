# TrackFlow · Pruebas automatizadas (Sprint 3)

Pruebas automatizadas del equipo de Calidad (Calidad de Software, UdeA 2026-2, equipo EAV01) sobre las tres APIs de TrackFlow y su frontend.

| Carpeta | Tipo | Herramienta | Contenido |
|---|---|---|---|
| [`api/`](api) | API e integración | Postman + Newman | 71 casos (AT-00 a AT-70) de HU-09, 10, 11, 13, 14, 16, 19, 20 y 21 |
| [`rendimiento/`](rendimiento) | Carga | Apache JMeter 5.6.3 | Hora pico: 50 clientes y 10 operadores concurrentes |
| [`funcional/`](funcional) | Funcional (E2E) | Playwright + pytest-bdd, Page Object | 10 escenarios Gherkin en español, Chromium y Firefox |

## Ambiente

Las pruebas corren en local, no contra Render: las tres APIs (rama `main` al 22/11/2026) con PostgreSQL 16 y RabbitMQ 3 en contenedores.

| Servicio | Dirección |
|---|---|
| API 1 · Envíos | http://localhost:18080 |
| API 2 · Reportes | http://localhost:18082 |
| API 3 · Logística | http://localhost:18083 |
| Frontend (TrackFlow-Frontend) | http://localhost:5173, con las tres URLs apuntando a las APIs locales |

Las claves de `api/local.postman_environment.json` y `funcional/support/config.py` son de esa instancia local de pruebas, no de producción. Se cambian por variables de entorno.

## Ejecutar

```bash
# API
cd api
npx newman run trackflow-sprint3.postman_collection.json -e local.postman_environment.json \
  --reporters cli,htmlextra -x

# Carga
cd rendimiento
jmeter -n -t trackflow-carga.jmx -l resultados.jtl -e -o reporte-html

# Funcional
cd funcional
pip install playwright==1.63.0 pytest pytest-bdd pytest-html
python -m playwright install chromium firefox
TF_NAVEGADOR=chromium pytest --html=reports/reporte-chromium.html
TF_NAVEGADOR=firefox  pytest --html=reports/reporte-firefox.html
```

## Resultados (22/11/2026)

| Suite | Resultado |
|---|---|
| API (Newman) | 71 casos, 194 aserciones: 192 pasan, 2 fallan por un defecto real (AT-35 y AT-70: errores que exponen clases Java) |
| Carga (JMeter) | 5.412 peticiones, 0 % de error, p95 de 63 ms, 74 peticiones/s |
| Funcional (Playwright) | 10 de 10 en Chromium y 10 de 10 en Firefox |

Los reportes HTML de cada ejecución están en `api/reportes/`, `rendimiento/reporte-html/` y `funcional/reports/`.
`rendimiento/con-limite-por-defecto/` es la primera corrida de carga, donde el límite del rastreo por IP devolvió 429 en el 93 % de las consultas.
