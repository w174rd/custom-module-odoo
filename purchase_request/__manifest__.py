{
    'name': "Purchase Request",

    'summary': "Module Purchase Request",

    'description': """
    modul purchase request
    """,

    'author': "Najib",
    'website': "https://odoo.com",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/content_view.xml',
        'views/item_menu.xml',
    ],

    # 'demo': [
    #     'demo/demo.xml',
    # ],

    'assets': {
        'web.assets_backend': [
            # 'purchase_request/static/src/js/email_validation_widget.js',
            # '/purchase_request/static/src/css/custom_style.css',
        ],
    },
    'installable': True,
    'application': True,
}