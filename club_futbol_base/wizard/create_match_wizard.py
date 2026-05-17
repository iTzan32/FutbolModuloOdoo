# -*- coding: utf-8 -*-

from odoo import fields, models


class FootballCreateMatchWizard(models.TransientModel):
    _name = "football.create.match.wizard"
    _description = "Wizard para crear partidos de fútbol base"

    team_id = fields.Many2one(
        comodel_name="football.team",
        string="Equipo",
        required=True,
    )
    opponent = fields.Char(string="Rival", required=True)
    match_date = fields.Datetime(string="Fecha y hora", required=True)
    field_name = fields.Char(string="Campo", required=True)
    match_type = fields.Selection(
        selection=[
            ("league", "Liga"),
            ("friendly", "Amistoso"),
            ("tournament", "Torneo"),
        ],
        string="Tipo de partido",
        default="league",
        required=True,
    )
    include_available_players = fields.Boolean(
        string="Incluir jugadores disponibles",
        help="Añade automáticamente a la convocatoria todos los jugadores disponibles del equipo.",
    )
    notes = fields.Text(string="Observaciones")

    def action_create_match(self):
        """Crea el partido y abre directamente su formulario."""
        self.ensure_one()

        player_ids = []
        if self.include_available_players:
            available_players = self.team_id.player_ids.filtered(lambda player: player.state == "available")
            player_ids = [(6, 0, available_players.ids)]

        match = self.env["football.match"].create(
            {
                "team_id": self.team_id.id,
                "opponent": self.opponent,
                "match_date": self.match_date,
                "field_name": self.field_name,
                "match_type": self.match_type,
                "state": "draft",
                "player_ids": player_ids,
                "notes": self.notes,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Partido creado",
            "res_model": "football.match",
            "view_mode": "form",
            "res_id": match.id,
            "target": "current",
        }

