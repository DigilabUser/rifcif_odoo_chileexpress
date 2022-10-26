# -*- coding: utf-8 -*-
import requests
import json
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class CotizaWizard(models.TransientModel):

    _name = "cotiza.wizard"

    weight = fields.Char('Peso')
    height = fields.Char('Altura')
    width = fields.Char('Ancho')
    length = fields.Char('Largo')
    delivery_price = fields.Char('Precio de Envío')
    city_id = fields.Many2one('res.city', 'Comuna de Origen')
    city2_id = fields.Many2one('res.city', 'Comuna de Destino')
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
        url = 'https://testservices.wschilexpress.com/georeference/api/v1.0/regions'
        data = requests.get(url)
        data = data.json()
        regions = data['regions']
        origin_regions = self.origin_region
        origin_region_id = ''
        for region in regions:
            if region['regionName'].replace(' ','-') == origin_regions:
                origin_region_id = region['regionId']
        _logger.info('REGIOOOOOOOOOOOOOOOOOOOOOOOOON%s',origin_region_id)
        url = 'https://testservices.wschilexpress.com/georeference/api/v1.0/coverage-areas?RegionCode={origin_region_id}&type=0'
        data = requests.get(url)
        data = data.json()
        for item in data:
            _logger.info('ITEEEMMMMMMMMMMMMMM%s',item)
            
