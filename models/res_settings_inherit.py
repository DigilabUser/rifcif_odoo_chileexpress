# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    cotizador_key = fields.Char('Cotizador Subscription Key')
    coberturas_key = fields.Char('Coberturas Subscription Key')
    envios_key = fields.Char('Envios Subscription Key')


