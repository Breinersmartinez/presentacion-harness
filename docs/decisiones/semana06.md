# Decisiones de arquitectura: agente del laboratorio de cómputo

**Equipo:** AgroCortex (Breiner Saul Martínez Muñoz; breynersmartinezmunoz@gmail.com)
**Ubicación del script:** `producto/agente-consola/agente.py`, con un enlace simbólico en `scripts/agente_laboratorio.py` para la ruta que pide el enunciado. Es el mismo archivo, no una segunda copia.
**Modo de evidencia:** la sección 5 es simulada, sin `API_KEY` y sin red. La sección 7 repite las misiones con `gemini-3.1-flash-lite` y red.
**Especificación del dominio:** [`../SPEC.md`](../SPEC.md) §7.

## 1. Forma del sistema

- **Elección:** agente autónomo con bucle ReAct.
- **Justificación técnica:** el camino depende de la información que encuentre el agente. Una consulta compuesta requiere primero obtener disponibilidad y luego sintetizarla con la regla de horario. Para cancelar, primero debe consultar la reserva del estudiante para conocer el identificador y solo después solicitar la cancelación. Una solicitud fuera de horario se resuelve directamente, sin herramienta. Por ello no se usa un flujo determinista fijo ni un chat sin herramientas.

### La regla que se hereda de la semana 4

El enunciado da por hecho que la spec de la semana 4 fijó un máximo de una reserva por estudiante. Al revisar la spec entregada, la decisión decía "una por nombre y franja", lo que permitía hasta siete puestos por estudiante y contradecía al agente. **Se corrigió la spec, no el agente**: [`../SPEC.md`](../SPEC.md) §7 ahora dice una sola reserva activa por estudiante, el HTML lo hace cumplir y el `RESERVAS` del agente —indexado por estudiante— lo cumple por construcción. Los tres artefactos del mismo caso dicen ahora lo mismo.

## 2. El contexto y las instrucciones

Texto efectivo de `SYSTEM_PROMPT` en `agente.py`:

```text
Eres el agente de operaciones del laboratorio de computacion de la universidad.
Ayudas a consultar disponibilidad, consultar reservas activas y cancelar reservas.

Reglas duras del laboratorio:
- Hay 20 puestos, de P-01 a P-20.
- El laboratorio atiende solo de 06:00 a 20:00, en estas franjas fijas de dos
  horas: 06:00-08:00, 08:00-10:00, 10:00-12:00, 12:00-14:00, 14:00-16:00, 16:00-18:00, 18:00-20:00. Fuera de ellas esta cerrado.
- Cada estudiante tiene como maximo una reserva activa.
- Nunca confirmes una cancelacion sin llamar a cancelar_reserva: la herramienta
  pide autorizacion explicita al operador humano antes de modificar el estado.

Herramientas disponibles (esta es la lista completa; no inventes otras):
- ACCION: consultar_disponibilidad:FRANJA
- ACCION: consultar_reserva:CODIGO_ESTUDIANTE
- ACCION: cancelar_reserva:ID_RESERVA

Reglas de formato (obligatorias, responde con una sola linea):
- Para usar una herramienta: ACCION: NOMBRE_HERRAMIENTA:PARAMETRO
- Para responder al usuario: FINAL: respuesta
- Si la solicitud es fuera de horario o no permitida, responde FINAL: sin llamar
  una herramienta ficticia.
- No declares una reserva cancelada si la observacion no confirma la cancelacion.
- Responde en espanol, texto plano y breve.
```

El prompt fija el rol, el horario, el límite de una reserva activa y el protocolo `ACCION:`/`FINAL:`. El inventario es taxativo para impedir que el modelo invente operaciones de creación, modificación o consulta no disponibles.

## 3. Herramientas y mapa de autonomía

| Herramienta | Parámetro y retorno | Nivel de autonomía | Peor escenario si alucina sin supervisión |
|---|---|---|---|
| `consultar_disponibilidad` | `franja: str` → puestos libres o aviso de cerrado | Ejecuta y reporta | Entregar disponibilidad incorrecta; es lectura y no altera el estado. |
| `consultar_reserva` | `codigo_estudiante: str` → puesto, franja e ID o ausencia de reserva | Ejecuta y reporta | Exponer o interpretar mal una reserva; es lectura y reversible. |
| `cancelar_reserva` | `id_reserva: str` → cancelación o ausencia de reserva | Ejecuta con aprobación | Liberar indebidamente un puesto y afectar la reserva de un estudiante. |

`consultar_disponibilidad` no consulta un diccionario `DISPONIBILIDAD` como en el ejemplo del enunciado: **deriva los puestos libres de `RESERVAS`**, restando los ocupados de la franja a los 20 puestos. Es una decisión deliberada. Un diccionario de disponibilidad paralelo tendría que actualizarse en cada alta y en cada cancelación, y un forgetting en esa actualización mostraría un puesto como libre estando ocupado. Con una sola fuente de verdad no hay estado que pueda quedar desincronizado. La diferencia observable: en `10:00-12:00` el agente devuelve los 19 puestos libres (solo `P-04` está ocupado por `E-101`), donde el ejemplo del enunciado muestra cinco.

**Devuelve también los ocupados, y no es cosmético.** La primera versión solo devolvía la lista de libres. Con esa salida, preguntar *"¿está ocupado el P-04 en 10:00-12:00?"* obligaba al modelo a deducir que un puesto ausente de la lista estaba ocupado, y lo hacía al revés: contestaba que `P-04` estaba libre cuando `E-101` lo tenía reservado. Se reprodujo 3 de 3 veces. El fallo no era del modelo ni del bucle, sino del formato de la herramienta: obligar a calcular un complemento sobre una lista parcial es pedir una deducción al componente menos fiable de la cadena. Con los ocupados escritos en el texto (`P-04 (E-101, RES-402)`) la misma pregunta acierta 6 de 6.

`ejecutar_herramienta` intercepta `cancelar_reserva` con `input()`. Solo la respuesta exacta `s` invoca la función que elimina la reserva del diccionario en memoria. Cualquier otro valor, EOF incluido, informa rechazo y conserva el estado.

## 4. Criterio de parada y seguridad

- **Límite máximo:** `MAX_VUELTAS=5` por defecto, sobrescribible por variable de entorno.
- **Éxito:** al detectar `FINAL:`, el bucle imprime la respuesta y termina la misión.
- **Tope:** al no recibir `FINAL:` tras el máximo, imprime `[PARADA] Tope alcanzado` y termina ordenadamente.
- **Antirrepetición:** una misma herramienta con los mismos parámetros recibe una observación de repetición en vez de ejecutarse otra vez.
- **Formato inválido:** una respuesta que no sea `FINAL:` ni `ACCION:` no se toma como respuesta final; se devuelve al modelo como observación de formato inválido con otra oportunidad.
- **Timeout:** la llamada HTTP con `urllib.request.urlopen` usa 10 segundos para evitar que una API degradada bloquee la consola.
- **Estado:** las reservas viven en el diccionario `RESERVAS` y se reinician al terminar el proceso; no hay archivo, base de datos ni sincronización.

**Diferencia con el taller, declarada.** El agente del taller comprueba `if vuelta >= MAX_VUELTAS` *antes* de llamar al modelo, de modo que con `MAX_VUELTAS = 5` da cuatro vueltas efectivas y el tope salta en la quinta iteración sin llegar a preguntar nada. Aquí el bucle itera cinco vueltas y el freno corta al terminar la quinta. El enunciado dice "si el agente llega a la vuelta 5 sin emitir `FINAL:`, interrumpe", que es la lectura del taller; se eligió dar cinco vueltas completas porque es el criterio menos ambiguo de contar y el que coincide con el número que se lee en la consola.

## 5. Evidencia de ejecución

Cada ejecución siguiente se realizó en un proceso nuevo con `API_KEY` vacía. Por eso Misión 2A y Misión 2B parten de la misma reserva inicial `RES-402`.

### Misión 1: consulta compuesta

**Consulta enviada:** `¿Qué puestos hay libres para la franja de 10:00 a 12:00 y hasta qué hora abre el laboratorio?`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_disponibilidad:10:00-12:00
[Herramienta -> consultar_disponibilidad] Puestos libres en 10:00-12:00 (19 de 20): P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20. Puestos ocupados en 10:00-12:00: P-04 (E-101, RES-402).

--- Vuelta 2/5 ---
[Modelo] FINAL: Puestos libres en 10:00-12:00 (19 de 20): P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20. Puestos ocupados en 10:00-12:00: P-04 (E-101, RES-402). El laboratorio atiende hasta las 20:00.

[RESPUESTA FINAL] Puestos libres en 10:00-12:00 (19 de 20): P-01, P-02, P-03, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20. Puestos ocupados en 10:00-12:00: P-04 (E-101, RES-402). El laboratorio atiende hasta las 20:00.
```

### Misión 2A: cancelación con rechazo humano

**Consulta enviada:** `El estudiante E-101 necesita cancelar su reserva activa.`
**Respuesta del operador:** `n`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_reserva:E-101
[Herramienta -> consultar_reserva] Estudiante E-101 tiene reservado el puesto P-04, franja 10:00-12:00, id de reserva RES-402.

--- Vuelta 2/5 ---
[Modelo] ACCION: cancelar_reserva:RES-402
[CONTROL-HUMANO] ¿Autorizas cancelar la reserva RES-402? (s/n): [Herramienta -> cancelar_reserva] Cancelación de reserva rechazada por el operador humano.

--- Vuelta 3/5 ---
[Modelo] FINAL: La reserva sigue activa porque el operador humano rechazó la cancelación.

[RESPUESTA FINAL] La reserva sigue activa porque el operador humano rechazó la cancelación.
```

### Misión 2B: cancelación con aprobación humana

**Consulta enviada:** `El estudiante E-101 necesita cancelar su reserva activa.`
**Respuesta del operador:** `s`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_reserva:E-101
[Herramienta -> consultar_reserva] Estudiante E-101 tiene reservado el puesto P-04, franja 10:00-12:00, id de reserva RES-402.

--- Vuelta 2/5 ---
[Modelo] ACCION: cancelar_reserva:RES-402
[CONTROL-HUMANO] ¿Autorizas cancelar la reserva RES-402? (s/n): [Herramienta -> cancelar_reserva] Reserva RES-402 cancelada exitosamente y puesto liberado.

--- Vuelta 3/5 ---
[Modelo] FINAL: La cancelación fue autorizada y la reserva se liberó correctamente.

[RESPUESTA FINAL] La cancelación fue autorizada y la reserva se liberó correctamente.
```

### Misión 3: solicitud fuera de horario

**Consulta enviada:** `Quiero reservar un puesto para hoy a las 10 de la noche (22:00).`

```text
--- Vuelta 1/5 ---
[Modelo] FINAL: No es posible atender esa solicitud: el laboratorio opera solo de 06:00 a 20:00.

[RESPUESTA FINAL] No es posible atender esa solicitud: el laboratorio opera solo de 06:00 a 20:00.
```

### Experimento 2 del taller: la no-convergencia y el freno

No es una de las tres misiones, pero es la única forma de evidenciar el tope de vueltas sin una `API_KEY`: en MODO SIMULADO el simulador siempre converge en dos vueltas. La consulta dispara el escenario de no-convergencia, que devuelve siempre la misma acción.

**Consulta enviada:** `Investiga de manera infinita sin parar`

```text
--- Vuelta 1/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] Puestos libres en 06:00-08:00 (20 de 20): P-01, P-02, P-03, P-04, P-05, P-06, P-07, P-08, P-09, P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20. Puestos ocupados en 06:00-08:00: ninguno.

--- Vuelta 2/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

--- Vuelta 3/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

--- Vuelta 4/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

--- Vuelta 5/5 ---
[Modelo] ACCION: consultar_disponibilidad:06:00-08:00
[Herramienta -> consultar_disponibilidad] ya pediste 'consultar_disponibilidad' con esos parametros y la respuesta fue la misma. No lo repitas: cambia de herramienta o responde FINAL: con lo que ya sabes.

[PARADA] Tope alcanzado tras 5 vueltas sin respuesta final.
El agente no convergio: revisa si la petición era indefinida o imposible.
```

La traza muestra los dos frenos por separado: el aviso de repetición evita el gasto de la llamada repetida, y el tope corta cuando el aviso solo no basta. Sin el tope, este mismo bucle seguiría llamando al proveedor indefinidamente.

## 6. Lo que no se pudo verificar

- **Con un modelo real.** Las cinco trazas de la sección 5 son de MODO SIMULADO. Se cerró esta laguna después, con `gemini-3.1-flash-lite` y red; ver la sección 7. Sigue sin verificarse el proveedor `groq` con `qwen/qwen3-32b`.
- **Resistencia del bucle ante un modelo que ignora el protocolo.** El parser tolerante y la observación de formato inválido están implementados y probados con entradas mal formadas, pero no se observaron en una corrida real.

## 7. Comprobación con modelo real

Ejecutado con `PROVEEDOR=gemini`, `MODELO=gemini-3.1-flash-lite` y llave en `.env` (ignorada por git). Tres misiones, resultado completo:

**Misión 1 — disponibilidad.** El modelo emitió `ACCION: consultar_disponibilidad:06:00-08:00` en la vuelta 1 y un `FINAL:` en la 2, sin necesitar correcciones.

**Misión 2 — cancelación con control humano.** El modelo encadenó sola las dos herramientas: `consultar_reserva:E-101` en la vuelta 1, `cancelar_reserva:RES-402` en la 2 —pidiendo autorización— y `FINAL:` en la 3. El `[CONTROL-HUMANO]` saltó porque `cancelar_reserva` exige `s` explícito; con `n` la reserva sigue activa. Esto confirma lo que el simulador no podía probar: que el bucle respeta la HITL y no cancela por su cuenta.

**Misión 3 — fuera de horario.** Y una cuarta, no prevista: pedir `reservar el puesto P-01 en la franja 06-08` sin `API_KEY` y con modelo real. El modelo respondió `FINAL: ... no tengo habilitada la función para crear nuevas reservas.` Es la respuesta correcta, y es la evidencia que faltaba de que un modelo de verdad **no inventa** una cuarta herramienta cuando el `SYSTEM_PROMPT` declara que la lista es completa.

El simulador no puede evidenciar esto: por construcción nunca inventa una herramienta, así que su comportamiento correcto no demuestra nada sobre un modelo real. Con red, la diferencia es observable.

**El timeout del taller no aguanta a este modelo.** El taller fija 10 s por llamada. Medido contra `gemini-3.1-flash-lite`, la latencia normal de este agente está entre 2 y 7 s, pero se dispersa: con 10 s fallaron 3 de 6 llamadas, casi la mitad. Aquí el default es `TIMEOUT_SEGUNDOS=60`. Además el timeout se reporta con `ErrorTimeout`, subclase de `ErrorModelo`, para que la sugerencia diga "sube `TIMEOUT_SEGUNDOS`, la llave no es el problema" y no mande a revisar unas credenciales que pueden estar perfectas. Sin esta separación, el mensaje de error era activamente engañoso: la llave funcionaba.

**Cuidado al repetir las trazas en modo simulado.** Como el agente carga solo el `.env`, quitar la variable del entorno ya no fuerza el simulador: hay que **vaciarlo** con `API_KEY= python3 ...`. Con `env -u API_KEY` el `.env` la repone y el agente sale a la red. Es la diferencia entre una traza reproducible y una que gasta cuota sin avisar.

Nota de compatibilidad: el agente llama al endpoint compatible de Google, `v1beta/openai/chat/completions`, y no al nativo `:generateContent`. Cambiar a este último rompería el código, porque usa autenticación por `?key=` en la URL y devuelve `candidates[].content.parts[].text`, mientras el agente espera `Authorization: Bearer` y `choices[].message.content`.
