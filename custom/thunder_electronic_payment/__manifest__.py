{
    "name": "Configuracion de pagos electronicos thunder",
    "summary": """
        modulo para configurar las generacion de facturas de los pedidos de pagos electronicos
    """,
    "author": "INGEINT CA",
    "website": "https://www.ingeint.com",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["base", "l10n_ve_printer", "bnc_payments", "portal_bdv_payment"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/config_electronic_payment_views.xml",
    ],
}
