import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):

    _inherit = "sale.order"

    def get_wizard(self):
        return{
            'name': ('Cotización ChileExpress'),
            'type': 'ir.actions.act_window',
            'res_model': 'cotiza.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'peso': self.suma, 'res_id': self.id} 
        }
    
    def get_cchile(self):
        return{
            'name': ('Cotización CorreosChile'),
            'type': 'ir.actions.act_window',
            'res_model': 'cchile.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'x_peso': self.suma, 'res_id': self.id} 
        }

    def get_blue(self):
        return{
            'name': ('Cotización BlueExpress'),
            'type': 'ir.actions.act_window',
            'res_model': 'blue.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'res_id': self.id} 
        }

