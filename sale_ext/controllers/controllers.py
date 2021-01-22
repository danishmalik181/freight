# -*- coding: utf-8 -*-
# from odoo import http


# class CalendarExt(http.Controller):
#     @http.route('/calendar_ext/calendar_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calendar_ext/calendar_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('calendar_ext.listing', {
#             'root': '/calendar_ext/calendar_ext',
#             'objects': http.request.env['calendar_ext.calendar_ext'].search([]),
#         })

#     @http.route('/calendar_ext/calendar_ext/objects/<model("calendar_ext.calendar_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calendar_ext.object', {
#             'object': obj
#         })
