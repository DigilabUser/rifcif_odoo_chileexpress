# -*- coding: utf-8 -*-
from email.policy import default
from multiprocessing import context
import requests
import json
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class CotizaWizard(models.TransientModel):

    _name = "cotiza.wizard"


    def _get_default_char(self):
        var = self._context.get('delivery_price',"")
        return var
    
    def _get_default_origen(self):
        comuna = self._context.get('origin_comuna',"")
        return comuna

    def _get_default_destino(self):
        destino = self._context.get('destination_comuna',"")
        return destino

    def _get_default_peso(self):
        peso = self._context.get('peso',"")
        return peso
    
    def _get_default_id(self):
        res = self._context.get('res_id',"")
        return res

    weight = fields.Char('Peso', default=_get_default_peso)
    height = fields.Char('Altura')
    width = fields.Char('Ancho')
    length = fields.Char('Largo')
    origin_comuna_id = fields.Many2one('res.comuna','Comuna de Origen',default=_get_default_origen)
    destination_comuna_id = fields.Many2one('res.comuna','Comuna de Destino',default=_get_default_destino)
    delivery_price = fields.Float('Precio de Envío', default=_get_default_char)
    origin_region_id = fields.Many2one('res.region', string='Region de Origen')
    destination_region_id = fields.Many2one('res.region', string='Region de Destino')

    def close_wizard(self):
        s_order = self.env['sale.order'].search([('id','=',self._get_default_id())])
        s_order.write({'chileexpress_price':self.delivery_price})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self._get_default_id(),
            'type': 'ir.actions.act_window',
            'target': 'current',
            #'context': {'precio': self.delivery_price}
        }

    def get_cotizacion(self):
        url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/business'
        header = {
            'Content-Type':'application/json',
            'Cache-Control':'no-cache',
            'Ocp-Apim-Subscription-Key':'f25fbe75153b4f8e908e11fb5c958a1d'
        }
        myobj = {
            "originCountyCode": self.origin_comuna_id.comuna_id,
            "destinationCountyCode": self.destination_comuna_id.comuna_id,
            "package": {
                "weight": self.weight,
                "height": self.height,
                "width": self.width,
                "length": self.length
            },
            "productType": 3,
            "contentType": 1,
            "declaredWorth": "2333",
            "deliveryTime": 0,
            "customerCardNumber": "0"
        }
        x = requests.post(url, json = myobj, headers=header)
        response = json.loads(x.text)
        prueba = response['data']['courierServiceOptions'][0]['serviceValue']
        ctx={}
        ctx.update({
            'delivery_price': prueba,
            'origin_comuna': self.origin_comuna_id.id,
            'destination_comuna': self.destination_comuna_id.id
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotiza.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }
    
            
