# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    blood_type = fields.Selection(
        [
            ('a_positive', 'A+'),
            ('a_negative', 'A-'),
            ('b_positive', 'B+'),
            ('b_negative', 'B-'),
            ('ab_positive', 'AB+'),
            ('ab_negative', 'AB-'),
            ('zero_positive', '0+'),
            ('zero_negative', '0-'),
        ],
        string="Blood Type",
        groups="hr.group_hr_user",
    )
