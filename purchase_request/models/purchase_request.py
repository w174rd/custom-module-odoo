from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'purchase.request'

    date = fields.Date(
        string="Tanggal Pengajuan",
        readonly=True
    )

    name = fields.Char(
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
        ('cancel', 'Cancel')
    ], string="Status", default="draft")

    status_to_display = fields.Html(
        compute="_compute_status_display",
        store=False
    )

    is_urgen = fields.Boolean(string="is Urgen", readonly=True)

    is_readonly = fields.Boolean(default=False, compute="_compute_is_readonly")

    # Relation product
    product_ids = fields.One2many('product.request', 'parent_id')

    def action_set_submit(self):
        is_valid = True
        for record in self:
            if record.product_ids:
                for product in record.product_ids:
                    print(f"======== {product.qty_request}")
                    if product.qty_request <= 0:
                        is_valid = False
            else:
                is_valid = False

        if is_valid:
            self.write({'status':'to_approve'})
            record.name = self._generate_pr_number()
            # record.date = self._get_formatted_today_date()
            record.date = fields.Date.context_today(self)
        else:
            raise UserError("Product dan QTY Request tidak boleh kosong")

    def _generate_pr_number(self):
        current_year = datetime.now().strftime('%y')
        current_month = datetime.now().strftime('%b').capitalize()
        
        sequence = self.env['ir.sequence'].next_by_code('purchase.request')
        
        return f"PR/{current_year}/{current_month}/{sequence}"
    
    def action_set_approve(self):
        approved = True
        
        if self.product_ids:
            for product in self.product_ids:
                    if product.qty_approved <= 0:
                        approved = False
        else:
            approved = False

        if approved:
            self.write({
                'status': 'approved',
                'is_urgen': False
                })
        else:
            raise UserError("Product dan QTY Approved tidak boleh kosong")

    def action_set_reject(self):
        self.write({
            'status': 'rejected',
            'is_urgen': False
            })

    def action_print_out(self):
        return self.env.ref("purchase_request.action_print_out_purchase_request").report_action(self)
    
    def _compute_is_readonly(self):
        user = self.env.user
        if user.has_group('purchase_request.group_purchase_request_user') and not user.has_group('purchase_request.group_purchase_request_approver') and self.status != 'draft':
            self.is_readonly = True
        else:
            self.is_readonly = False

    def _cron_task_update_status(self):
        records = self.search([('status', 'in', ['to_approve'])])
        print(">>>>>> Cron is running")
        for record in records:
            if record.date:
                current_date = datetime.now().date()

                # Hitung selisih waktu dalam bulan
                delta = relativedelta(current_date, record.date)
                weeks = delta.days // 7

                print(f"Interval: {delta.days} days, {weeks} weeks, {delta.months} months")

                if delta.months >= 1:
                    print("after 1 month")
                    record.write({'status': 'cancel',
                         'is_urgen': False
                         })
                elif weeks >= 2:
                    print("after 2 weeks")
                    record.write({'is_urgen': True})


    def _compute_status_display(self):
        for record in self:
            status_label = dict(self._fields['status'].selection).get(record.status, record.status)
            if record.is_urgen and record.status == 'to_approve':
                record.status_to_display = f"""
                    <span class="custom-badge custom-warning-badge">{status_label}</span>
                    <span class="custom-badge custom-danger-badge">Need to process</span>
                """
            elif record.status == 'approved':
                record.status_to_display = f"""
                    <span class="custom-badge custom-success-badge">{status_label}</span>
                """
            elif record.status == 'rejected':
                record.status_to_display = f"""
                    <span class="custom-badge custom-danger-badge">{status_label}</span>
                """
            elif record.status == 'to_approve':
                record.status_to_display = f"""
                    <span class="custom-badge custom-warning-badge">{status_label}</span>
                """    
            else:
                record.status_to_display = f"""
                    <span class="custom-badge custom-primary-badge">{status_label}</span>
                """




