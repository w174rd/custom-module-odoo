
from odoo import models, fields

class SalesInherit(models.Model):
    _inherit= 'sale.order'

    test = fields.Char(
        string="Test"
    )

    def action_test(self):
        self.test.write("label")



