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

    def _get_default_largo(self):
        largo = self._context.get('largo',"")
        return largo
    
    def _get_default_alto(self):
        alt = self._context.get('alto',"")
        return alt

    def _get_default_ancho(self):
        anch = self._context.get('ancho',"")
        return anch

    def _get_default_price(self):
        var = self._context.get('price',"")
        _logger.info('VAAAAAAAAAR%s',var)
        return var

    def _get_default_x_peso(self):
        peso = self._context.get('x_peso',"")
        return peso
    
    def _get_default_id(self):
        res = self._context.get('res_id',"")
        _logger.info('REEEEEEEEEEES%s',res)
        return res

    def _get_default_origen(self):
        origen = self._context.get('comuna_origen',"")
        return origen

    def _get_default_destino(self):
        destino = self._context.get('comuna_destino',"")
        return destino


    comuna_orig_id = fields.Many2one('res.comuna.blue', 'Comuna de Origen', default=_get_default_origen)
    comuna_dest_id = fields.Many2one('res.comuna.blue', 'Comuna de Destino', default=_get_default_destino)
    precio = fields.Float('Precio', default=_get_default_price)
    x_peso = fields.Float('Peso', default=_get_default_x_peso)
    largo = fields.Float('Largo', default=_get_default_largo)
    ancho = fields.Float('Ancho', default=_get_default_ancho)
    alto = fields.Float('Alto', default=_get_default_alto)


    def cotizar_blue(self):
        url = 'https://bx-tracking.bluex.cl/bx-pricing/v1'
        header = {
            'BX-TOKEN':'012189d840019c5295517203a8ddb567',
            'BX-USERCODE':'51274',
            'BX-CLIENT_ACCOUNT':'83171800-1-8'
        }
        myobj = {
                "from": {
                    "country": "CL",
                    "district": self.comuna_orig_id.codigo_distrito
                },
                "to": {
                    "country": "CL",
                    "state": self.comuna_dest_id.codigo_estado,
                    "district": self.comuna_dest_id.codigo_distrito
                },
                "serviceType": "EX",
                "serviciosComplementarios": None,
                "datosProducto": {
                    "producto": "P",
                    "familiaProducto": "PAQU",
                    "largo": self.largo,
                    "ancho": self.ancho,
                    "alto": self.alto,
                    "pesoFisico": self.x_peso,
                    "cantidadPiezas": 1,
                    "unidades": 1
                    }
                }
        y = requests.post(url, json = myobj, headers=header)
        response = json.loads(y.text)
        _logger.info('RESPONSEEEEEEEEEEEEEE%s',response)
        precio_flete = response['data']['flete']

        ctx={}
        ctx.update({    
            'price': precio_flete,
            'comuna_origen': self.comuna_orig_id.id,
            'comuna_destino': self.comuna_dest_id.id,
            'x_peso': self.x_peso,
            'ancho': self.ancho,
            'alto': self.alto,
            'largo': self.alto
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'blue.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }


    def close_blue(self):
        s3_order = self.env['sale.order'].search([('id','=',self._get_default_id())])
        s3_order.write({'blueexpress_price':self.precio})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self._get_default_id(),
            'type': 'ir.actions.act_window',
            'target': 'current',
            #'context': {'precio': self.delivery_price}
        }

