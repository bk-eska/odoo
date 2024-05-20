# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models, tools


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text_tr(self, amount):

        def _convert_nnn_tr(val):
            single = ['Sıfır', 'Bir', 'İki', 'Üç', 'Dört',
                      'Beş', 'Altı', 'Yedi', 'Sekiz', 'Dokuz']
            tens = ['', 'On', 'Yirmi', 'Otuz', 'Kırk', 'Elli',
                    'Altmış', 'Yetmiş', 'Seksen', 'Doksan']
            word = ''
            digits = list(int(d) for d in "{0:03d}".format(val))
            if val == 0:
                return single[0]
            if digits[2] > 0:
                word = single[digits[2]]
            if digits[1] > 0:
                if word == '':
                    word = tens[digits[1]]
                else:
                    word = tens[digits[1]] + '-' + word
            if digits[0] > 0:
                if word == '':
                    word = u'Yüz'
                else:
                    word = u'Yüz' + '-' + word
            if digits[0] > 1:
                word = single[digits[0]] + '-' + word
            return word

        def turkish_number(val):
            denom = ['', 'Bin', 'Milyon', 'Milyar', 'Trilyon', 'Katrilyon',
                     'Kentilyon', 'Seksilyon', 'Septilyon', 'Oktilyon',
                     'Nonilyon', 'Desilyon', 'Undesilyon', 'Dodesilyon',
                     'Tredesilyon', 'Katordesilyon', 'Kendesilyon',
                     'Seksdesilyon', 'Septendesilyon', 'Oktodesilyon',
                     'Novemdesilyon', 'Vigintilyon']

            if val < 1000:
                return _convert_nnn_tr(val)
            if val < 2000:
                return u'Bin-' + _convert_nnn_tr(val % 1000)
            for (didx, dval) in ((v - 1, 1000 ** v)
                                 for v in range(len(denom))):
                if dval > val:
                    mod = 1000 ** didx
                    l = val // mod
                    r = val - (l * mod)
                    ret = _convert_nnn_tr(l) + '-' + denom[didx]
                    if r > 0:
                        ret = ret + ', ' + turkish_number(r)
                    return ret

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
                        amt_value=turkish_number(integer_value),
                        amt_word=self.currency_unit_label,
                        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + \
                            tools.ustr(' {amt_value} {amt_word}').format(
                                amt_value=turkish_number(fractional_value),
                                amt_word=self.currency_subunit_label,
                            )
        return amount_words

    def amount_to_text(self, amount):
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].search([('code', '=', lang_code)])
        if lang.iso_code == 'tr':
            return self.amount_to_text_tr(amount)
        else:
            return super(ResCurrency, self).amount_to_text(amount)


