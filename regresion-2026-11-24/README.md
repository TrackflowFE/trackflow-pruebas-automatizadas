# Regresión del 24/11/2026

Se repitió después de que desarrollo fusionara los arreglos de Sonar, sobre los main de ese día:
envíos `c7683ec`, reportes `fa17d02`, logística `0c8a00d` y frontend `1047d30`, con las APIs en local.

| Suite | Resultado |
|---|---|
| Unitarias (las tres APIs, `mvnw verify`) | 879 pruebas, 0 fallos (443 envíos · 221 reportes · 215 logística) |
| API (Newman) | 79 peticiones, 198 aserciones, 2 fallos: AT-35 y AT-70, defecto S3-01 (igual que el 22/11) |
| Funcionales (Playwright + pytest-bdd) | 10 de 10 en Chromium y 10 de 10 en Firefox |

Antes de cada corrida se reiniciaron las APIs, porque los límites de PQR por IP viven en memoria (defecto S3-02).
Antes de Newman se hizo una petición a cada API para calentarla: en frío, el primer login tarda unos 1,7 s y
supera el umbral de 1.500 ms de AT-00.

La prueba de carga (JMeter) no se repitió: los cambios no tocan los flujos medidos.
