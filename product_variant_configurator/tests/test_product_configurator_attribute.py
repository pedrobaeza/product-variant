# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import SavepointCase


class TestProductConfiguratorAttribute(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductConfiguratorAttribute, cls).setUpClass()
        # ENVIRONMENTS
        cls.product_attribute = cls.env['product.attribute']
        cls.product_attribute_value = cls.env['product.attribute.value']
        cls.product_configuration_attribute = \
            cls.env['product.configurator.attribute']
        cls.product_attribute_price = cls.env['product.attribute.price']
        cls.product_template = cls.env['product.template'].with_context(
            check_variant_creation=True)

        # Instances: product attribute
        cls.attribute1 = cls.product_attribute.create({
            'name': 'Test Attribute 1',
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

        # Instances: product template
        cls.product_template1 = cls.product_template.create({
            'name': 'Product template 1',
            'no_create_variants': 'no',
            'attribute_line_ids': [
                (0, 0, {'attribute_id': cls.attribute1.id,
                        'value_ids': [(6, 0, [cls.value1.id,
                                              cls.value2.id])]})],
        })

    def test_product_configurator_attribute(self):

        # Set Extra price for value1
        self.product_attribute_price.create({
            'product_tmpl_id': self.product_template1.id,
            'value_id': self.value1.id,
            'price_extra': 100.00,
        })

        # create new product configuration attribute record.
        conf_attr = self.product_configuration_attribute.create({
            'product_tmpl_id': self.product_template1.id,
            'attribute_id': self.attribute1.id,
            'value_id': self.value1.id,
            'owner_model': 'product_product',
            'owner_id': 1
        })

        # Price Extra for conf_attr should be equal to 100.
        # Result OK.
        self.assertEqual(conf_attr.price_extra, 100.00)

        # Possible Values for the selected Attribute
        # should be equal to the value_ids set.
        # Result OK.
        self.assertEqual(conf_attr.possible_value_ids,
                         self.attribute1.value_ids)