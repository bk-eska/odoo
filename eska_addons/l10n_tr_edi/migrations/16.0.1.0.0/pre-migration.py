# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

field_renames = [
    ('res.company', 'res_company', 'edi_environment', 'l10n_tr_edi_environment'),
    ('res.partner', 'res_partner', 'party_identifiers', 'l10n_tr_party_identifiers'),
    ('res.partner', 'res_partner', 'party_identifiers', 'l10n_tr_party_identifiers'),
]

model_renames = [
    ("account.einvoice.identification", "l10n_tr.party.identification"),
    ("res.partner.party.identification", "l10n_tr.party.identification"),
]

def rename_fields(env, field):
    cr = env.cr
    cr.execute('SELECT name FROM ir_model_fields WHERE model=%s AND name=%s',
        (field[0], field[3]))
    if cr.fetchall():
        return
    cr.execute('SELECT name FROM ir_model_fields WHERE model=%s AND name=%s',
               (field[0], field[2]))
    if cr.fetchall():
        openupgrade.rename_fields(env, [field])

def rename_models(env, model):
    if openupgrade.table_exists(env.cr, model[0].replace('.', '_')) and \
            not openupgrade.table_exists(env.cr, model[1].replace('.', '_')):
        openupgrade.rename_models(env.cr, [(model[0], model[1])])
        openupgrade.rename_tables(env.cr, [(model[0].replace('.', '_'),
                                            model[1].replace('.', '_'))])


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    for model in model_renames:
        rename_models(env, model)
    for field in field_renames:
        rename_fields(env, field)
