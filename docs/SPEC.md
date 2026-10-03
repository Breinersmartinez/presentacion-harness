# Especificación — Reserva de puestos del laboratorio

**Estado:** decisiones cerradas para el Caso A del reto de la semana 4.
**Alcance del producto:** un archivo HTML que abre con doble clic, sin instalación, servidor ni dependencias.
**Espejo legible:** [`especificacion-reserva-puestos-laboratorio.html`](especificacion-reserva-puestos-laboratorio.html). Este markdown es la fuente contractual; ante cualquier diferencia entre los dos, manda este archivo.

---

## 1. Resumen

Construir una página local para que un estudiante vea los veinte puestos del laboratorio por franjas de dos horas, identifique los libres y reserve uno con su nombre; así puede escoger un puesto sin depender de una lista manual.

## 2. Objetivos

- Al abrir [`../producto/reservas-laboratorio.html`](../producto/reservas-laboratorio.html) con doble clic, se muestran exactamente 20 puestos y 7 franjas: 06–08, 08–10, 10–12, 12–14, 14–16, 16–18 y 18–20.
- Un usuario con nombre puede reservar una celda libre mediante un clic; el cambio se refleja en la misma vista.
- Una reserva permanece visible después de recargar el navegador en el mismo equipo.
- Una celda ya reservada no acepta una segunda reserva.
- Un estudiante tiene como máximo una reserva activa: si ya reservó, el intento de reservar otra celda se rechaza con un aviso.

## 3. Fuera de alcance

- **Cancelación:** se difiere para concentrar el ciclo en reservar y verificar el mínimo funcional.
- **Inicio de sesión y roles:** no se implementan porque el reto no permite servidor ni base de datos.
- **Sincronización entre equipos:** no se implementa; `localStorage` solo conserva datos en un navegador.
- **Sanciones por inasistencia:** no se implementan porque requieren una política institucional que el requisito no entrega.
- **Puestos con equipamiento especial:** se tratan como equivalentes en este ciclo porque no se definieron categorías.
- **Fechas y reserva anticipada:** no se modelan; la vista es el estado de un día de operación.

## 4. Diseño

La interfaz tiene un campo de nombre y una tabla. Cada cruce puesto–franja es una celda disponible o reservada. Al reservar, la aplicación valida el nombre, comprueba que ese estudiante no tenga ya una reserva activa, guarda el dato localmente y vuelve a dibujar la tabla.

Flujo de una reserva:

1. El estudiante escribe su nombre.
2. Elige una celda libre.
3. La aplicación valida el nombre y que no exista una reserva previa para esa persona.
4. Guarda la reserva en `localStorage` del navegador.
5. Actualiza la tabla y muestra el resultado en el aviso.

## 5. Casos borde

| Situación | Comportamiento esperado |
|---|---|
| El nombre está vacío. | No se reserva la celda, se muestra un aviso y el foco vuelve al campo de nombre. |
| La celda ya está reservada. | Se muestra como reservada, queda deshabilitada y no admite un clic adicional. |
| El estudiante ya tiene una reserva activa en otra celda. | No se crea la segunda reserva y se muestra un aviso que indica en qué puesto y franja está la reserva previa. |
| Dos nombres que solo difieren en mayúsculas, acentos o espacios. | Se consideran la misma persona, así que el segundo intento se rechaza. |
| El almacenamiento local contiene datos inválidos. | La tabla se muestra sin reservas y explica que los datos guardados no eran válidos. |
| El navegador no conserva la reserva en otro equipo. | La aplicación no promete sincronización; la reserva solo existe en el navegador que la creó. |

## 6. Criterios de aceptación

| Criterio | Cómo verificar | Respuesta |
|---|---|---|
| El archivo abre sin instalar dependencias. | Abrirlo con doble clic en un navegador moderno. | Sí / No |
| Hay 20 filas de puestos y 7 franjas de dos horas entre 06:00 y 20:00. | Contar los encabezados y las filas de la tabla. | Sí / No |
| Un nombre y un clic sobre una celda libre generan una reserva visible. | Escribir "Ana", pulsar una celda libre y leer el estado. | Sí / No |
| Sin nombre no se crea una reserva. | Vaciar el campo, pulsar una celda libre y comprobar el aviso. | Sí / No |
| Una reserva sobrevive a recargar la página. | Reservar, recargar y revisar la misma celda. | Sí / No |
| Un estudiante no puede tener dos reservas activas. | Reservar con un nombre, pulsar otra celda libre con el mismo nombre y comprobar que el aviso cita la reserva previa. | Sí / No |

## 7. Decisiones

| Duda | Elección | Descartado | Por qué |
|---|---|---|---|
| ¿Cómo identificar al estudiante? | Nombre escrito, máximo 40 caracteres. | Login institucional. | El archivo debe funcionar localmente y no hay servicio de autenticación. |
| ¿Qué franjas existen? | Siete franjas fijas de 2 horas. | Horarios configurables. | El enunciado fija 06:00–20:00 y el reto busca un mínimo pequeño. |
| ¿Cuántas reservas permite un estudiante? | Una sola reserva activa por estudiante, en cualquier franja. | Límites por franja, límites diarios y sanciones. | El enunciado no da esas políticas y no deben inventarse. Una sola reserva activa es el límite más simple de explicar y de comprobar, y es la misma regla que aplica el agente de la semana 6 sobre este mismo caso. |
| ¿Con cuánta anticipación se puede reservar? | El producto no modela fechas: la vista es el estado de un día de operación y una reserva vale para la franja que se elige en pantalla. | Calendario, reserva anticipada y reserva recurrente. | El caso del reto habla de franjas, no de fechas; introducir un calendario sería alcance agregado sin requisito que lo pida. |
| ¿Qué pasa si el que reserva no llega? | No hay penalización: la reserva sigue ocupando el puesto hasta que se libere a mano. | Registro de inasistencia, avisos y sanciones. | Una penalización exige una política institucional que el requisito no entrega. |
| ¿Dónde persiste? | `localStorage` del navegador. | Base de datos o sincronización. | La restricción prohíbe servidor y dependencias. |
| ¿Hasta cuándo se puede cancelar sin consecuencia? | No se define plazo porque la cancelación no está en este ciclo. | Un plazo de cancelación libre de penalización. | Fijar un plazo sobre una operación que no existe sería especificar algo que no se puede comprobar. |
| ¿Los veinte puestos son iguales? | Sí, los veinte son equivalentes en este ciclo. | Puestos con equipamiento especial. | No se definieron categorías de equipamiento en el requisito. |
| ¿Qué pasa si el laboratorio cierra por mantenimiento un día ya reservado? | El producto no lleva la baja: si el cierre se declara, el laboratorista avisa por el canal habitual y las reservas se liberan a mano desde el navegador. | Baja automática de reservas, lista de espera y reagendamiento. | Sin servidor no hay fuente de estado externa que sepa del cierre, y automatizarlo exigiría un modelo de avisos que el caso no entrega. |

**Trazabilidad con el agente de la semana 6.** Estas mismas reglas son las que aplica [`../producto/agente-consola/agente.py`](../producto/agente-consola/agente.py): 20 puestos `P-01`–`P-20`, siete franjas de dos horas entre 06:00 y 20:00 y **una reserva activa por estudiante**. La justificación está en [`decisiones/semana06.md`](decisiones/semana06.md).
