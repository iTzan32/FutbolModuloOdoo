# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request


class FootballMatchController(http.Controller):
    """Controller público para consultar el estado de un partido por código."""

    @http.route(
        "/club_futbol/partido/<string:codigo>/estado",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def match_status(self, codigo, **kwargs):
        match = request.env["football.match"].sudo().search([("code", "=", codigo)], limit=1)

        if not match:
            payload = {
                "found": False,
                "code": codigo,
                "message": "No existe ningún partido con ese código.",
            }
            return request.make_response(
                json.dumps(payload, ensure_ascii=False),
                headers=[("Content-Type", "application/json; charset=utf-8")],
            )

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
