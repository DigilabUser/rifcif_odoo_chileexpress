# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class ResComunaCchile(models.Model):

    _name = "res.comuna.cchile"

    name = fields.Char('Nombre')