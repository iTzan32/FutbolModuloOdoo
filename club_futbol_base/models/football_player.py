# -*- coding: utf-8 -*-

# relativedelta calcula años completos entre dos fechas.
from dateutil.relativedelta import relativedelta

# api, fields y models son las piezas base para crear modelos en Odoo.
from odoo import api, fields, models
# ValidationError muestra errores de validación al usuario.
from odoo.exceptions import ValidationError


class FootballPlayer(models.Model):
    # Nombre técnico del modelo en la base de datos de Odoo.
    _name = "football.player"
    # Descripción legible que Odoo muestra en permisos y metadatos.
    _description = "Jugador de fútbol base"
    # Orden por defecto al listar jugadores.
    _order = "team_id asc, jersey_number asc, surname asc, name asc"

    # Datos personales básicos del jugador.
    name = fields.Char(string="Nombre", required=True)
    surname = fields.Char(string="Apellidos", required=True)
    # Campo calculado para mostrar nombre y apellidos juntos.
    full_name = fields.Char(
        string="Nombre completo",
        compute="_compute_full_name",
        store=True,
    )
    # Datos de contacto e identificación.
    dni = fields.Char(string="DNI")
    phone = fields.Char(string="Teléfono")
    # Fecha de nacimiento usada para calcular la edad.
    birthdate = fields.Date(string="Fecha de nacimiento")
    age = fields.Integer(string="Edad", compute="_compute_age")
    # Imagen que Odoo renderiza como foto del jugador.
    photo = fields.Image(string="Foto")
    # Posición deportiva elegida entre valores cerrados.
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
    # Número de camiseta del jugador.
    jersey_number = fields.Integer(string="Dorsal", required=True)
    # Estado deportivo usado para saber si puede ser convocado.
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
    # Relación con el equipo al que pertenece el jugador.
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
            # Evita valores vacíos antes de unir el texto.
            parts = [player.name or "", player.surname or ""]
            player.full_name = " ".join(part for part in parts if part).strip()

    @api.depends("birthdate")
    def _compute_age(self):
        """Calcula la edad usando la fecha actual del servidor de Odoo."""
        today = fields.Date.today()
        for player in self:
            # Si no hay fecha de nacimiento, se muestra edad 0.
            player.age = relativedelta(today, player.birthdate).years if player.birthdate else 0

    @api.constrains("birthdate")
    def _check_birthdate(self):
        """Evita registrar jugadores con fecha de nacimiento futura."""
        today = fields.Date.today()
        for player in self:
            # Bloquea fechas imposibles antes de guardar.
            if player.birthdate and player.birthdate > today:
                raise ValidationError("La fecha de nacimiento no puede ser futura.")

    @api.constrains("jersey_number")
    def _check_jersey_number(self):
        """Un dorsal debe estar entre 1 y 99."""
        for player in self:
            # Limita el dorsal al rango habitual de camisetas.
            if player.jersey_number < 1 or player.jersey_number > 99:
                raise ValidationError("El dorsal debe estar entre 1 y 99.")
