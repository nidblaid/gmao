# -*- coding: utf-8 -*-
{
    'name': "Gmao",

    'summary': """
        Gmao module is an extension for Maintenance business applications""",

    'description': """
        Sales Analytics module is an extension for Sales business applications that provides comprehensive insights into the performance of salespersons. 
	The module calculates and presents key metrics, such as active leads, dispatched leads, processed leads, quotations, sales orders, and delivery rates for both "cold" and "fresh" data.
    """,

    'author': "Econostic",
    'website': "http://www.econostic.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','base_automation', 'mrp', 'maintenance', 'fleet', 'repair'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'wizard/update_results_view.xml',
        'views/views.xml',
        # 'views/templates.xml',
        
    ],
    'installable': True,
	'auto_install': False,
	'application': True,
}
