# Plan — correcciones de cumplimiento: semanas 4 y 6

**Fuentes de verdad:** [especificación de reservas](../especificacion-reserva-puestos-laboratorio.html) y [reto de semana 6](https://ingenieria-aplicaciones-ia.netlify.app/semana06/workshop).  
**Responsable:** Breiner Martínez.  
**Alcance:** corregir el límite declarado del HTML y llevar el agente de consola, su documentación y sus trazas al contrato del reto de semana 6. Este plan no sustituye [PLAN.md](../PLAN.md), que conserva la evidencia del ciclo original de semana 4.

## Tareas

| # | Resultado | Responsable | Depende de | Estimación | Criterio de aceptación |
|---|---|---|---|---:|---|
| 1 | El HTML impide que un mismo nombre reserve más de un puesto en la misma franja. | Breiner Martínez | — | 1 h | Al reservar `Ana` en una franja y pulsar otra celda libre de esa misma franja con el nombre `Ana`, no se crea la segunda reserva y se muestra un aviso; `Ana` sí puede reservar en una franja distinta. **Superada por la tarea 6.** |
| 2 | El agente implementa en memoria el dominio obligatorio: puestos `P-01`–`P-20`, siete franjas `HH:00-HH:00`, una reserva por estudiante e identificadores `RES-*`. | Breiner Martínez | — | 3 h | `agente.py` declara estado en memoria y las funciones `consultar_disponibilidad(franja)`, `consultar_reserva(codigo_estudiante)` y `cancelar_reserva(id_reserva)`; una consulta inválida informa que el laboratorio está cerrado. |
| 3 | El bucle ReAct y el simulador ejecutan las tres misiones oficiales con salvaguardas correctas. | Breiner Martínez | 2 | 2 h | Con `API_KEY` vacía: (a) la misión compuesta consulta `10:00-12:00` y responde con puestos y cierre a las 20:00; (b) cancelar `E-101` pide confirmación y tanto `n` como `s` producen el resultado correcto; (c) la solicitud de 22:00 responde `FINAL:` en la primera vuelta sin herramienta. El tope predeterminado es 5 y las llamadas HTTP usan 10 segundos. |
| 4 | La documentación de semana 6 describe la arquitectura y conserva trazas reales de las cuatro ejecuciones requeridas. | Breiner Martínez | 2, 3 | 2 h | Existe `docs/decisiones/semana06.md` con el `SYSTEM_PROMPT` literal, mapa de autonomía, criterio de parada y trazas de Misión 1, Misión 2 con `n`, Misión 2 con `s` y Misión 3. |
| 5 | El README del agente describe únicamente el comportamiento corregido y cómo repetir las pruebas. | Breiner Martínez | 2, 3, 4 | 1 h | `producto/agente-consola/README.md` nombra exactamente las tres herramientas oficiales, el estado en memoria, `MAX_VUELTAS=5` y los comandos para reproducir las misiones. |

## Segunda ronda: unificar la regla y cerrar los huecos de los enunciados

**Origen:** una auditoría de los dos retos contra los enunciados encontró que el enunciado de la semana 6 da por hecho que la spec de la semana 4 fijó un máximo de una reserva por estudiante, cuando la spec decidía "una por nombre y franja". Los tres artefactos del mismo caso decían cosas distintas.

| # | Resultado | Responsable | Depende de | Estimación | Criterio de aceptación |
|---|---|---|---|---:|---|
| 6 | Una sola reserva activa por estudiante, en los tres artefactos. | Breiner Martínez | — | 1 h | La spec (`docs/SPEC.md` §7 y su espejo HTML) dice una reserva activa por estudiante; el HTML rechaza una segunda reserva del mismo nombre y el aviso cita el puesto y la franja de la reserva previa; el agente mantiene la regla por construcción de `RESERVAS`. |
| 7 | Las seis decisiones que el enunciado de la semana 4 manda decidir están escritas con su porqué. | Breiner Martínez | 6 | 1 h | La tabla de decisiones cubre identificación, franjas, límite de reservas, anticipación, inasistencia, cancelación sin consecuencia, persistencia, equivalencia de los puestos y cierre por mantenimiento. |
| 8 | El entregable `docs/SPEC.md` tiene las siete secciones en markdown. | Breiner Martínez | 6, 7 | 1 h | `docs/SPEC.md` contiene Resumen, Objetivos, Fuera de alcance, Diseño, Casos borde, Criterios de aceptación y Decisiones; el HTML queda como espejo declarado. |
| 9 | El criterio de parada del agente queda evidenciado, no solo descrito. | Breiner Martínez | 3 | 1 h | Existe en `docs/decisiones/semana06.md` una quinta traza, con salida real de terminal, donde el bucle agota `MAX_VUELTAS` e imprime `[PARADA] Tope alcanzado`. |
| 10 | Las divergencias frente al agente del taller quedan declaradas, no escondidas. | Breiner Martínez | 3 | 30 min | `semana06.md` explica por qué la disponibilidad se deriva de `RESERVAS` en vez de un diccionario aparte, por qué hay cinco vueltas efectivas y no cuatro, y que `scripts/agente_laboratorio.py` es un enlace simbólico y no una segunda copia. |
| 11 | El reporte de la semana 4 responde lo que el enunciado pregunta. | Breiner Martínez | 8 | 1 h | `semana04.md` declara el renombre de `escribir-spec` a `crear-especificacion`, dice dónde vive cada copia incluyendo `~/.opencode/skills/`, y contiene la tabla de dos columnas de la medición del skill del taller. |

**Fuera de esta ronda:** volver a ejecutar las cuatro tareas del ciclo original por `ejecutar-plan` para llenar las columnas de conducta de la tabla por tarea; requiere repetir el ciclo y solo aporta registro, no cambio de producto.

## Orden y dependencias

La tarea 1 es independiente porque corrige una decisión ya documentada del HTML. La tarea 2 establece el dominio y las tres herramientas; sin ella no se puede validar el bucle ni generar evidencia real. La tarea 3 prueba la conducta agéntica sobre ese dominio. La documentación y el README dependen de la implementación comprobada para no registrar trazas o instrucciones divergentes.

## Primera tarea

**Tarea 1 — límite de una reserva por nombre y franja.** No tiene dependencias y puede ejecutarse de inmediato.

## Fuera de este ciclo

- Cancelación desde el HTML: continúa fuera de alcance de la spec de semana 4; la cancelación exigida se implementa solo en el agente de consola de semana 6.
- Login, roles, servidor, base de datos y sincronización entre equipos: siguen fuera de alcance.
- Creación de reservas desde el agente: no se agrega, porque el reto de semana 6 exige consulta y cancelación, no una nueva operación de reserva.
