# -*- coding: utf-8 -*-
from email.policy import default
from multiprocessing import context
import requests
import json
import logging
import xmltodict
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class BlueWizard(models.TransientModel):

    _name = "blue.wizard"

    comuna_orig_id = fields.Many2one('res.comuna.cchile', 'Comuna de Origen')
    comuna_dest_id = fields.Many2one('res.comuna.cchile', 'Comuna de Destino')
    precio = fields.Float('Precio')

    def cotizar_blue(self):
        url = 'https://bx-tracking.bluex.cl/bx-pricing/v1'
        header = {
            'BX-TOKEN':'012189d840019c5295517203a8ddb567',
            'BX-USERCODE':'51274',
            'BX-CLIENT-ACCOUNT':'USREDUALBER'
        }
        myobj = {
            "from": {
                "country": "CL",
                "district": "SCL"
            },
            "to": {
                "country": "CL",
                "state": 13,
                "district": "SCL"
            },
            "serviceType": "EX",
            "serviciosComplementarios": "",
            "datosProducto": {
                "producto": "P",
                "familiaProducto": "PAQU",
                "largo": "10.0",
                "ancho": "5.0",
                "alto": "7.5",
                "pesoFisico": "1.0",
                "cantidadPiezas": 1,
                "unidades": 1
            }
        }
        y = requests.post(url, json = myobj, headers=header)
        response = json.loads(y.text)
        _logger.info('RESPONSEEEEEEEEEEEEEE%s',response)

    def close_blue(self):
        pass