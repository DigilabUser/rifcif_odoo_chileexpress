# -*- coding: utf-8 -*-
from email.policy import default
from multiprocessing import context
import requests
import json
import logging
import xmltodict
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class CchileWizard(models.TransientModel):

    _name = "cchile.wizard"

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


    comuna_origen_id = fields.Many2one('res.comuna.cchile', 'Comuna de Origen', default=_get_default_origen)
    comuna_destino_id = fields.Many2one('res.comuna.cchile', 'Comuna de Destino', default=_get_default_destino)
    x_peso = fields.Float('Peso', default=_get_default_x_peso)
    x_volumen = fields.Float('Volumen')
    price = fields.Float('Precio', default=_get_default_price)

    def cotizar(self):
        url="http://b2b.correos.cl/ServicioTarificacionCEPEmpresasExterno/cch/ws/tarificacionCEP/externo/implementacion/ExternoTarificacion.asmx?WSDL"
        headers = {'content-type': 'text/xml'}
        body = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:consultaCobertura>
                <tem:usuario>LIBRERIAEDUARDOALBERS</tem:usuario>
                <tem:contrasena>c458ff3b3ecd3fc6462bd1339174e397</tem:contrasena>
                <tem:consultaCobertura>
                    <tem:ComunaRemitente>{}</tem:ComunaRemitente>
                    <tem:PaisRemitente>056</tem:PaisRemitente>
                    <tem:CodigoPostalRemitente></tem:CodigoPostalRemitente>
                    <tem:ComunaDestino>{}</tem:ComunaDestino>
                    <tem:PaisDestinatario>056</tem:PaisDestinatario>
                    <tem:CodigoPostalDestinatario></tem:CodigoPostalDestinatario>
                    <tem:ImporteReembolso>0</tem:ImporteReembolso>
                    <tem:ImporteValorAsegurado>0</tem:ImporteValorAsegurado>
                    <tem:NumeroTotalPieza>1</tem:NumeroTotalPieza>
                    <tem:TipoPortes>P</tem:TipoPortes>
                    <tem:Kilos>{}</tem:Kilos>
                    <tem:Volumen>0</tem:Volumen>
                </tem:consultaCobertura>
            </tem:consultaCobertura>
        </soapenv:Body>
        </soapenv:Envelope>

        """
        x = requests.post(url,data=body.format(self.comuna_origen_id.name,self.comuna_destino_id.name,self.x_peso),headers=headers)
        obj = xmltodict.parse(x.text)
        obj_json = json.dumps(obj)
        response = json.loads(obj_json)
        ans = response["soap:Envelope"]["soap:Body"]["consultaCoberturaResponse"]["consultaCoberturaResult"]["ServicioTO"]
        precio_flete = 0 
        for what in ans:
            if what["CodigoServicio"] == "24":
                precio_flete = what["TotalTasacion"]["Total"]
        ctx={}
        ctx.update({
            'price': precio_flete,
            'comuna_origen': self.comuna_origen_id.id,
            'comuna_destino': self.comuna_destino_id.id
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cchile.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }

        _logger.info('RESPONSEEEEEEEEEEEEEE%s',response)
        _logger.info('ANSSSSSSSSSSSSSSSS%s',ans)

    def close(self):
        s2_order = self.env['sale.order'].search([('id','=',self._get_default_id())])
        s2_order.write({'correoschile_price':self.price})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self._get_default_id(),
            'type': 'ir.actions.act_window',
            'target': 'current',
            #'context': {'precio': self.delivery_price}
        }