# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FootballMatch(models.Model):
    _name = "football.match"
    _description = "Partido de fútbol base"
    _order = "match_date asc, state asc, code asc"

    code = fields.Char(
        string="Código",
        required=True,
        copy=False,
        readonly=True,
        default="Nuevo",
    )
    team_id = fields.Many2one(
        comodel_name="football.team",
        string="Equipo",
        required=True,
        ondelete="cascade",
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
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("played", "Jugado"),
            ("cancelled", "Cancelado"),
        ],
        string="Estado",
        default="draft",
        required=True,
    )
    player_ids = fields.Many2many(
        comodel_name="football.player",
        relation="football_match_player_rel",
        column1="match_id",
        column2="player_id",
        string="Convocatoria",
    )
    goals_for = fields.Integer(string="Goles a favor")
    goals_against = fields.Integer(string="Goles en contra")
    result_label = fields.Char(
        string="Resultado",
        compute="_compute_result_label",
        store=True,
    )
    total_goals = fields.Integer(
        string="Total de goles",
        compute="_compute_total_goals",
        store=True,
    )
    notes = fields.Text(string="Observaciones")

    _sql_constraints = [
        ("code_unique", "unique(code)", "El código del partido debe ser único."),
        ("goals_for_positive", "CHECK(goals_for >= 0)", "Los goles a favor no pueden ser negativos."),
        ("goals_against_positive", "CHECK(goals_against >= 0)", "Los goles en contra no pueden ser negativos."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """Asigna automáticamente el código del partido mediante ir.sequence."""
        for vals in vals_list:
            if vals.get("code", "Nuevo") == "Nuevo":
                vals["code"] = self.env["ir.sequence"].next_by_code("football.match") or "Nuevo"
        return super().create(vals_list)

    @api.depends("state", "goals_for", "goals_against")
    def _compute_result_label(self):
        """Muestra Victoria, Empate, Derrota o Pendiente según el estado y los goles."""
        for match in self:
            if match.state != "played":
                match.result_label = "Pendiente"
            elif match.goals_for > match.goals_against:
                match.result_label = "Victoria"
            elif match.goals_for == match.goals_against:
                match.result_label = "Empate"
            else:
                match.result_label = "Derrota"

    @api.depends("goals_for", "goals_against")
    def _compute_total_goals(self):
        """Calcula la suma de goles de ambos equipos."""
        for match in self:
            match.total_goals = match.goals_for + match.goals_against

    @api.constrains("state", "match_date")
    def _check_match_date(self):
        """No se pueden dejar partidos confirmados con una fecha pasada."""
        now = fields.Datetime.now()
        for match in self:
            if match.state == "confirmed" and match.match_date and match.match_date < now:
                raise ValidationError("No se puede confirmar un partido con fecha pasada.")

    @api.constrains("team_id", "player_ids")
    def _check_players_belong_to_team(self):
        """Todos los convocados deben pertenecer al equipo del partido."""
        for match in self:
            wrong_players = match.player_ids.filtered(lambda player: player.team_id != match.team_id)
            if wrong_players:
                names = ", ".join(wrong_players.mapped("full_name"))
                raise ValidationError(
                    "Hay jugadores convocados que no pertenecen al equipo del partido: %s." % names
                )

    @api.constrains("player_ids")
    def _check_unavailable_players(self):
        """Solo se pueden convocar jugadores disponibles."""
        for match in self:
            unavailable = match.player_ids.filtered(lambda player: player.state != "available")
            if unavailable:
                names = ", ".join(unavailable.mapped("full_name"))
                raise ValidationError(
                    "No se pueden convocar jugadores lesionados, sancionados o de baja: %s." % names
                )

    @api.constrains("team_id", "match_date", "state")
    def _check_team_busy(self):
        """Evita dos partidos confirmados del mismo equipo a la misma hora."""
        for match in self:
            if match.state != "confirmed" or not match.team_id or not match.match_date:
                continue
            busy_match = self.search(
                [
                    ("id", "!=", match.id),
                    ("team_id", "=", match.team_id.id),
                    ("match_date", "=", match.match_date),
                    ("state", "=", "confirmed"),
                ],
                limit=1,
            )
            if busy_match:
                raise ValidationError(
                    "El equipo ya tiene otro partido confirmado en la misma fecha y hora."
                )

    def action_confirm(self):
        for match in self:
            match.state = "confirmed"

    def action_set_draft(self):
        for match in self:
            match.state = "draft"

    def action_mark_played(self):
        for match in self:
            match.state = "played"

    def action_cancel(self):
        for match in self:
            match.state = "cancelled"

    def action_print_pending_matches(self):
        """Permite lanzar el informe desde un partido usando su equipo."""
        self.ensure_one()
        return self.env.ref("club_futbol_base.action_report_pending_matches").report_action(self.team_id)

