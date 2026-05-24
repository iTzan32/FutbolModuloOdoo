# -*- coding: utf-8 -*-

# api, fields y models permiten definir el modelo y sus reglas.
from odoo import api, fields, models
# ValidationError se usa para frenar guardados no válidos.
from odoo.exceptions import ValidationError


class FootballMatch(models.Model):
    # Nombre técnico del modelo de partidos.
    _name = "football.match"
    # Descripción legible del modelo.
    _description = "Partido de fútbol base"
    # Orden cronológico por defecto en listados.
    _order = "match_date asc, state asc, code asc"

    # Código único que se rellena automáticamente con una secuencia.
    code = fields.Char(
        string="Código",
        required=True,
        copy=False,
        readonly=True,
        default="Nuevo",
    )
    # Equipo propio que disputa el partido.
    team_id = fields.Many2one(
        comodel_name="football.team",
        string="Equipo",
        required=True,
        ondelete="cascade",
    )
    # Rival, fecha y campo son los datos principales del encuentro.
    opponent = fields.Char(string="Rival", required=True)
    match_date = fields.Datetime(string="Fecha y hora", required=True)
    field_name = fields.Char(string="Campo", required=True)
    # Tipo de partido para clasificar liga, amistoso o torneo.
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
    # Flujo de estado del partido dentro de la gestión.
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
    # Jugadores convocados para este partido.
    player_ids = fields.Many2many(
        comodel_name="football.player",
        relation="football_match_player_rel",
        column1="match_id",
        column2="player_id",
        string="Convocatoria",
    )
    # Marcador del partido.
    goals_for = fields.Integer(string="Goles a favor")
    goals_against = fields.Integer(string="Goles en contra")
    # Texto calculado del resultado final.
    result_label = fields.Char(
        string="Resultado",
        compute="_compute_result_label",
        store=True,
    )
    # Total de goles del encuentro.
    total_goals = fields.Integer(
        string="Total de goles",
        compute="_compute_total_goals",
        store=True,
    )
    # Campo libre para comentarios internos.
    notes = fields.Text(string="Observaciones")

    # Reglas SQL que protegen datos duplicados o negativos.
    _sql_constraints = [
        ("code_unique", "unique(code)", "El código del partido debe ser único."),
        ("goals_for_positive", "CHECK(goals_for >= 0)", "Los goles a favor no pueden ser negativos."),
        ("goals_against_positive", "CHECK(goals_against >= 0)", "Los goles en contra no pueden ser negativos."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """Asigna automáticamente el código del partido mediante ir.sequence."""
        for vals in vals_list:
            # Solo genera código si el usuario no ha indicado uno.
            if vals.get("code", "Nuevo") == "Nuevo":
                vals["code"] = self.env["ir.sequence"].next_by_code("football.match") or "Nuevo"
        return super().create(vals_list)

    @api.depends("state", "goals_for", "goals_against")
    def _compute_result_label(self):
        """Muestra Victoria, Empate, Derrota o Pendiente según el estado y los goles."""
        for match in self:
            # Antes de jugarse, el resultado se considera pendiente.
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
            # Suma ambos marcadores para análisis y listados.
            match.total_goals = match.goals_for + match.goals_against

    @api.constrains("state", "match_date")
    def _check_match_date(self):
        """No se pueden dejar partidos confirmados con una fecha pasada."""
        now = fields.Datetime.now()
        for match in self:
            # Solo valida la fecha si el partido está confirmado.
            if match.state == "confirmed" and match.match_date and match.match_date < now:
                raise ValidationError("No se puede confirmar un partido con fecha pasada.")

    @api.constrains("team_id", "player_ids")
    def _check_players_belong_to_team(self):
        """Todos los convocados deben pertenecer al equipo del partido."""
        for match in self:
            # Localiza jugadores de otros equipos dentro de la convocatoria.
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
            # Busca lesionados, sancionados o bajas entre los convocados.
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
            # Ignora borradores, cancelados o registros incompletos.
            if match.state != "confirmed" or not match.team_id or not match.match_date:
                continue
            # Busca otro partido confirmado que choque exactamente en fecha y hora.
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
        """Cambia el partido a confirmado."""
        for match in self:
            match.state = "confirmed"

    def action_set_draft(self):
        """Devuelve el partido al estado borrador."""
        for match in self:
            match.state = "draft"

    def action_mark_played(self):
        """Marca el partido como jugado."""
        for match in self:
            match.state = "played"

    def action_cancel(self):
        """Cancela el partido."""
        for match in self:
            match.state = "cancelled"

    def action_print_pending_matches(self):
        """Permite lanzar el informe desde un partido usando su equipo."""
        self.ensure_one()
        return self.env.ref("club_futbol_base.action_report_pending_matches").report_action(self.team_id)
