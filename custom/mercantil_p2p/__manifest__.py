# -*- coding: utf-8 -*-
{
    "name": "Mercantil Payments",
    "summary": """
        Pago movil con la api del mercantil 
    """,
    "author": "Ingeint",
    "website": "https://ingeint.com/",
    "category": "Services",
    "version": "14.0.0.1",
    "depends": [
        "base",
        "account",
        "contacts",
        "portal",
        "payment",
        "payment_acquirer_list",
        "ingeint_isp_control",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/payment_acquierer.xml",
        "wizards/wizard_mercantil_config_payment.xml",
        "views/menu.xml",
    ],
}
