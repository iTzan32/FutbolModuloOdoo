# -*- coding: utf-8 -*-

# fields y models permiten crear un asistente temporal en Odoo.
from odoo import fields, models


class FootballCreateMatchWizard(models.TransientModel):
    # Modelo temporal: sus datos se usan solo durante el asistente.
    _name = "football.create.match.wizard"
    # Descripción del wizard en Odoo.
    _description = "Wizard para crear partidos de fútbol base"

    # Equipo para el que se creará el partido.
    team_id = fields.Many2one(
        comodel_name="football.team",
        string="Equipo",
        required=True,
    )
    # Datos mínimos del nuevo partido.
    opponent = fields.Char(string="Rival", required=True)
    match_date = fields.Datetime(string="Fecha y hora", required=True)
    field_name = fields.Char(string="Campo", required=True)
    # Tipo de partido elegido desde el asistente.
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
    # Opción para añadir automáticamente la plantilla disponible.
    include_available_players = fields.Boolean(
        string="Incluir jugadores disponibles",
        help="Añade automáticamente a la convocatoria todos los jugadores disponibles del equipo.",
    )
    # Observaciones copiadas al partido creado.
    notes = fields.Text(string="Observaciones")

    def action_create_match(self):
        """Crea el partido y abre directamente su formulario."""
        self.ensure_one()

        # Por defecto no añade jugadores a la convocatoria.
        player_ids = []
        if self.include_available_players:
            # Filtra solo jugadores disponibles del equipo seleccionado.
            available_players = self.team_id.player_ids.filtered(lambda player: player.state == "available")
            # Comando many2many para reemplazar la convocatoria por esos jugadores.
            player_ids = [(6, 0, available_players.ids)]

        # Crea el partido real con los datos introducidos en el wizard.
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

        # Devuelve una acción para abrir el formulario del partido creado.
        return {
            "type": "ir.actions.act_window",
            "name": "Partido creado",
            "res_model": "football.match",
            "view_mode": "form",
            "res_id": match.id,
            "target": "current",
        }
