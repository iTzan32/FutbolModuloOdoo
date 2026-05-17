# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FootballPlayer(models.Model):
    _name = "football.player"
    _description = "Jugador de fútbol base"
    _order = "team_id asc, jersey_number asc, surname asc, name asc"

    name = fields.Char(string="Nombre", required=True)
    surname = fields.Char(string="Apellidos", required=True)
    full_name = fields.Char(
        string="Nombre completo",
        compute="_compute_full_name",
        store=True,
    )
    dni = fields.Char(string="DNI")
    phone = fields.Char(string="Teléfono")
    birthdate = fields.Date(string="Fecha de nacimiento")
    age = fields.Integer(string="Edad", compute="_compute_age")
    photo = fields.Image(string="Foto")
    position = fields.Selection(
        selection=[
            ("goalkeeper", "Portero"),
            ("defender", "Defensa"),
            ("midfielder", "Centrocampista"),
            ("forward", "Delantero"),
        ],
        string="Posición",
        required=True,
    )
    jersey_number = fields.Integer(string="Dorsal", required=True)
    state = fields.Selection(
        selection=[
            ("available", "Disponible"),
            ("injured", "Lesionado"),
            ("suspended", "Sancionado"),
            ("inactive", "Baja"),
        ],
        string="Estado",
        default="available",
        required=True,
    )
    team_id = fields.Many2one(
        comodel_name="football.team",
        string="Equipo",
        required=True,
        ondelete="cascade",
    )

    @api.depends("name", "surname")
    def _compute_full_name(self):
        """Une nombre y apellidos para mostrar al jugador de forma clara."""
        for player in self:
            parts = [player.name or "", player.surname or ""]
            player.full_name = " ".join(part for part in parts if part).strip()

    @api.depends("birthdate")
    def _compute_age(self):
        """Calcula la edad usando la fecha actual del servidor de Odoo."""
        today = fields.Date.today()
        for player in self:
            player.age = relativedelta(today, player.birthdate).years if player.birthdate else 0

    @api.constrains("birthdate")
    def _check_birthdate(self):
        """Evita registrar jugadores con fecha de nacimiento futura."""
        today = fields.Date.today()
        for player in self:
            if player.birthdate and player.birthdate > today:
                raise ValidationError("La fecha de nacimiento no puede ser futura.")

    @api.constrains("jersey_number")
    def _check_jersey_number(self):
        """Un dorsal debe estar entre 1 y 99."""
        for player in self:
            if player.jersey_number < 1 or player.jersey_number > 99:
                raise ValidationError("El dorsal debe estar entre 1 y 99.")

