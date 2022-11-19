# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class ResRegion(models.Model):

    _name = "res.region"

    name = fields.Char('Nombre')
    region_id = fields.Char('Region ID')