from AptUrl.Helpers import _
from odoo import models, fields, api
import datetime


class FreightVendor(models.TransientModel):
    _name = 'freight.vendor.wiz'
    _description = 'freight vendor mail send'

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string=' Partner')
    subject = fields.Char(
        string='Subject',
        required=True)
    body = fields.Html(
        string='Body',
        required=False)
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string='Attachment_ids')
    template_id = fields.Many2one(
        comodel_name='mail.template',
        string='Use Template',
        required=False)