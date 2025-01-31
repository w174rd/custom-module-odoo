
from odoo import models, fields, api


class ProductInherit(models.Model):
    _name = 'product.request'
    _description = 'Product Request'
    
    product = fields.Many2one('product.product', string="Product")
    qty_request = fields.Integer(string="Qty Request")
    qty_approved = fields.Integer(string="Qty Approved")
    user_state = fields.Char(readonly=True)
    groups_id = fields.Selection([
        ('user', 'User'),
        ('approver', 'Approver'),
    ], default="user", compute="_compute_groups_id")
    price = fields.Float(string="Price", store=True, compute="_compute_product_price")


    # Relation Purchase Request
    parent_id = fields.Many2one('purchase.request', readonly=True)
    wizard_id = fields.Many2one('wizard.rfq', readonly=True)

    relation_pr_number_pr = fields.Char(
        related='parent_id.name', 
        string="Nomor PR"
    )

    relation_pr_submited_by = fields.Many2one(
        related='parent_id.submited_by', 
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

    def _compute_groups_id(self):
        user = self.env.user
        if user.has_group('purchase_request.group_purchase_request_user') and not user.has_group('purchase_request.group_purchase_request_approver'):
            self.groups_id = 'user'
        else:
            self.groups_id = 'approver'


    def action_create_rfq(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create RFQ',
            'res_model': 'wizard.rfq',
            'view_mode': 'form',
            'target': 'new',
        }
    
    @api.depends('product')
    def _compute_product_price(self):
        for record in self:
            record.write({'price': record.product.lst_price})