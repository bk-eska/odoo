# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": 'Location Management County Support',
    "summary": 'Adds county support to location management',
    "version": "16.0.1.0.0",
    "category": 'Localization',
    "author": 'Eska',
    "website": 'http://www.eskayazilim.com.tr',
    "license": 'AGPL-3',
    "depends": [
        'base_location',
        'base_county'
    ],
    "data": [
        'views/res_county_view.xml',
        'views/res_better_zip_view.xml'
    ],
    "installable": True,
    "auto_install": True,
}
