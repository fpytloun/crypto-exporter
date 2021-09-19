#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Handles the zcha.in data and communication """

import logging
import requests
from ..lib import utils
from .connector import Connector

log = logging.getLogger('crypto-exporter')


class ZchainConnector(Connector):
    """ The ZchainConnector class """
    settings = {}
    params = {
        'addresses': {
            'key_type': 'list',
            'default': None,
            'mandatory': True,
        },
        'url': {
            'key_type': 'string',
            'default': 'https://api.zcha.in/v2',
            'mandatory': False,
        },
    }

    def __init__(self):
        self.exchange = 'zchain'
        self.params.update(super().params)  # merge with the global params
        self.settings = utils.gather_environ(self.params)
        super().__init__()

    def retrieve_accounts(self):
        """ Connects to the dcrdata API and retrieves the account information """
        if not self.settings['addresses']:
            return

        for address in self.settings['addresses']:
            url = f"{self.settings['url']}/mainnet/accounts/{address}"
            try:
                r = requests.get(url, timeout=self.settings['timeout']).json()
            except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout
            ) as e:
                log.warning(f"Can't connect to {self.settings['url']}. Exception caught: {utils.short_msg(e)}")

            balance = float(r.get('balance'))
            if not self._accounts.get('ZEC'):
                self._accounts.update({'ZEC': {}})
            self._accounts['ZEC'].update({
                address: balance,
            })
