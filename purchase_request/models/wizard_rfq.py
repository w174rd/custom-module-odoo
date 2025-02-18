from odoo import models, fields, api
from odoo.exceptions import (
    AccessError,
    RedirectWarning,
    UserError,
    ValidationError,
)

class WizardRFQ(models.Model):
    _name = 'wizard.rfq'
    _description = 'Wizard RFQ'

    vendor = fields.Many2one('res.partner', string="Vendor", required=True)
    product_req_ids = fields.One2many('product.request', 'wizard_id', store=False)

    @api.model
    def default_get(self, fields_list):
        res = super(WizardRFQ, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids', []) # Ambil ID yang dipilih
        if active_ids:
            print(f"======== {active_ids} ========")
            products = []
            for product in self.env['product.request'].browse(active_ids):
                products.append((0, 0, {
                    'product': product.product.id,
                    'qty_request': product.qty_request,
                    'qty_approved': product.qty_approved,
                    'parent_id': product.parent_id.id
                }))
            res.update({'product_req_ids': products})
        return res
    


    def action_create_rfq(self):
        active_ids = self.env.context.get('active_ids', [])

        if self.env['product.request'].browse(active_ids).purchase_order:
            raise UserError("Purchase Order sudah dibuat sebelumnya")

        # Buat Purchase Order (RFQ)
        purchase_order_record = self.env['purchase.order'].create({
            'partner_id': self.vendor.id,  # Vendor dari wizard
        })

        for product in self.env['product.request'].browse(active_ids):

            self.env['purchase.order.line'].create({
                'order_id': purchase_order_record.id,
                'product_id': product.product.id,
                'product_qty': product.qty_approved,
                # 'price_unit': product.product.standard_price,
                # 'date_planned': fields.Date.today(),
            })

            # update status
            if product.parent_id:
                product.parent_id.write({'status': 'rfq_created'})

            product.write({
                'purchase_order': purchase_order_record.id
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Request for Quotation',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': purchase_order_record.id,
            'target': 'current',
        }