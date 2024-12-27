
from odoo import models, fields, api


class ProductInherit(models.Model):
    _name = 'product.request'
    _description = 'Product Request'

    parent_id = fields.Many2one('purchase.request', readonly=True)
    product = fields.Many2one('product.product', string="Product")
    qty_request = fields.Integer(string="Qty Request")
    qty_approved = fields.Integer(string="Qty Approved")
    user_state = fields.Char(readonly=True)

    @api.onchange('qty_approved')
    def _onchange_qty_approved(self):
        user_type = self.env.user.purchase_request_rule
        for record in self:
            if user_type == 'approver':
                record.user_state = 'approver'
            else:
                record.user_state = 'user'