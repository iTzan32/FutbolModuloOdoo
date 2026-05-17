# -*- coding: utf-8 -*-

from odoo import api, fields, models


class FootballTeam(models.Model):
    _name = "football.team"
    _description = "Equipo de fútbol base"
    _order = "season desc, category asc, name asc"

    name = fields.Char(string="Nombre del equipo", required=True)
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
    season = fields.Char(string="Temporada", required=True, default="2025/2026")
    coach_name = fields.Char(string="Entrenador")
    phone = fields.Char(string="Teléfono de contacto")
    player_ids = fields.One2many(
        comodel_name="football.player",
        inverse_name="team_id",
        string="Jugadores",
    )
    match_ids = fields.One2many(
        comodel_name="football.match",
        inverse_name="team_id",
        string="Partidos",
    )
    player_count = fields.Integer(
        string="Número de jugadores",
        compute="_compute_player_count",
    )
    active = fields.Boolean(string="Activo", default=True)

    @api.depends("player_ids")
    def _compute_player_count(self):
        """Calcula cuántos jugadores tiene cada equipo."""
        for team in self:
            team.player_count = len(team.player_ids)

    def get_pending_matches_for_report(self):
        """Devuelve los partidos que deben aparecer en el informe PDF."""
        self.ensure_one()
        return self.match_ids.filtered(
            lambda match: match.state in ("draft", "confirmed")
        ).sorted(lambda match: (match.match_date, match.code))

    def get_available_players_for_report(self):
        """Devuelve los jugadores disponibles que se imprimen en el informe."""
        self.ensure_one()
        return self.player_ids.filtered(lambda player: player.state == "available").sorted(
            lambda player: (player.jersey_number, player.full_name)
        )
