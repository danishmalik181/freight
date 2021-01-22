# -*- coding: utf-8 -*-
{
    'name': "Sales Extension Module",

    'summary': """ Warehouse Management, This theme module is exclusively for Sales""",

    'description': """
        Warehouse Update
    """,

    'author': "silverdale",
    'website': "http://www.silverdaletech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'General',
    'version': '14.0.2102',

    # any module necessary for this one to work correctly
    # 'depends' : ['sale', 'crm', 'project','stock', 'portal_sale', 'delivery', 'purchase', 'account', 'website_sale', 'sale_order_dates','website','mail','survey'],
    'depends' : ['mail','sale','stock','delivery',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        "views/report_sale_pickticket_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",

        "report/kmi_reports.xml",

        "data/mail_template_data.xml",

        "wizards/mail_compose_message_view.xml",
        "wizards/freight_vendor_mail.xml",
    ],
    # 'qweb': [
    #         "static/src/xml/web_calendar.xml",
    #     ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
