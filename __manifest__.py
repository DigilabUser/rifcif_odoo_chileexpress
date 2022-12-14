{
    "name": "Rifcif Odoo-ChileExpress Integrator", 
    "summary": "Odoo Community ChileExpress Integrator",
    "version": "14.0.1.0.1", 
    "category": "sales", 
    "license": "LGPL-3", 
    "author": "Ingenieria Rifcif",
    "website": "https://rifcif.cl",
    "contributors": [
        "Luis Erique Alva Villena <luis.alva@digilab.pe",
        "Jorge Eduardo Escobar Amaya <jorge.escobar@digilab.pe",
    ],
    "depends": [
        "sale_management",
        "rifcif_library_albers"
    ],
    "excludes": [],
    "data": [
        'data/comunas_data.xml',
        'data/regions_data.xml',
        'data/comunas_cchile_data.xml',
        'data/comunas_blue_data.xml',
        'security/ir.model.access.xml',
        'views/settings_inherit.xml',
        'views/sale_order.xml',
        'views/cotiza_wizard.xml',
        'views/cchile_wizard.xml',
        'views/res_comuna.xml',
        'views/res_region.xml',
        'views/res_comuna_cchile.xml',
        'views/blue_wizard.xml',
        'views/res_comuna_blue.xml',
    ],
    "qweb": [],
    "images": [],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    "auto_install": False
}
