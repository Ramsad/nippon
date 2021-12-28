from odoo import api, fields, models , _


class MembersCertificate(models.TransientModel):
    _name = 'members.certificate.wizard'
    _rec_name = 'name'
    _description = 'Certificates'

    name = fields.Char()
    amount = fields.Float(string="Amount", required=False, )
    certificate_no = fields.Char(string="Certificate No.", required=False, )
    certificate = fields.Binary(string="Certificate", required=False, )
    date = fields.Date(string="Date", required=False, default=fields.Date.today())
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
    belt = fields.Selection(string="Belt", selection=[('Yellow', 'Yellow'),
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

    state = fields.Selection(string="", selection=[('new', 'New'), ('paid', 'Paid'),
                                                   ('passed', 'Passed'), ('failed', 'Failed'), ],
                             default="new", required=False, )

    @api.onchange('belt')
    def _onchange_belt(self):
        self.kyu = False
        self.dan = False

    def generate_invoice(self):

        test_details = self.partner_id.write(
            {
                "certificate_line_ids": [(0,0,{
                    "belt":self.belt,
                    "kyu":self.kyu,
                    "dan":self.dan,
                    "certificate_no":self.certificate_no,
                    # "certificate":self.certificate,
                    "partner_id":self.partner_id,
                    "amount":self.amount
                }
                )]
            }
        )
        test_id = self.partner_id.certificate_line_ids.ids[-1]

        test_generate_invoice = self.partner_id.certificate_line_ids.search([('id','=',test_id)]).generate_invoice()

        # invoice = self.env['account.move'].create(
        #
        #     {
        #         "move_type": "out_invoice",
        #         "partner_id": self._context['partner_id'],
        #         "invoice_line_ids": [(0, 0, {
        #             "product_id": self.env.ref('karate_management.belt_test_product_template').product_variant_id,
        #             "price_unit": self.amount,
        #
        #         })]
        #
        #     }
        # )
        #
        # test_details.write({"invoice_id":invoice})


    def action_view_test_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'target': 'current',
            'res_id': self.invoice_id.id,
        }
