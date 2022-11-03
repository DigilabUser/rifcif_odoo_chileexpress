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
        _logger.info('VARRRRRRRRRRRRR%s',var)
        return self._context.get('delivery_price',"")
    
    # def _get_default_origen(self):
    #     comuna = self._context.get('origin_comuna',"")
    #     _logger.info('COMUNAAAAAAAAAA%s',comuna)
    #     return comuna

    # def _get_default_destino(self):
    #     destino = self._context.get('destination_comuna',"")
    #     _logger.info('DESCOMUNAAAAAAAAAA%s',destino)
    #     return self._context.get('destination_comuna',"")

    weight = fields.Char('Peso')
    height = fields.Char('Altura')
    width = fields.Char('Ancho')
    length = fields.Char('Largo')
    origin_comuna = fields.Many2one('res.comuna','Comuna de Origen')
    destination_comuna = fields.Many2one('res.comuna','Comuna de Destino')
    delivery_price = fields.Float('Precio de Envío', default=_get_default_char)
    origin_region = fields.Selection([
        ('TARAPACA', 'Tarapaca'),
        ('ANTOFAGASTA', 'Antofagasta'),
        ('ATACAMA', 'Atacama'),
        ('COQUIMBO', 'Coquimbo'),
        ('VALPARAISO', 'Valparaiso'),
        ('LIBERTADOR-GRAL-BERNARDO-O-HIGGINS','Libertador Gral Bernardo O HIGGINS'),
        ('MAULE','Maule'),
        ('BIOBIO','Biobio'),
        ('ARAUCANIA','Araucania'),
        ('METROPOLITANA-DE-SANTIAGO','Metropolitana de Santiago'),
        ('LOS-LAGOS','Los Lagos'),
        ('AISEN-DEL-GRAL-C-IBANEZ-DEL-CAMPO','Aysén del General Carlos Ibáñez del Campo'),
        ('MAGALLANES-Y-LA-ANTARTICA-CHILENA','Magallanes y la Antartica Chilena'),
        ('LOS-RIOS','Los Rios'),
        ('ARICA-Y-PARINACOTA','Arica y Parinacota'),
        ('NUBLE','Nuble')
    ], string='Region de Origen')
    destination_region = fields.Selection([
        ('TARAPACA', 'Tarapaca'),
        ('ANTOFAGASTA', 'Antofagasta'),
        ('ATACAMA', 'Atacama'),
        ('COQUIMBO', 'Coquimbo'),
        ('VALPARAISO', 'Valparaiso'),
        ('LIBERTADOR-GRAL-BERNARDO-O-HIGGINS','Libertador Gral Bernardo O HIGGINS'),
        ('MAULE','Maule'),
        ('BIOBIO','Biobio'),
        ('ARAUCANIA','Araucania'),
        ('METROPOLITANA-DE-SANTIAGO','Metropolitana de Santiago'),
        ('LOS-LAGOS','Los Lagos'),
        ('AISEN-DEL-GRAL-C-IBANEZ-DEL-CAMPO','Aysén del General Carlos Ibáñez del Campo'),
        ('MAGALLANES-Y-LA-ANTARTICA-CHILENA','Magallanes y la Antartica Chilena'),
        ('LOS-RIOS','Los Rios'),
        ('ARICA-Y-PARINACOTA','Arica y Parinacota'),
        ('NUBLE','Nuble')
    ], string='Region de Destino')

    def get_cotizacion(self):
        url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/business'
        header = {
            'Content-Type':'application/json',
            'Cache-Control':'no-cache',
            'Ocp-Apim-Subscription-Key':'f25fbe75153b4f8e908e11fb5c958a1d'
        }
        myobj = {
            "originCountyCode": self.origin_comuna.comuna_id,
            "destinationCountyCode": self.destination_comuna.comuna_id,
            "package": {
                "weight": "16",
                "height": "1",
                "width": "1",
                "length": "1"
            },
            "productType": 3,
            "contentType": 1,
            "declaredWorth": "2333",
            "deliveryTime": 0,
            "customerCardNumber": "0"
        }
        _logger.info('MYOBJJJJJJJJJJJJJJJJJJJJJJJJJJ%s',myobj)
        x = requests.post(url, json = myobj, headers=header)
        response = json.loads(x.text)
        _logger.info('RESPONSEEEEEEEEEEEEEEEEEEEEEEEEEEE%s',response)
        prueba = response['data']['courierServiceOptions'][0]['serviceValue']
        #context = "{'delivery_price':'"+prueba+"','origin_comuna':'"+self.origin_comuna+"','destination_comuna':'"+self.destination_comuna+"'}"
        context= "{'delivery_price':"+prueba+"}"
        #context = "{'origin_comuna':'"+self.origin_comuna+"'}"
        _logger.info('PrueBAAAAAAAAAAAAAAAAAAAAAAAAAAAA%s',context)
        #self.delivery_price = float(response['data']['courierServiceOptions'][0]['serviceValue'])
        #_logger.info('POSSTTTTTTTTTTTTTTT%s',response['data']['courierServiceOptions'][0]['serviceValue'])
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotiza.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }
        # url = 'https://testservices.wschilexpress.com/georeference/api/v1.0/regions'
        # data = requests.get(url)
        # data = data.json()
        # regions = data['regions']
        # origin_regions = self.origin_region
        # origin_region_id = ''
        # for region in regions:
        #     if region['regionName'].replace(' ','-') == origin_regions:
        #         origin_region_id = region['regionId']
        # _logger.info('REGIOOOOOOOOOOOOOOOOOOOOOOOOON%s',origin_region_id)
        # url = 'https://testservices.wschilexpress.com/georeference/api/v1.0/coverage-areas?RegionCode={origin_region_id}&type=0'
        # data = requests.get(url)
        # data = data.json()
        # for item in data:
        #     _logger.info('ITEEEMMMMMMMMMMMMMM%s',item)
        
    # @api.onchange('origin_region')
    # def _get_selection(self):
    #     lst = []
    #     lst.append(('1','value1'))
    #     lst.append(('2','value2'))
    #     lst.append(('3','value3'))
    #     return lst

    # origin_comuna = fields.Selection(_get_selection, string='Comuna de origen')
    
            
