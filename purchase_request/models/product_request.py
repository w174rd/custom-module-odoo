
from odoo import models, fields


class ProductInherit(models.Model):
    _name = 'product.request'

    parent_id = fields.Many2one('purchase.request', readonly=True,
        invisible=True)
    product = fields.Many2one(
        'product.product', 
        string = "Product",
    )
    qtyRequest = fields.Integer(string="Qty Request")
    qtyApproved = fields.Integer(string="Qty Approved")