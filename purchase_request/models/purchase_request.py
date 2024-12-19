from odoo import models, fields

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'purchase.request'

    name = fields.Char(string="Name")