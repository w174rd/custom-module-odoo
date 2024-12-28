from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'purchase.request'

    tanggal_pengajuan = fields.Date(
        string="Tanggal Pengajuan",
        readonly=True
    )
    # created_by = fields.Many2one('res.users', default= lambda self : self.env.user.id)
    nomor_pr = fields.Char(
        string="Nomor PR", 
        readonly=True
    )
    diajukan_oleh = fields.Many2one(
        'hr.employee',
        string="Diajukan Oleh",
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1),
        readonly=True
    )
    status = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default="draft")

    # Relation product
    product_ids = fields.One2many('product.request', 'parent_id')

    # Relation Purchase Request Line
    purchase_request_line_id = fields.One2many(
        comodel_name='purchase.request.line',
        inverse_name='purchase_request_id',
        string='Request Lines'
    )
    
    relation_pr_line_status = fields.Selection(
        related='purchase_request_line_id.status', 
        string="Status"
    )

    # @api.depends('diajukan_oleh')
    # def get_employee_safely(self):
    #     try:
    #         employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
    #         if not employee:
    #             raise UserError("Tidak ada karyawan yang ditemukan untuk user ini.")
    #         return employee.name
    #     except Exception as e:
    #         raise UserError(f"Error: {str(e)}")

    def action_set_submit(self):
        self.status = 'to_approve'
        for record in self:
            record.nomor_pr = self._generate_pr_number()
            # record.tanggal_pengajuan = self._get_formatted_today_date()
            record.tanggal_pengajuan = fields.Date.context_today(self)

    def _generate_pr_number(self):
        current_year = datetime.now().strftime('%y')
        current_month = datetime.now().strftime('%b').capitalize()
        
        sequence = self.env['ir.sequence'].next_by_code('purchase.request')
        
        return f"PR/{current_year}/{current_month}/{sequence}"
    
    def action_set_approve(self):
        for record in self:
            self.env['purchase.request.line'].create({
                'purchase_request_id': record.id,
            })
        self.status = 'approved'

    def action_set_reject(self):
        self.status = 'rejected'
    
    # def _get_formatted_today_date(self):
    #     today = fields.Date.context_today(self)
    #     formatted_date = today.strftime('%d/%m/%Y')
    #     return formatted_date




