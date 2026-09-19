# Informe de validación — reserva de puestos del laboratorio

**Skill:** validar-resultado · **Producto:** `producto/reservas-laboratorio.html`
**Spec:** `docs/especificacion-reserva-puestos-laboratorio.html`
**Fecha:** 19 de septiembre de 2026 · **Ejecución:** Chrome real (headless) vía DevTools Protocol, con interacción simulada y recarga.

## Veredicto

**Sirve** — los cinco criterios de la spec se comprobaron con evidencia observable en un navegador real y ninguno falló.

## Criterios verificados

| Criterio de la spec (§6) | Estado | Evidencia |
|---|---|---|
| El archivo abre sin instalar dependencias. | Sí | Carga por `file://` sin instalación; 0 errores de consola y 0 peticiones fallidas en Chrome. |
| Hay 20 filas de puestos y 7 franjas de dos horas entre 06:00 y 20:00. | Sí | DOM: encabezados `Puesto` + `06–08`…`18–20`; 20 filas; 140 celdas. |
| Un nombre y un clic sobre una celda libre generan una reserva visible. | Sí | Con nombre "Ana" y un clic, la celda pasa a "Reservado: Ana", queda deshabilitada y el aviso dice "Reservaste el puesto 1, franja 06–08." |
| Sin nombre no se crea una reserva. | Sí | Con el campo vacío, un clic no reserva: la celda sigue "Disponible" y el aviso dice "Escribe tu nombre antes de reservar." |
| Una reserva sobrevive a recargar la página. | Sí | Tras `reload`, la misma celda sigue "Reservado: Ana" y deshabilitada; la tabla mantiene 20 filas y 140 celdas. |

## Fuera de los criterios

- La clave interna de `localStorage` conserva la marca del proyecto anterior del grupo; no es visible para el usuario y no afecta el comportamiento. Se anota como limpieza futura, no como fallo.
- El informe de ejecución de la cadena en la semana 4 registró para `ejecutar-plan` "No verificable (9/9 escenarios simulados)": valor esperado para un criterio no comprobable en ese entorno; el presente informe comprueba hoy el criterio de persistencia en un navegador real.

## Siguiente corrección

- Tramo: ninguno (no hay fallo).
- Cambio concreto requerido: `Ninguno`.