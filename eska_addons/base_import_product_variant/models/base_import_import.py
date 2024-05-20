# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class BaseImportImport(models.TransientModel):
    _inherit = 'base_import.import'

    def get_variant_import_fields(self):
        return ['variant_id', 'variant_attributes', 'variant_attribute_values']

    def is_variant_field(self, field):
        if not field.startswith("variant_"):
            return False
        return True if self.env['ir.model.fields'].search([
            ('model_id.model', '=', 'product.product'),
            ('name', '=', field[8:]),
            ('readonly', '=', False),
        ]) else False

    def find_external_id(self, model, external_id):
        if '.' not in external_id:
            return False
        module = external_id.split('.', 1)[0]
        name = external_id.split('.', 1)[1]
        return self.env['ir.model.data'].search([
            ('model', '=', model),
            ('module', '=', module),
            ('name', '=', name),
        ])


    def execute_import(self, fields, columns, options, dryrun=False):
        result = super().execute_import(fields, columns, options, dryrun)
        if self.res_model == 'product.template' and 'ids' in result and result['ids']:
            variant_obj = self.env["product.product"]
            template_obj = self.env["product.template"]
            attribute_line_obj = self.env['product.template.attribute.line']
            attribute_value_obj = self.env['product.attribute.value']
            attribute_obj = self.env['product.attribute']
            external_obj = self.env['ir.model.data']
            # add variant columns
            for index, column in enumerate(columns) :
                if column in self.get_variant_import_fields() or self.is_variant_field(column):
                    fields[index] = column
            data, import_fields = self._convert_import_data(fields, options)
            for index in range(0, len(result["ids"])):
                row = data[index]
                # do attributes exists?
                if 'variant_attributes' in import_fields and \
                        'variant_attribute_values' in import_fields:
                    attributes = row[import_fields.index('variant_attributes')].split('|')
                    attributes = list(filter(None, attributes))
                    attribute_values = row[import_fields.index('variant_attribute_values')].split('|')
                    attribute_values = list(filter(None, attribute_values))
                    if len(attributes) != len(attribute_values):
                        raise ValueError(
                            _("Attribute and value count is different in row %d.") % (index+1))
                    attribute_ids = []
                    attribute_value_ids = []
                    # prepare attribute records
                    for attribute in attributes:
                        if attributes.count(attribute) > 1:
                            raise ValueError(
                                _("Attribute %s is used multiple times at line %d.") % (attribute, index+1))
                        external = self.find_external_id(
                            'product.attribute', attribute)
                        if external:
                            attribute_rec = attribute_obj.search(
                                [('id', '=', external.res_id)], limit=1)
                        else:
                            attribute_rec = attribute_obj.search(
                                [('name', '=', attribute)], limit=1)
                        if not attribute_rec:
                            attribute_rec = attribute_obj.create(
                                {'name': attribute})
                        attribute_ids.append(attribute_rec.id)
                    # prepare attribute value records
                    for val_index, attribute_val in enumerate(attribute_values):
                        external = self.find_external_id(
                            'product.attribute', attribute)
                        if external:
                            attribute_value_rec = attribute_value_obj.search(
                                [('id', '=', external.res_id)], limit=1)
                        else:
                            attribute_value_rec = attribute_value_obj.search([
                                ('name', '=', attribute_val),
                                ('attribute_id', '=', attribute_ids[val_index]),
                            ], limit=1)
                        if not attribute_value_rec:
                            attribute_value_rec = attribute_value_obj.create({
                                'name': attribute_val,
                                'attribute_id': attribute_ids[val_index],
                            })
                        attribute_value_ids.append(attribute_value_rec.id)
                    # check if product exists
                    template = template_obj.search([
                        ("id", "=", result["ids"][index]),
                    ],limit=1)
                    if template:
                        domain = [('product_tmpl_id', '=', template.id)]
                        for attribute_value_id in attribute_value_ids:
                            domain.append(
                                ('product_template_attribute_value_ids.product_attribute_value_id.id', '=', attribute_value_id))
                        variant = variant_obj.search(domain, limit=1)
                        if not variant:
                            for att_index, attribute_id in enumerate(attribute_ids):
                                attribute_line = attribute_line_obj.search([
                                    ('attribute_id','=', attribute_id),
                                    ('product_tmpl_id', '=', template.id),
                                ],limit=1)
                                if attribute_line:
                                    attribute_line.write({
                                        'value_ids': [
                                            (6, 0, attribute_line.value_ids.ids +
                                             [attribute_value_ids[att_index]])]
                                    })
                                else:
                                    attribute_line_obj.create({
                                        'attribute_id': attribute_id,
                                        'product_tmpl_id': template.id,
                                        'value_ids': [(6, 0, [
                                            attribute_value_ids[att_index]])]
                                    })
                            # create the variant
                            template._create_variant_ids()
                        variant = variant_obj.search(domain, limit=1)
                        if not variant:
                            raise ValueError(
                                _("Cannot create variant in row %d.") % (index+1))
                        # update variant values
                        values = {}
                        for field in import_fields:
                            if field == 'variant_id':
                                if dryrun:
                                    continue
                                external_id = row[import_fields.index(field)]
                                module = external_id.split('.', 1)[0]
                                name = external_id.split('.', 1)[1]
                                external_by_id = self.env['ir.model.data'].search([
                                    ('model', '=', 'product.product'),
                                    ('res_id', '=', variant.id),
                                ])
                                external_by_ref = self.find_external_id(
                                    'product.product', external_id)
                                if external_by_ref and external_by_id:
                                    if external_by_id != external_by_ref:
                                        # id has a different ref
                                        external_by_ref.unlink()
                                        external_by_id.write({
                                            'module': module,
                                            'name': name
                                        })
                                elif external_by_id:
                                    # id exist with wrong ref
                                    external_by_id.write({
                                        'module': module,
                                        'name': name
                                    })
                                elif external_by_ref:
                                    # ref is pointing to wrong id
                                    external_by_ref.write({
                                        'res_id': variant.id,
                                    })
                                else:
                                    # no ref create one
                                    external_obj.create({
                                        'model': 'product.product',
                                        'module': module,
                                        'name': name,
                                        'res_id': variant.id,
                                    })
                                continue
                            if self.is_variant_field(field):
                                values[field[8:]] = row[import_fields.index(field)]
                        if values:
                            variant.write(values)
        return result
