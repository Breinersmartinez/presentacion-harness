# Informe de validación — reserva de puestos del laboratorio

**Skill:** `validar-resultado` · **Producto:** `producto/reservas-laboratorio.html`
**Spec:** [`SPEC.md`](SPEC.md) §6 (espejo: [`especificacion-reserva-puestos-laboratorio.html`](especificacion-reserva-puestos-laboratorio.html))
**Ejecución:** Google Chrome `--headless=new`, apertura por `file://` en un perfil limpio, interacción real sobre los botones y `location.reload()` para la persistencia. El DOM resultante se volca con `--dump-dom` y las aserciones se leen del propio documento.

## Veredicto

**Sirve** — los seis criterios de la spec se comprobaron con evidencia observable en un navegador real y ninguno falló.

## Criterios verificados

| Criterio de la spec (§6) | Estado | Evidencia |
|---|---|---|
| El archivo abre sin instalar dependencias. | Sí | Carga por `file://`, origen `file://`, sin instalación. El archivo no contiene ninguna referencia a un recurso remoto. |
| Hay 20 filas de puestos y 7 franjas de dos horas entre 06:00 y 20:00. | Sí | DOM: 20 filas, 140 celdas; encabezados `Puesto`, `06–08`, `08–10`, `10–12`, `12–14`, `14–16`, `16–18`, `18–20`. |
| Un nombre y un clic sobre una celda libre generan una reserva visible. | Sí | Con nombre "Ana" y un clic: la celda queda `Reservado: Ana`, `disabled=true`, aviso `Reservaste el puesto 1, franja 08–10.` |
| Sin nombre no se crea una reserva. | Sí | Con el campo vacío y un clic: la celda sigue `Disponible` y el aviso dice `Escribe tu nombre antes de reservar.` |
| Una reserva sobrevive a recargar la página. | Sí | Tras `location.reload()`, la misma celda sigue `Reservado: Ana` y deshabilitada; la tabla conserva 20 filas y 140 celdas; `localStorage` contiene `{"1-08–10":"Ana"}`. |
| Un estudiante no puede tener dos reservas activas. | Sí | Con "Ana" ya reservado, un clic en otra franja no crea nada: aviso `Ya tienes una reserva activa en el puesto 1, franja 08–10. El límite es una reserva por estudiante.` y la celda sigue `Disponible`. |

## Casos borde de §5 comprobados

- **Nombres que solo difieren en mayúsculas, acentos o espacios:** con `"  aNA  "` el segundo intento también se rechaza con el mismo aviso. Se consideran la misma persona.
- **Almacenamiento local inválido:** verificado fuera del navegador con el código de `cargar()`: ante un JSON corrupto o con claves inválidas devuelve un diccionario vacío y deja el aviso `Las reservas guardadas no eran válidas; se inició una vista vacía.`

## Fuera de los criterios

- La clave interna de `localStorage` (`agrocortex-reservas-laboratorio-v1`) conserva la marca de un proyecto anterior del grupo. No es visible para el usuario y no afecta al comportamiento. Anotado como limpieza futura, no como fallo.
- El producto no modela fechas ni tiene herramienta de cancelación. Es alcance declarado en `SPEC.md` §3, no una omisión.
- La evidencia del agente de la semana 6 es independiente de este producto y está en [`decisiones/semana06.md`](decisiones/semana06.md).

## Cambios respecto a la validación anterior

Este informe reemplaza al del 19 de septiembre. La diferencia de comportamiento es deliberada: el producto pasó de "una reserva por nombre y franja" a "una sola reserva activa por estudiante", para que el HTML y el agente de la semana 6 apliquen la misma regla del mismo caso. El criterio que prueba ese cambio es el sexto, nuevo en §6. Los cinco anteriores se volvieron a comprobar y siguen pasando.

## Siguiente corrección

- Tramo: ninguno (no hay fallo).
- Cambio concreto requerido: `Ninguno`.