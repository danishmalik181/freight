# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from PIL import Image
import requests
from io import BytesIO
import codecs
import pdb
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_freight_vendor = fields.Boolean(string="Freight Vendor")
    sale_order_partner = fields.Many2one('sale.order', string='Sale_order_partner')


class MailComposeInherit(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail_custom(self):
        partners = []
        for line in self.partner_ids:
            partners.append((0, 0, {
                'name': line.name,
                'display_name': line.name,
                'sale_order_partner': self._context.get('active_id'),
                'email': line.email}))
            active_order = self.env['sale.order'].search([('id', '=', self._context.get('active_id'))],limit=1)

            active_order.sale_partner = [(5,0,0)]
            active_order.sale_partner = partners

            template = self.env.ref('sale_ext.quote_email_template_freight_vendor')
            post_message = active_order.message_post_with_template(template.id, composition_mode='comment')

            #     self.send_mail_custom()
    #     return {'type': 'ir.actions.act_window_close', 'infos': 'mail_sent'}
    #
    # def send_mail_custom(self, auto_commit=False):
    #     """ Process the wizard content and proceed with sending the related
    #         email(s), rendering any template patterns on the fly if needed. """
    #     notif_layout = self._context.get('custom_layout')
    #     # Several custom layouts make use of the model description at rendering, e.g. in the
    #     # 'View <document>' button. Some models are used for different business concepts, such as
    #     # 'purchase.order' which is used for a RFQ and and PO. To avoid confusion, we must use a
    #     # different wording depending on the state of the object.
    #     # Therefore, we can set the description in the context from the beginning to avoid falling
    #     # back on the regular display_name retrieved in '_notify_prepare_template_context'.
    #     model_description = self._context.get('model_description')
    #     for wizard in self:
    #         # Duplicate attachments linked to the email.template.
    #         # Indeed, basic mail.compose.message wizard duplicates attachments in mass
    #         # mailing mode. But in 'single post' mode, attachments of an email template
    #         # also have to be duplicated to avoid changing their ownership.
    #         if wizard.attachment_ids and wizard.composition_mode != 'mass_mail' and wizard.template_id:
    #             new_attachment_ids = []
    #             for attachment in wizard.attachment_ids:
    #                 if attachment in wizard.template_id.attachment_ids:
    #                     new_attachment_ids.append(attachment.copy({'res_model': 'mail.compose.message', 'res_id': wizard.id}).id)
    #                 else:
    #                     new_attachment_ids.append(attachment.id)
    #             new_attachment_ids.reverse()
    #             wizard.write({'attachment_ids': [(6, 0, new_attachment_ids)]})
    #
    #         # Mass Mailing
    #         mass_mode = wizard.composition_mode in ('mass_mail', 'mass_post')
    #
    #         ActiveModel = self.env[wizard.model] if wizard.model and hasattr(self.env[wizard.model], 'message_post') else self.env['mail.thread']
    #         if wizard.composition_mode == 'mass_post':
    #             # do not send emails directly but use the queue instead
    #             # add context key to avoid subscribing the author
    #             ActiveModel = ActiveModel.with_context(mail_notify_force_send=False, mail_create_nosubscribe=True)
    #         # wizard works in batch mode: [res_id] or active_ids or active_domain
    #         if mass_mode and wizard.use_active_domain and wizard.model:
    #             res_ids = self.env[wizard.model].search(ast.literal_eval(wizard.active_domain)).ids
    #         elif mass_mode and wizard.model and self._context.get('active_ids'):
    #             res_ids = self._context['active_ids']
    #         else:
    #             res_ids = [wizard.res_id]
    #
    #         batch_size = int(self.env['ir.config_parameter'].sudo().get_param('mail.batch_size')) or self._batch_size
    #         sliced_res_ids = [res_ids[i:i + batch_size] for i in range(0, len(res_ids), batch_size)]
    #
    #         if wizard.composition_mode == 'mass_mail' or wizard.is_log or (wizard.composition_mode == 'mass_post' and not wizard.notify):  # log a note: subtype is False
    #             subtype_id = False
    #         elif wizard.subtype_id:
    #             subtype_id = wizard.subtype_id.id
    #         else:
    #             subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
    #
    #         for res_ids in sliced_res_ids:
    #             # mass mail mode: mail are sudo-ed, as when going through get_mail_values
    #             # standard access rights on related records will be checked when browsing them
    #             # to compute mail values. If people have access to the records they have rights
    #             # to create lots of emails in sudo as it is consdiered as a technical model.
    #             batch_mails_sudo = self.env['mail.mail'].sudo()
    #             all_mail_values = wizard.get_mail_values(res_ids)
    #             for res_id, mail_values in all_mail_values.items():
    #                 if wizard.composition_mode == 'mass_mail':
    #                     batch_mails_sudo |= self.env['mail.mail'].sudo().create(mail_values)
    #                 else:
    #                     post_params = dict(
    #                         message_type=wizard.message_type,
    #                         subtype_id=subtype_id,
    #                         email_layout_xmlid=notif_layout,
    #                         add_sign=not bool(wizard.template_id),
    #                         mail_auto_delete=wizard.template_id.auto_delete if wizard.template_id else False,
    #                         model_description=model_description)
    #                     post_params.update(mail_values)
    #                     if ActiveModel._name == 'mail.thread':
    #                         if wizard.model:
    #                             post_params['model'] = wizard.model
    #                             post_params['res_id'] = res_id
    #                         if not ActiveModel.message_notify(**post_params):
    #                             # if message_notify returns an empty record set, no recipients where found.
    #                             raise UserError(_("No recipient found."))
    #                     else:
    #                         ActiveModel.browse(res_id).message_post(**post_params)
    #
    #             if wizard.composition_mode == 'mass_mail':
    #                 batch_mails_sudo.send(auto_commit=auto_commit)
