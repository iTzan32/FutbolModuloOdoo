# -*- coding: utf-8 -*-
# Manifest del módulo: Odoo lee este diccionario al instalar la app.
{
    # Nombre y textos que aparecen en la pantalla de Apps.
    "name": "Club Fútbol Base",
    "summary": "Gestión sencilla de equipos, jugadores y partidos de un club de fútbol base",
    "description": """
Módulo académico para gestionar un club de fútbol base.

Permite registrar equipos, jugadores y partidos, crear partidos mediante un
wizard, consultar el estado de un partido por controller web y generar un
informe PDF de partidos pendientes por equipo.
    """,
    # Metadatos de autoría y versión del módulo.
    "author": "Proyecto académico SGE",
    "version": "1.0.0",
    "category": "Sports/Management",
    # Módulos de Odoo necesarios para que este funcione.
    "depends": ["base", "web"],
    # Archivos cargados siempre al instalar o actualizar el módulo.
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml",
        "views/football_menu.xml",
        "views/football_team_views.xml",
        "views/football_player_views.xml",
        "views/football_match_views.xml",
        "wizard/create_match_wizard_views.xml",
        "report/report_pending_matches.xml",
        "report/report_pending_matches_templates.xml",
    ],
    # Datos de ejemplo que Odoo carga solo con demo activada.
    "demo": [
        "demo/demo_data.xml",
    ],
    # Indica que el módulo se puede instalar y aparece como aplicación.
    "installable": True,
    "application": True,
}
