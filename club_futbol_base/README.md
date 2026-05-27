# Club Fútbol Base - Módulo Odoo

## 1. Descripción general

Este módulo gestiona la información básica de un club de fútbol base dentro de Odoo. Permite trabajar con equipos, jugadores y partidos, de forma sencilla y adecuada para un proyecto académico de **Sistemes de Gestió Empresarial**.

El módulo se llama técnicamente `club_futbol_base` y crea tres modelos principales:

- `football.team`: equipos del club.
- `football.player`: jugadores de cada equipo.
- `football.match`: partidos, convocatorias y resultados.

Además incluye un wizard para crear partidos rápidamente, un informe PDF con partidos pendientes por equipo y un controller web para consultar el estado de un partido mediante su código.

## 2. Objetivo del proyecto

El objetivo es resolver una necesidad realista de gestión deportiva: centralizar los datos de un club de fútbol base. Con este módulo el club puede saber qué jugadores pertenecen a cada equipo, qué partidos tiene programados, qué jugadores están disponibles y cuál es el estado de cada encuentro.

Es útil porque evita gestionar esta información de forma dispersa en hojas de cálculo o documentos sueltos. Odoo permite guardar los datos, relacionarlos, consultarlos desde vistas, imprimir informes y exponer información mediante una URL.

## 3. Requisitos técnicos cumplidos

| Requisito del profesor | Dónde se cumple en el proyecto | Archivo relacionado |
| --- | --- | --- |
| 4 vistas como mínimo | Hay vistas lista, formulario, kanban, calendario y search | `views/football_team_views.xml`, `views/football_player_views.xml`, `views/football_match_views.xml` |
| 4 métodos como mínimo | Hay métodos computados, restricciones y acciones | `models/football_player.py`, `models/football_match.py`, `models/football_team.py` |
| Vista search obligatoria | Search de partidos con filtros y agrupaciones | `views/football_match_views.xml` |
| 2 modelos relacionados | Equipos, jugadores y partidos relacionados con Many2one, One2many y Many2many | `models/football_team.py`, `models/football_player.py`, `models/football_match.py` |
| Wizard | Wizard para crear partidos de forma simplificada | `wizard/create_match_wizard.py`, `wizard/create_match_wizard_views.xml` |
| Funcionalidades especiales de vistas | Decoraciones de colores, líneas editables, sumatorios y widgets | `views/football_team_views.xml`, `views/football_player_views.xml`, `views/football_match_views.xml` |
| Report PDF | Informe de partidos pendientes por equipo | `report/report_pending_matches.xml`, `report/report_pending_matches_templates.xml` |
| Web controller | Ruta JSON para consultar el estado de un partido | `controllers/main.py` |
| Secuencia automática | Códigos de partido con `ir.sequence` | `data/ir_sequence.xml`, `models/football_match.py` |
| Seguridad | Permisos para usuarios internos | `security/ir.model.access.csv` |
| Datos de demostración | Equipos, jugadores y partidos de ejemplo | `demo/demo_data.xml` |

## 4. Estructura de archivos

- `__init__.py`: carga los paquetes principales del módulo: modelos, wizard y controllers.
- `__manifest__.py`: define la información del módulo, dependencias, datos XML, demo e instalación.
- `README.md`: explica el proyecto y sirve como guía de defensa.
- `controllers/__init__.py`: carga el archivo de controllers.
- `controllers/main.py`: define la ruta web `/club_futbol/partido/<codigo>/estado`.
- `data/ir_sequence.xml`: crea la secuencia automática para códigos de partido.
- `demo/demo_data.xml`: incluye equipos, jugadores y partidos de ejemplo.
- `models/__init__.py`: carga los modelos Python.
- `models/football_team.py`: define equipos y calcula el número de jugadores.
- `models/football_player.py`: define jugadores, edad, nombre completo y restricciones.
- `models/football_match.py`: define partidos, resultado, goles, restricciones, ordenación y acciones.
- `report/report_pending_matches.xml`: registra la acción del informe PDF.
- `report/report_pending_matches_templates.xml`: define la plantilla QWeb del informe.
- `security/ir.model.access.csv`: concede permisos básicos a usuarios internos.
- `views/football_menu.xml`: crea los menús principales del módulo.
- `views/football_team_views.xml`: define vistas de equipos.
- `views/football_player_views.xml`: define vistas de jugadores, incluida kanban.
- `views/football_match_views.xml`: define vistas de partidos, calendario y search.
- `wizard/__init__.py`: carga el wizard.
- `wizard/create_match_wizard.py`: crea partidos de forma rápida.
- `wizard/create_match_wizard_views.xml`: define la vista y acción del wizard.

## 5. Explicación de los modelos

### `football.team`

Representa un equipo del club. Sus campos principales son:

- `name`: nombre del equipo.
- `category`: categoría deportiva, como benjamín, alevín o juvenil.
- `season`: temporada, por ejemplo `2025/2026`.
- `coach_name`: entrenador del equipo.
- `phone`: teléfono de contacto.
- `player_ids`: jugadores del equipo.
- `match_ids`: partidos del equipo.
- `player_count`: número de jugadores calculado automáticamente.
- `active`: permite archivar equipos sin borrarlos.

### `football.player`

Representa un jugador. Sus campos principales son:

- `name` y `surname`: nombre y apellidos.
- `full_name`: nombre completo calculado.
- `dni`: documento identificativo.
- `phone`: teléfono.
- `birthdate`: fecha de nacimiento.
- `age`: edad calculada.
- `photo`: imagen del jugador.
- `position`: posición en el campo.
- `jersey_number`: dorsal.
- `state`: disponible, lesionado, sancionado o baja.
- `team_id`: equipo al que pertenece.

### `football.match`

Representa un partido. Sus campos principales son:

- `code`: código único generado automáticamente.
- `team_id`: equipo propio.
- `opponent`: rival.
- `match_date`: fecha y hora del partido.
- `field_name`: campo de juego.
- `match_type`: liga, amistoso o torneo.
- `state`: borrador, confirmado, jugado o cancelado.
- `player_ids`: convocatoria del partido.
- `goals_for` y `goals_against`: goles a favor y en contra.
- `result_label`: resultado calculado.
- `total_goals`: suma total de goles.
- `notes`: observaciones.

## 6. Explicación de las relaciones

El módulo usa las tres relaciones más habituales de Odoo:

- `Many2one`: cada jugador tiene un equipo mediante `team_id`. Cada partido también pertenece a un equipo mediante `team_id`.
- `One2many`: cada equipo muestra sus jugadores con `player_ids` y sus partidos con `match_ids`.
- `Many2many`: cada partido puede convocar varios jugadores y cada jugador puede participar en varios partidos mediante `player_ids`.

Estas relaciones permiten navegar desde un equipo a sus jugadores, desde un jugador a su equipo y desde un partido a su convocatoria.

## 7. Explicación de los métodos

### Métodos en `football.team`

- `_compute_player_count`: calcula el número de jugadores relacionados con el equipo.
- `get_pending_matches_for_report`: obtiene los partidos borrador o confirmados para el PDF.
- `get_available_players_for_report`: obtiene los jugadores disponibles para el PDF.

### Métodos en `football.player`

- `_compute_full_name`: concatena nombre y apellidos para obtener el nombre completo.
- `_compute_age`: calcula la edad usando la fecha de nacimiento.
- `_check_birthdate`: impide guardar una fecha de nacimiento futura.
- `_check_jersey_number`: impide dorsales menores que 1 o mayores que 99.

### Métodos en `football.match`

- `create`: asigna automáticamente un código usando `ir.sequence`.
- `_compute_result_label`: calcula si el resultado es Victoria, Empate, Derrota o Pendiente.
- `_compute_total_goals`: suma goles a favor y goles en contra.
- `_check_match_date`: impide confirmar partidos con fecha pasada.
- `_check_players_belong_to_team`: impide convocar jugadores de otro equipo.
- `_check_unavailable_players`: impide convocar jugadores lesionados, sancionados o de baja.
- `_check_team_busy`: impide tener dos partidos confirmados del mismo equipo a la misma fecha y hora.
- `action_confirm`: cambia el partido a confirmado.
- `action_set_draft`: devuelve el partido a borrador.
- `action_mark_played`: marca el partido como jugado.
- `action_cancel`: cancela el partido.
- `action_print_pending_matches`: permite imprimir el informe desde un partido.

## 8. Explicación del wizard

El wizard `football.create.match.wizard` sirve para crear un partido con menos pasos.

Funcionamiento:

1. El usuario entra en **Club Fútbol Base > Gestión deportiva > Crear partido rápido**.
2. Selecciona el equipo, rival, fecha, campo y tipo de partido.
3. Puede marcar `Incluir jugadores disponibles`.
4. Si lo marca, el wizard busca los jugadores del equipo cuyo estado sea `Disponible`.
5. Crea un registro `football.match` en estado `Borrador`.
6. Abre automáticamente el formulario del partido creado.

Este wizard demuestra el uso de `models.TransientModel` y automatiza una tarea frecuente.

## 9. Explicación del report PDF

El informe se llama **Informe de partidos pendientes por equipo**.

Se puede imprimir desde:

- El menú de impresión de un equipo.
- El botón `Informe pendientes` del formulario de un partido.

El PDF muestra:

- Nombre del proyecto.
- Equipo.
- Categoría.
- Temporada.
- Entrenador.
- Tabla de partidos en estado borrador o confirmado.
- Lista de jugadores disponibles.
- Fecha de generación del informe.

Los archivos implicados son:

- `report/report_pending_matches.xml`: registra la acción del informe.
- `report/report_pending_matches_templates.xml`: define el contenido visual del PDF.

## 10. Explicación del web controller

El controller está en `controllers/main.py`.

Ruta:

```text
/club_futbol/partido/<codigo>/estado
```

Ejemplo:

```text
/club_futbol/partido/PART-00001/estado
```

Recibe el código de un partido y devuelve una respuesta JSON. Si existe, devuelve:

- `found: true`
- `code`
- `team`
- `opponent`
- `match_date`
- `state`
- `result_label`

Si no existe, devuelve:

- `found: false`
- `message`

Esto demuestra cómo Odoo puede exponer información del módulo mediante una ruta web.

## 11. Cómo instalar el módulo

1. Copiar la carpeta `club_futbol_base` dentro de la carpeta de addons de Odoo.
2. Reiniciar el servidor de Odoo.
3. Activar el modo desarrollador si hace falta.
4. Ir a **Aplicaciones**.
5. Pulsar **Actualizar lista de aplicaciones**.
6. Buscar **Club Fútbol Base**.
7. Instalar el módulo.

### Instalación con Docker

El proyecto incluye un `docker-compose.yml` en la raíz para levantar Odoo y PostgreSQL sin instalar nada manualmente.

Pasos:

1. Abrir una terminal en la carpeta raíz del proyecto.
2. Ejecutar:

```bash
docker compose up -d
```

3. Abrir Odoo en:

```text
http://localhost:8069
```

4. Crear una base de datos desde la pantalla inicial de Odoo.
5. Entrar en **Aplicaciones**.
6. Actualizar la lista de aplicaciones.
7. Buscar e instalar **Club Fútbol Base**.

El `docker-compose.yml` monta el módulo local en `/mnt/extra-addons/club_futbol_base`, por eso Odoo puede encontrarlo como addon personalizado.

## 12. Cómo probar el proyecto

Pruebas recomendadas para la defensa:

1. Crear un equipo con categoría, temporada, entrenador y teléfono.
2. Crear varios jugadores para ese equipo.
3. Comprobar que el campo `Nombre completo` se calcula solo.
4. Comprobar que la edad se calcula a partir de la fecha de nacimiento.
5. Intentar crear un jugador con fecha de nacimiento futura y ver que Odoo no lo permite.
6. Intentar poner un dorsal `0` o `100` y ver que Odoo no lo permite.
7. Crear un partido y comprobar que el código se genera automáticamente.
8. Confirmar un partido y ver el estado en la barra superior.
9. Marcar un partido como jugado e introducir goles para ver `Victoria`, `Empate` o `Derrota`.
10. Probar que no deja convocar jugadores lesionados, sancionados o de baja.
11. Probar que no deja convocar jugadores de otro equipo.
12. Crear dos partidos confirmados para el mismo equipo a la misma fecha y hora y comprobar que no lo permite.
13. Usar el wizard **Crear partido rápido**.
14. Marcar `Incluir jugadores disponibles` y comprobar que se añaden automáticamente a la convocatoria.
15. Imprimir el PDF desde un equipo.
16. Imprimir el PDF desde el botón de un partido.
17. Consultar la URL del controller con un código real.

## 13. Posibles preguntas de defensa

**¿Qué modelos has creado?**  
He creado `football.team`, `football.player`, `football.match` y el wizard `football.create.match.wizard`.

**¿Qué relaciones hay?**  
Un equipo tiene muchos jugadores y muchos partidos. Cada jugador pertenece a un equipo. Cada partido pertenece a un equipo y puede tener varios jugadores convocados.

**¿Qué hace el wizard?**  
Crea un partido de forma rápida y opcionalmente añade automáticamente todos los jugadores disponibles del equipo.

**¿Qué hace el controller?**  
Permite consultar el estado de un partido por código mediante la ruta `/club_futbol/partido/<codigo>/estado`.

**¿Dónde están los métodos computados?**  
En `models/football_team.py`, `models/football_player.py` y `models/football_match.py`.

**¿Dónde están las restricciones?**  
Principalmente en `models/football_player.py` y `models/football_match.py`, usando `@api.constrains` y restricciones SQL.

**¿Dónde está el report?**  
En `report/report_pending_matches.xml` y `report/report_pending_matches_templates.xml`.

**¿Qué vistas especiales has usado?**  
He usado kanban para jugadores, calendario para partidos, search con filtros y agrupaciones, decoraciones de color en listas, widgets `image`, `statusbar`, `many2many_tags` y `badge`, además de sumatorios en la lista de partidos.

## 14. Comentarios en código

El código incluye comentarios breves en los puntos importantes:

- Secuencia automática de partidos.
- Cálculos de campos computados.
- Restricciones principales.
- Lista editable de jugadores en equipos.
- Búsqueda general de partidos en la vista search.

No se han añadido comentarios innecesarios para que el código siga siendo limpio y fácil de leer.

## 15. Calidad y revisión

Antes de entregar el módulo conviene revisar:

- Los imports de Python.
- Que los modelos estén cargados en `models/__init__.py`.
- Que el wizard esté cargado en `wizard/__init__.py`.
- Que los controllers estén cargados en `controllers/__init__.py`.
- Que todos los XML estén referenciados en `__manifest__.py`.
- Que no haya IDs XML duplicados.
- Que exista `security/ir.model.access.csv`.
- Que el módulo aparezca como instalable en Odoo.

El módulo está planteado para ser sencillo, defendible y completo, sin añadir complejidad innecesaria.
