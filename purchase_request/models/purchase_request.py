from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'purchase.request'

    tanggal_pengajuan = fields.Date(
        string="Tanggal Pengajuan",
        readonly=True,
        default=fields.Date.context_today
    )
    # created_by = fields.Many2one('res.users', default= lambda self : self.env.user.id)
    nomor_pr = fields.Char(string="Nomor PR")
    diajukan_oleh = fields.Many2one(
        'hr.employee',
        string="Diajukan Oleh",
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
    )
    status = fields.Selection([
        ('Draft', 'Draft'),
        ('To approve', 'To approve'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], string="Status")

    # @api.depends('diajukan_oleh')
    # def get_employee_safely(self):
    #     try:
    #         employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
    #         if not employee:
    #             raise UserError("Tidak ada karyawan yang ditemukan untuk user ini.")
    #         return employee.name
    #     except Exception as e:
    #         raise UserError(f"Error: {str(e)}")

