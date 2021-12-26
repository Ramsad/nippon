from odoo import api, fields, models
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Product(models.Model):
    _inherit = 'product.template'

    months = fields.Integer(string="Months", required=False, )

    membership_date_from = fields.Date(string='Membership Start Date',
                                       help='Date from which membership becomes active.', compute='compute_date')
    membership_date_to = fields.Date(string='Membership End Date',
                                     help='Date until which membership remains active.' ,compute='compute_date')


    @api.depends('months')
    def compute_date(self):
        for rec in self :
            if rec.months :
                rec.membership_date_from = fields.date.today()

                EndDate = fields.date.today() + relativedelta(months=rec.months)
                # EndDate # = fields.date.today() + timedelta(days=rec.months*30)
                rec.membership_date_to =EndDate
            else :
                rec.membership_date_from = fields.date.today()
                EndDate = fields.date.today() + relativedelta(months=rec.months)
                # EndDate = fields.date.today() + timedelta(days=rec.months*30)
                rec.membership_date_to = EndDate
