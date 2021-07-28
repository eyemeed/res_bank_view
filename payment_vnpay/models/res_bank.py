# coding: utf-8

import logging
import hashlib
import urllib
# import urllib2

# from urllib import urlencode
from urllib.parse import urlencode
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.http import request
# from odoo.addons.queue_job.job import job

class ResBank(models.Model):
    _name = 'res.bank'
    _inherit = 'account.payment'

    def get_remote_addr(request):
        return request.httprequest.remote_addr

    def vnpay_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        tx_values = dict(values)

        reference_number = (values['reference'])
        data_query = {
            'vnp_Version': '2.0.0',
            'vnp_Command': 'pay',
            'vnp_OrderType': 'oldmc',
            'vnp_TmnCode': self.vnpay_website_code,
            'vnp_Amount':  int(float(values['amount'])*100),
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_CurrCode': 'VND',
            'vnp_Locale': 'vn',
            'vnp_OrderInfo': 'Thanh toan don hang %s' % reference_number,
            'vnp_ReturnUrl':  base_url + '/payment/vnpay/dpn/',
            'vnp_TxnRef':  reference_number,
            'vnp_IpAddr': request.httprequest.remote_addr
        }

        tx_values.update(data_query)

        return tx_values


