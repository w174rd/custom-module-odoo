
from odoo import models, fields, api


class ProductInherit(models.Model):
    _name = 'product.request'

    parent_id = fields.Many2one('purchase.request', readonly=True,
        invisible=True)
    product = fields.Many2one(
        'product.product', 
        string = "Product",
    )
    qty_request = fields.Integer(string="Qty Request")
    qty_approved = fields.Integer(string="Qty Approved")
    is_approver = fields.Boolean(string="Is Approver", compute="_compute_is_approver")

# @api.depends('user_id')  # Jika ingin tergantung pada user tertentu
def _compute_is_approver(self):
    for record in self:
        has_group = self.env.user.has_group('purchase_request.group_purchase_request_user')
        print("=============================")
        print(has_group)
        record.is_approver = has_group