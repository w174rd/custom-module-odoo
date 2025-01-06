
from odoo import models, fields

class ResUsers(models.Model):
    _inherit= 'res.users'

    purchase_request_rule = fields.Selection([
        ('user', 'User'),
        ('approver', 'Approver'),
    ], default='user')

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
       
        if 'purchase_request_rule' in vals:
            group_ids = [(3, self.env.ref('purchase_request.group_purchase_request_user').id), (3, self.env.ref('purchase_request.group_purchase_request_approver').id)]
            if vals['purchase_request_rule'] == 'user':
                group_ids.append((4, self.env.ref('purchase_request.group_purchase_request_user').id))
            if vals['purchase_request_rule'] == 'approver':
                group_ids.append((4, self.env.ref('purchase_request.group_purchase_request_approver').id))
            
            self.write({'groups_id': group_ids})

        return res