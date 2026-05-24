# -*- coding: utf-8 -*-

# json convierte diccionarios Python en respuestas JSON.
import json

# http permite declarar rutas web en Odoo.
from odoo import http
# request da acceso al entorno y a la respuesta HTTP actual.
from odoo.http import request


class FootballMatchController(http.Controller):
    """Controller público para consultar el estado de un partido por código."""

    # Ruta pública que devuelve el estado de un partido en formato JSON.
    @http.route(
        "/club_futbol/partido/<string:codigo>/estado",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def match_status(self, codigo, **kwargs):
        # sudo permite consultar el partido aunque el visitante no haya iniciado sesión.
        match = request.env["football.match"].sudo().search([("code", "=", codigo)], limit=1)

        if not match:
            # Respuesta cuando no existe ningún partido con ese código.
            payload = {
                "found": False,
                "code": codigo,
                "message": "No existe ningún partido con ese código.",
            }
            return request.make_response(
                json.dumps(payload, ensure_ascii=False),
                headers=[("Content-Type", "application/json; charset=utf-8")],
            )

        # Respuesta con los datos públicos principales del partido.
        payload = {
            "found": True,
            "code": match.code,
            "team": match.team_id.name,
            "opponent": match.opponent,
            "match_date": match.match_date.isoformat() if match.match_date else False,
            "state": match.state,
            "result_label": match.result_label,
        }
        return request.make_response(
            json.dumps(payload, ensure_ascii=False),
            headers=[("Content-Type", "application/json; charset=utf-8")],
        )
