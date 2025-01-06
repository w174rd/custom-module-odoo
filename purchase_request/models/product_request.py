
from odoo import models, fields, api


class ProductInherit(models.Model):
    _name = 'product.request'
    _description = 'Product Request'
    
    product = fields.Many2one('product.product', string="Product")
    qty_request = fields.Integer(string="Qty Request")
    qty_approved = fields.Integer(string="Qty Approved")
    user_state = fields.Char(readonly=True)

    # Relation Purchase Request
    parent_id = fields.Many2one('purchase.request', readonly=True)
    wizard_id = fields.Many2one('wizard.rfq', readonly=True)

    relation_pr_nomor_pr = fields.Char(
        related='parent_id.nomor_pr', 
        string="Nomor PR"
    )

    relation_pr_diajukan_oleh = fields.Many2one(
        related='parent_id.diajukan_oleh', 
        string="Diajukan oleh"
    )

    relation_pr_status = fields.Selection(
        related='parent_id.status', 
        string="Status"
    )

    custom_status_display = fields.Char(
        compute="_compute_status_display",
        store=False
    )

    def _compute_status_display(self):
        for record in self:
            if record.relation_pr_status == 'approved':
                record.custom_status_display = 'PR Validated'
            elif record.relation_pr_status == 'rfq_created':
                record.custom_status_display = 'RFQ Created'
            else:
                record.custom_status_display = False


    def action_create_rfq(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create RFQ',
            'res_model': 'wizard.rfq',
            'view_mode': 'form',
            'target': 'new',
        }