
from odoo import models, fields

class PurchaseRequestLine(models.Model):
    _name= 'purchase.request.line'
    _description = 'Purchase Request Line'

    nomor_pr = fields.Char(string="Nomor PR")
    diajukan_oleh = fields.Char(string="Diajukan Oleh")
    product = fields.Char(string="Product")
    quantity = fields.Char(string="Quantity")
    status = fields.Selection([
        ('PR Validated', 'PR Validated'),
        ('RFQ Created', 'Diajukan oleh'),
    ], string='Status', default='PR Validated')