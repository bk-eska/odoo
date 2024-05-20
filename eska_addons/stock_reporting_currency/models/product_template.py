# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    report_currency_standard_price = fields.Float(
        string='Currency Cost',
        compute='_compute_report_currency_standard_price',
        inverse='_set_report_currency_standard_price',
        search='_search_report_currency_standard_price',
        digits='Product Price',
        groups="base.group_user",
    )

    report_currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_report_currency_id',
    )

    @api.depends('company_id')
    def _compute_report_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            template.report_currency_id = template.company_id.sudo().report_currency_id.id or\
                                          main_company.report_currency_id.id

    @api.depends_context('company')
    @api.depends('product_variant_ids', 'product_variant_ids.report_currency_standard_price')
    def _compute_report_currency_standard_price(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.report_currency_standard_price = template.product_variant_ids.report_currency_standard_price
        for template in (self - unique_variants):
            template.report_currency_standard_price = 0.0

    def _set_report_currency_standard_price(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.report_currency_standard_price = template.report_currency_standard_price

    def _search_report_currency_standard_price(self, operator, value):
        products = self.env['product.product'].search([('report_currency_standard_price', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]
