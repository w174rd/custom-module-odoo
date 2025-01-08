from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'purchase.request'

    date = fields.Date(
        string="Tanggal Pengajuan",
        readonly=True
    )

    pr_number = fields.Char(
        string="Nomor PR", 
        readonly=True
    )
    submited_by = fields.Many2one(
        'hr.employee',
        string="Diajukan Oleh",
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1),
        readonly=True
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pr_validated', 'PR Validated'),
        ('rfq_created', 'RFQ Created'),
    ], string="Status", default="draft")

    is_readonly = fields.Boolean(default=False, compute="_compute_is_readonly")

    # Relation product
    product_ids = fields.One2many('product.request', 'parent_id')

    def action_set_submit(self):
        self.status = 'to_approve'
        for record in self:
            record.pr_number = self._generate_pr_number()
            # record.date = self._get_formatted_today_date()
            record.date = fields.Date.context_today(self)

    def _generate_pr_number(self):
        current_year = datetime.now().strftime('%y')
        current_month = datetime.now().strftime('%b').capitalize()
        
        sequence = self.env['ir.sequence'].next_by_code('purchase.request')
        
        return f"PR/{current_year}/{current_month}/{sequence}"
    
    def action_set_approve(self):
        self.status = 'approved'

    def action_set_reject(self):
        self.status = 'rejected'

    def action_print_out(self):
        return self.env.ref("purchase_request.action_print_out_purchase_request").report_action(self)
    
    def _compute_is_readonly(self):
        user = self.env.user
        if user.has_group('purchase_request.group_purchase_request_user') and not user.has_group('purchase_request.group_purchase_request_approver') and self.status != 'draft':
            self.is_readonly = True
        else:
            self.is_readonly = False




