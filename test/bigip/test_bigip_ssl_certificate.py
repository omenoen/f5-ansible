#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2017 F5 Networks Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import patch
from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes
from ansible.module_utils.f5_utils import (
    AnsibleF5Client
)
from library.bigip_ssl_certificate import (
    KeyParameters,
    CertParameters,
    ModuleManager,
    ArgumentSpec
)


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters_key(self):
        key_content = load_fixture('create_insecure_key1.key')
        args = dict(
            key_content=key_content,
            name="cert1",
            partition="Common",
            state="present",
            password='password',
            server='localhost',
            user='admin'
        )
        p = KeyParameters(args)
        assert p.name == 'cert1'
        assert p.key_filename == 'cert1.key'
        assert '-----BEGIN RSA PRIVATE KEY-----' in p.key_content
        assert '-----END RSA PRIVATE KEY-----' in p.key_content
        assert p.key_checksum == '91bdddcf0077e2bb2a0258aae2ae3117be392e83'
        assert p.state == 'present'
        assert p.user == 'admin'
        assert p.server == 'localhost'
        assert p.password == 'password'
        assert p.partition == 'Common'

    def test_module_parameters_cert(self):
        cert_content = load_fixture('create_insecure_cert1.crt')
        args = dict(
            cert_content=cert_content,
            name="cert1",
            partition="Common",
            state="present",
            password='password',
            server='localhost',
            user='admin'
        )
        p = CertParameters(args)
        assert p.name == 'cert1'
        assert p.cert_filename == 'cert1.crt'
        assert 'Signature Algorithm' in p.cert_content
        assert '-----BEGIN CERTIFICATE-----' in p.cert_content
        assert '-----END CERTIFICATE-----' in p.cert_content
        assert p.cert_checksum == '1e55aa57ee166a380e756b5aa4a835c5849490fe'
        assert p.state == 'present'
        assert p.user == 'admin'
        assert p.server == 'localhost'
        assert p.password == 'password'
        assert p.partition == 'Common'

#    def test_api_parameters(self):
#        args = dict(
#            name='foo',
#            community='public',
#            host='10.10.10.10',
#            network='other',
#            version=1,
#            port=1000
#        )
#        p = Parameters(args)
#        assert p.name == 'foo'


#class TestManager(unittest.TestCase):
#
#    def setUp(self):
#        self.spec = ArgumentSpec()
#
#    @patch('ansible.module_utils.f5_utils.AnsibleF5Client._get_mgmt_root',
#           return_value=True)
#    def test_create_trap(self, *args):
#        set_module_args(dict(
#            name='foo',
#            snmp_version='1',
#            community='public',
#            destination='10.10.10.10',
#            port=1000,
#            network='other',
#            password='password',
#            server='localhost',
#            user='admin'
#        ))
#
#        client = AnsibleF5Client(
#            argument_spec=self.spec.argument_spec,
#            supports_check_mode=self.spec.supports_check_mode,
#            f5_product_name=self.spec.f5_product_name
#        )
#        mm = ModuleManager(client)
#
#        # Override methods to force specific logic in the module to happen
#        mm.exit_json = lambda x: False
#        mm.create_on_device = lambda: True
#        mm.exists = lambda: False
#
#        results = mm.exec_module()
#
#        assert results['changed'] is True