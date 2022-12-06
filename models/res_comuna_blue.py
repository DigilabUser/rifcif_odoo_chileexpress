# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class ResComunaBlue(models.Model):

    _name = "res.comuna.blue"

    name = fields.Char('Nombre')
    codigo_estado = fields.Char('Código Estado')
    codigo_distrito = fields.Char('Código Distrito')