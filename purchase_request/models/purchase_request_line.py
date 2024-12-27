
from odoo import models, fields

class PurchaseRequestLine(models.Model):
    _name= 'purchase.request.line'
    _description = 'Purchase Request Line'

    status = fields.Selection([
        ('pr_validated', 'PR Validated'),
        ('rfq_created', 'RFQ Created'),
    ], string='Status', default='pr_validated')

    purchase_request_id = fields.Many2one(
        comodel_name='purchase.request',
        string='Purchase Request',
        ondelete='cascade'
    )