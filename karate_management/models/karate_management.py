# -*- coding: utf-8 -*-
from odoo import models, fields, api , _

class KarateManagement(models.Model):
    _inherit = 'res.partner'

    reg_no = fields.Char(string="Reg No", required=False, default="NK")
    registration_date = fields.Date(string="Registration Date", required=False,default=fields.Date.today() )
    dob = fields.Date(string="Date of Birth", required=False, )
    age = fields.Integer(string="Age", required=False, compute='calculate_age')
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female')],default="male", required=False, )
    nationality = fields.Many2one(comodel_name="res.country", string="Nationality", required=False, )
    whatsapp = fields.Char(string="Whatsapp", required=False, default="+971 ")
    phone = fields.Char(string="", required=False,default="+971 " )
    mobile = fields.Char(string="", required=False,default="+971 " )
    activities = fields.Many2one(comodel_name="membership.activities", string="Activities", required=False, )
    is_student = fields.Boolean(string="Student",  )

    certificate_line_ids = fields.One2many(comodel_name="members.certificate", inverse_name="partner_id", string="Certificates", required=False, )

    @api.model
    def create(self, values):
        # values['reg_no'] = self.env['ir.sequence'].next_by_code('seq.membership') or _('New')
        return super(KarateManagement, self).create(values)



    @api.depends('dob')
    def calculate_age(self):
        for rec in self:
            if rec.dob:
                today = fields.datetime.today()
                age =  today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
                rec.age = age
            else :
                rec.age = 0



class Activities(models.Model):
    _name = 'membership.activities'
    _rec_name = 'name'
    _description = 'Activities'

    name = fields.Char()


class MembersCertificate(models.Model):
    _name = 'members.certificate'
    _rec_name = 'name'
    _description = 'Certificates'

    name = fields.Char()
    amount = fields.Float(string="Amount",  required=False, )
    certificate_no = fields.Char(string="Certificate No.",  required=False, )
    certificate = fields.Binary(string="Certificate",  required=False, )
    date = fields.Date(string="Date", required=False,default=fields.Date.today() )
    status = fields.Selection(string="Status", selection=[('new', 'New'), ('paid', 'paid'), ], required=False, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="", required=False, )
    invoice_id = fields.Many2one(comodel_name="account.move", string="Invoice", required=False, )
    kyu = fields.Selection(string="Kyu", selection=[('9th', '9th'),
                                                    ('8th', '8th'),
                                                    ('7th', '7th'),
                                                    ('6th', '6th'),
                                                    ('5th', '5th'),
                                                    ('4th', '4th'),
                                                    ('3rd', '3rd'),
                                                    ('2nd', '2nd'),
                                                    ('1st', '1st'),

                                                    ], required=False, )
    belt  = fields.Selection(string="Belt", selection=[('Yellow', 'Yellow'),
                                                       ('Orange', 'Orange'),
                                                       ('Green', 'Green'),
                                                       ('Blue', 'Blue'),
                                                       ('Purple', 'Purple'),
                                                       ('Brown', 'Brown'),
                                                       ('Black', 'Black'),
                                                       ], required=False, )
    dan = fields.Selection(string="Dan", selection=[
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
    ], required=False, )

    state = fields.Selection(string="", selection=[('new', 'New'), ('in_progress', 'In Progress'),
                                                   ('passed', 'Passed'),('failed', 'Failed'), ],
                             default="new", required=False, )
    payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy')],
        string="Payment Status", related="invoice_id.payment_state")

    @api.onchange('belt')
    def _onchange_belt(self):
        self.kyu = False
        self.dan = False

    def generate_invoice(self):
        invoice = self.env['account.move'].create(

            {
                "move_type":"out_invoice",
                "partner_id": self._context['partner_id'] ,
                "invoice_line_ids":[(0, 0, {
                    "product_id": self.env.ref('karate_management.belt_test_product_template').product_variant_id,
                    "price_unit": self.amount,

                })]


            }
        )
        invoice.action_post()
        self.write({

            "invoice_id":invoice,
        })

    def action_view_test_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'target': 'current',
            'res_id': self.invoice_id.id,
        }