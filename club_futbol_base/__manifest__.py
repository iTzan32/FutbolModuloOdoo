# -*- coding: utf-8 -*-
{
    "name": "Club Fútbol Base",
    "summary": "Gestión sencilla de equipos, jugadores y partidos de un club de fútbol base",
    "description": """
Módulo académico para gestionar un club de fútbol base.

Permite registrar equipos, jugadores y partidos, crear partidos mediante un
wizard, consultar el estado de un partido por controller web y generar un
informe PDF de partidos pendientes por equipo.
    """,
    "author": "Proyecto académico SGE",
    "version": "1.0.0",
    "category": "Sports/Management",
    "depends": ["base", "web"],
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
    "demo": [
        "demo/demo_data.xml",
    ],
    "installable": True,
    "application": True,
}

