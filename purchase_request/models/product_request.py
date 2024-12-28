
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

    relation_pr_line_status = fields.Selection(
        related='parent_id.relation_pr_line_status', 
        string="Status"
    )

    # nomor_pr = fields.Char(
    #     related='parent_id.nomor_pr', 
    #     string="Nomor PR"
    # )
    # diajukan_oleh = fields.Many2one(
    #     related='parent_id.diajukan_oleh', 
    #     string="Diajukan oleh"
    # )

    def action_create_rfq(self):
        # self.relation_pr_line_status = 'rfq_created'
        for record in self:
            if record.parent_id:
                for relation_pr_line in record.parent_id.purchase_request_line_id:
                    relation_pr_line.status = 'rfq_created'


    @api.onchange('qty_approved')
    def _onchange_qty_approved(self):
        user_type = self.env.user.purchase_request_rule
        for record in self:
            if user_type == 'approver':
                record.user_state = 'approver'
            else:
                record.user_state = 'user'