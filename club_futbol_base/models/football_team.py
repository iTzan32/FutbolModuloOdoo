# -*- coding: utf-8 -*-

# api, fields y models son las utilidades principales de Odoo ORM.
from odoo import api, fields, models


class FootballTeam(models.Model):
    # Nombre técnico del modelo de equipos.
    _name = "football.team"
    # Descripción legible para Odoo.
    _description = "Equipo de fútbol base"
    # Orden por defecto en listados.
    _order = "season desc, category asc, name asc"

    # Datos principales del equipo.
    name = fields.Char(string="Nombre del equipo", required=True)
    # Categoría deportiva del equipo.
    category = fields.Selection(
        selection=[
            ("prebenjamin", "Prebenjamín"),
            ("benjamin", "Benjamín"),
            ("alevin", "Alevín"),
            ("infantil", "Infantil"),
            ("cadete", "Cadete"),
            ("juvenil", "Juvenil"),
        ],
        string="Categoría",
        required=True,
    )
    # Temporada activa del equipo.
    season = fields.Char(string="Temporada", required=True, default="2025/2026")
    # Datos de contacto del entrenador o responsable.
    coach_name = fields.Char(string="Entrenador")
    phone = fields.Char(string="Teléfono de contacto")
    # Jugadores asociados a este equipo.
    player_ids = fields.One2many(
        comodel_name="football.player",
        inverse_name="team_id",
        string="Jugadores",
    )
    # Partidos asociados a este equipo.
    match_ids = fields.One2many(
        comodel_name="football.match",
        inverse_name="team_id",
        string="Partidos",
    )
    # Contador calculado para mostrar el tamaño de la plantilla.
    player_count = fields.Integer(
        string="Número de jugadores",
        compute="_compute_player_count",
    )
    # Permite archivar equipos sin borrarlos.
    active = fields.Boolean(string="Activo", default=True)

    @api.depends("player_ids")
    def _compute_player_count(self):
        """Calcula cuántos jugadores tiene cada equipo."""
        for team in self:
            # Cuenta los registros enlazados en player_ids.
            team.player_count = len(team.player_ids)

    def get_pending_matches_for_report(self):
        """Devuelve los partidos que deben aparecer en el informe PDF."""
        self.ensure_one()
        # Filtra pendientes y confirmados, y los ordena para el PDF.
        return self.match_ids.filtered(
            lambda match: match.state in ("draft", "confirmed")
        ).sorted(lambda match: (match.match_date, match.code))

    def get_available_players_for_report(self):
        """Devuelve los jugadores disponibles que se imprimen en el informe."""
        self.ensure_one()
        # Filtra jugadores convocables y los ordena por dorsal.
        return self.player_ids.filtered(lambda player: player.state == "available").sorted(
            lambda player: (player.jersey_number, player.full_name)
        )
