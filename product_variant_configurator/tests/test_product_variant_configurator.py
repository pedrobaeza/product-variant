# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# © 2016 2016 ACSONE SA/NV
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import SavepointCase
from openerp.exceptions import ValidationError


class TestProductVariantConfigurator(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductVariantConfigurator, cls).setUpClass()

        # ENVIRONMENTS
        cls.product_attribute = cls.env['product.attribute']
        cls.product_attribute_value = cls.env['product.attribute.value']
        cls.product_category = cls.env['product.category']
        cls.product_product = cls.env['product.product']
        cls.product_template = cls.env['product.template'].with_context(
            check_variant_creation=True)

        # INSTANCES
        # Instances: product category
        cls.category1 = cls.product_category.create({
            'name': 'No create variants category',
        })
        cls.category2 = cls.product_category.create({
            'name': 'Create variants category',
            'no_create_variants': False,
        })
        # Instances: product attribute
        cls.attribute1 = cls.product_attribute.create({
            'name': 'Test Attribute 1',
        })
        cls.attribute2 = cls.product_attribute.create({
            'name': 'Test Attribute 2',
        })
        # Instances: product attribute value
        cls.value1 = cls.product_attribute_value.create({
            'name': 'Value 1',
            'attribute_id': cls.attribute1.id,
        })
        cls.value2 = cls.product_attribute_value.create({
            'name': 'Value 2',
            'attribute_id': cls.attribute1.id,
        })
        cls.value3 = cls.product_attribute_value.create({
            'name': 'Value 3',
            'attribute_id': cls.attribute2.id,
        })
        cls.value4 = cls.product_attribute_value.create({
            'name': 'Value 4',
            'attribute_id': cls.attribute2.id,
        })
        # Instances: product template
        cls.product_template_yes = cls.product_template.create({
            'name': 'Product template 1',
            'no_create_variants': 'yes',
            'attribute_line_ids': [
                (0, 0, {'attribute_id': cls.attribute1.id,
                        'value_ids': [(6, 0, [cls.value1.id,
                                              cls.value2.id])]})],
        })
        cls.product_template_no = cls.product_template.create({
            'name': 'Product template 2',
            'no_create_variants': 'no',
        })
        cls.product_template_empty_no = cls.product_template.create({
            'name': 'Product template 3',
            'no_create_variants': 'empty',
            'categ_id': cls.category1.id,
        })
        cls.product_template_empty_yes = cls.product_template.create({
            'name': 'Product template 3',
            'no_create_variants': 'empty',
            'categ_id': cls.category2.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': cls.attribute1.id,
                        'value_ids': [(6, 0, [cls.value1.id,
                                              cls.value2.id])]})],
        })

    def test_no_create_variants(self):
        tmpl = self.product_template.create({
            'name': 'No create variants template',
            'no_create_variants': 'yes',
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]})],
        })
        self.assertEquals(len(tmpl.product_variant_ids), 0)
        tmpl = self.product_template.create({
            'name': 'No variants template',
            'no_create_variants': 'yes',
        })
        self.assertEquals(len(tmpl.product_variant_ids), 0)

    def test_no_create_variants_category(self):
        self.assertTrue(self.category1.no_create_variants)
        tmpl = self.product_template.create({
            'name': 'Category option template',
            'categ_id': self.category1.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]})],
        })
        self.assertTrue(tmpl.no_create_variants == 'empty')
        self.assertEquals(len(tmpl.product_variant_ids), 0)
        tmpl = self.product_template.create({
            'name': 'No variants template',
            'categ_id': self.category1.id,
        })
        self.assertTrue(tmpl.no_create_variants == 'empty')
        self.assertEquals(len(tmpl.product_variant_ids), 0)

    def test_create_variants(self):
        tmpl = self.product_template.create({
            'name': 'Create variants template',
            'no_create_variants': 'no',
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]})],
        })
        self.assertEquals(len(tmpl.product_variant_ids), 2)
        tmpl = self.product_template.create({
            'name': 'No variants template',
            'no_create_variants': 'no',
        })
        self.assertEquals(len(tmpl.product_variant_ids), 1)

    def test_create_variants_category(self):
        self.assertFalse(self.category2.no_create_variants)
        tmpl = self.product_template.create({
            'name': 'Category option template',
            'categ_id': self.category2.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]})],
        })
        self.assertTrue(tmpl.no_create_variants == 'empty')
        self.assertEquals(len(tmpl.product_variant_ids), 2)
        tmpl = self.product_template.create({
            'name': 'No variants template',
            'categ_id': self.category2.id,
        })
        self.assertTrue(tmpl.no_create_variants == 'empty')
        self.assertEquals(len(tmpl.product_variant_ids), 1)

    def test_category_change(self):
        self.assertTrue(self.category1.no_create_variants)
        tmpl = self.product_template.create({
            'name': 'Category option template',
            'categ_id': self.category1.id,
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]})],
        })
        self.assertTrue(tmpl.no_create_variants == 'empty')
        self.assertEquals(len(tmpl.product_variant_ids), 0)
        self.category1.no_create_variants = False
        self.assertEquals(len(tmpl.product_variant_ids), 2)

    def test_onchange_no_create_variants(self):
        with self.cr.savepoint():
            self.product_template_yes.no_create_variants = 'no'
            result = self.product_template_yes.onchange_no_create_variants()
            self.assertTrue('warning' in result)

    def test_onchange_no_create_variants_category(self):
        with self.cr.savepoint():
            self.category1.no_create_variants = False
            result = self.category1.onchange_no_create_variants()
            self.assertTrue('warning' in result)

    def test_open_attribute_prices(self):
        result = self.product_template_no.action_open_attribute_prices()
        self.assertEqual(result['type'], u'ir.actions.act_window')

    def test_get_product_attributes_dict(self):
        attrs_dict = self.product_template_yes._get_product_attributes_dict()
        self.assertEquals(len(attrs_dict), 1)
        self.assertEquals(len(attrs_dict[0]), 1)

    def test_get_product_description(self):
        product = self.product_product.create({
            'name': 'Test product',
            'product_tmpl_id': self.product_template_yes.id
        })
        self.assertEquals(product._get_product_description(
            product.product_tmpl_id, product, product.attribute_value_ids),
            'Test product')

        self.current_user = self.env.user
        # Add current user to group: group_supplier_inv_check_total
        group_id = (
            'product_variant_configurator.'
            'group_product_variant_extended_description')
        self.env.ref(group_id).write({'users': [(4, self.current_user.id)]})

        self.assertEquals(product._get_product_description(
            product.product_tmpl_id, product, product.attribute_value_ids),
            'Test product')

    def test_onchange_product_tmpl_id(self):
        product = self.product_product.create({
            'name': 'Test product',
            'product_tmpl_id': self.product_template_yes.id
        })
        with self.cr.savepoint(), self.assertRaises(ValidationError):
            product.product_tmpl_id = self.product_template_no

        with self.cr.savepoint():
            product.product_tmpl_id = self.product_template_empty_no
            res = product.onchange_product_tmpl_id()
            self.assertEquals(
                res,
                {'domain': {'product_id': [
                    ('product_tmpl_id', '=', self.product_template_empty_no.id)
                ]}})

    def test_templ_name_search(self):
        res = self.product_template.name_search('Product template 222')
        for r in res:
            if r[0] == self.product_template_no.id:
                self.fail()
        res = self.product_template.name_search('Product template 2')
        for r in res:
            if r[0] == self.product_template_no.id:
                return
        self.fail()

    def test_check_configuration_validity(self):

        tmpl = self.product_template.create({
            'name': 'Product template Check',
            'no_create_variants': 'yes',
            'attribute_line_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_ids': [(6, 0, [self.value1.id,
                                              self.value2.id])]}),
                (0, 0, {'attribute_id': self.attribute2.id,
                        'value_ids': [(6, 0, [self.value3.id,
                                              self.value4.id])]})
            ],
        })

        with self.cr.savepoint(), self.assertRaises(ValidationError):
            product_vals = {
                'name': 'Test product Check',
                'product_tmpl_id': tmpl.id,
                'product_attribute_ids': [(0, 0, {
                    'product_tmpl_id': tmpl.id,
                    'attribute_id': self.attribute1.id,
                    'value_id': None
                })]
            }
            self.product_product.check_configuration_validity(product_vals)

    def test_onchange_product_attribute_ids(self):
        product = self.product_product.create({
            'name': 'Test product Check',
            'product_tmpl_id': self.product_template_yes.id,
        })
        product_attribute_vals = {
            'product_tmpl_id': self.product_template_yes.id,
            'attribute_id': self.attribute1.id,
            'value_id': self.value2.id,
            'owner_model': 'res.partner',
        }
        product.write(
            {'product_attribute_ids': [(0, 0, product_attribute_vals)]})
        result = product.onchange_product_attribute_ids()
        self.assertTrue(
            ('product_tmpl_id', '=', self.product_template_yes.id)
            in result['domain']['product_id']
        )

    def test_get_product_attributes_values_dict(self):
        product = self.product_product.create({
            'name': 'Test product Check',
            'product_tmpl_id': self.product_template_yes.id,
            'product_attribute_ids': [(0, 0, {
                'product_tmpl_id': self.product_template_yes.id,
                'attribute_id': self.attribute1.id,
                'value_id': self.value1.id,
            })]
        })
        result = product._get_product_attributes_values_dict()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0],
                         {'attribute_id': self.attribute1.id,
                          'value_id': self.value1.id})

    def test_get_product_attributes_values_text(self):
        product = self.product_product.create({
            'name': 'Test product Check',
            'product_tmpl_id': self.product_template_yes.id,
            'product_attribute_ids': [(0, 0, {
                'product_tmpl_id': self.product_template_yes.id,
                'attribute_id': self.attribute1.id,
                'value_id': self.value1.id,
            })]
        })
        result = product._get_product_attributes_values_text()
        expected_result = "%s\n%s: %s" % (
            self.product_template_yes.name,
            self.attribute1.name,
            self.value1.name
        )
        self.assertEqual(result, expected_result)

        product = self.product_product.create({
            'name': 'Test product Check',
            'product_tmpl_id': self.product_template_yes.id,
        })
        result = product._get_product_attributes_values_text()
        self.assertEqual(result, self.product_template_yes.name)

    def test_create_variant_from_vals(self):
        vals = {
            'product_tmpl_id': self.product_template_yes.id,
            'product_attribute_ids': [(0, 0, {
                'product_tmpl_id': self.product_template_yes.id,
                'attribute_id': self.attribute1.id,
                'value_id': self.value1.id,
                'owner_model': 'purchase.order.line'
            })]
        }
        self.product_product._create_variant_from_vals(vals)
        self.assertTrue('product_id' in vals)

    def test_unlink(self):

        product = self.product_product.create({
            'name': 'Test product Check',
            'product_tmpl_id': self.product_template_yes.id,
            'product_attribute_ids': [
                (0, 0, {'attribute_id': self.attribute1.id,
                        'value_id': self.value1.id,
                        'product_tmpl_id': self.product_template_yes.id,
                        })
            ]})

        self.assertTrue(product.unlink())
