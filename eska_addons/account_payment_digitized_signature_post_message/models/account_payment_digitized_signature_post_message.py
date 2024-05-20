from odoo import models, Command, fields, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_account_unsign(self):
        res = super(AccountPayment, self).action_account_unsign()
        self.signature = False
        self.message_post(
            body=_('Payment unsigned'),
        )
        return res

    def write(self, vals):
        res = super(AccountPayment, self).write(vals)
        if vals.get('signature'):
            for account in self:
                account._attach_sign()
        return res

    def _attach_sign(self):
        self.ensure_one()
        report = self.env['ir.actions.reports']._render_qweb_pdf("account.action_report_payment_receipt", self.id)
        filename = "%s_signed_payment" % self.name
        if self.partner_id:
            message = _('Payment signed by %s') % (self.partner_id.name)
        else:
            message = _('Payment signed')
        self.message_post(
            attachments=[('%s.pdf' % filename, report[0])],
            body=message,
        )

