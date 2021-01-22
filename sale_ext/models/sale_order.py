import pdb
from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    weight_order = fields.Float('Total Gross Weight', compute='_calc_weight')
    sale_partner = fields.One2many('res.partner','sale_order_partner',string='Partners',store=True)

    @api.depends('order_line')
    def _calc_weight(self):
        for order in self:
            weight = 0.0
            for line in order.order_line:
                weight += line.product_id and line.product_id.weight * line.product_uom_qty
            order.weight_order = weight

    def send_mail_freight(self):
        template = self.env.ref('sale_ext.quote_email_template_freight_vendor')
        post_message = self.message_post_with_template(template.id, composition_mode='comment')

    def action_freight_vendor_quotation_send(self):
        '''
        This function opens a window to compose an email for freight vendor,
        with the freight vendor template message loaded by default
        '''
        self.ensure_one()
        template = self.env.ref('sale_ext.quote_email_template_freight_vendor', False)
        compose_form = self.env.ref('sale_ext.email_compose_freight_vendor_message_wizard_form', False)
        # compose_form = self.env.ref('mail.email_compose_freight_vendor_message_wizard_form', False)
        ctx = dict(
            default_model='sale.order',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            custom_layout='mail.mail_notification_light',
            vendor_quote=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_freight_vendor_mail_send(self):
        '''
        This function opens a window to compose an email for freight vendor,
        with the freight vendor template message loaded by default
        '''
        self.ensure_one()
        template = self.env.ref('sale_ext.quote_email_template_freight_vendor', False)
        compose_form = self.env.ref('sale_ext.freight_vendor_mail_wizard_form', False)
        # compose_form = self.env.ref('mail.email_compose_freight_vendor_message_wizard_form', False)
        ctx = dict(
            default_model='sale.order',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            custom_layout='mail.mail_notification_light',
            vendor_quote=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'freight.vendor.wiz',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }