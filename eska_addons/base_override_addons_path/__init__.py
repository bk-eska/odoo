# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import odoo

odoo.addons.__path__ = odoo.addons.__path__[2:] + odoo.addons.__path__[:2]
