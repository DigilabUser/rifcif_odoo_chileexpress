# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class ResComuna(models.Model):

    _name = "res.comuna"

    name = fields.Char('Nombre')
    region = fields.Char('Region')
    comuna_id = fields.Char('ID de la Comuna')