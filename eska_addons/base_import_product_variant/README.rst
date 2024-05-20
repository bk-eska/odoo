======================
Product Variant Import
======================


This module provides variant import functionality.

What is the format of the import file?
======================================

1) Each line contains a variant of a template

2) Each line contains three types of fields:

    - Field of a template (fields that doesn't start with "variant\_")
    - Special fields to describe which variant ("variant_id", "variant_attributes" and "variant_attribute_values")
    - Fields of the variant (fields that starts with "variant\_")

3) "variant_id" column is optional but can be used to set the external id of the variant.

4) "variant_attributes" field is '|' delimeted attribute list. Example: Color|Size

5) "variant_attribute_values" field is '|' delimeted attribute value list. Example: Red|XL


How it works?
=============

1) Import the file from products (templates), not the variants.

2) Do not select fields starting with "variant\_" during the import. They will be processed even if you don't select them.

3) When import button is hit, it will import the template first by ignoring variant columns. Then it will search for the variant using "variant_attributes" and "variant_attribute_values" columns and create it if it doesn't exist. Then it creates the external identifier and finally updates any field on variant with the columns that starts with "variant\_".

4) Once imported, you can refer to variants with external id later as needed.

