# -*- coding: utf-8 -*-
{
    'name': "karate_management",
    'summary': """ 
               Karate Management System
               """,
    'description': """
        Karate Management System
    """,
    'author': "Ramsad PV",
    'category': 'Uncategorized',
    'version': '14.0.1',
    'depends': ['base','membership','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/belt_test_product.xml',
        'views/hide.xml',
        'wizard/test_details.xml',
        'views/karate_management.xml',
        'views/templates.xml',
        'views/activities.xml',
        'views/producut.xml',
    ],
}
