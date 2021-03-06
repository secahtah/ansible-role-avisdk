#!/usr/bin/python
#
# Created on Aug 25, 2016
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
# Avi Version: 17.1.1
#
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
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: avi_ipaddrgroup
author: Gaurav Rastogi (grastogi@avinetworks.com)

short_description: Module for setup of IpAddrGroup Avi RESTful Object
description:
    - This module is used to configure IpAddrGroup object
    - more examples at U(https://github.com/avinetworks/devops)
requirements: [ avisdk ]
version_added: "2.4"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent", "present"]
    avi_api_update_method:
        description:
            - Default method for object update is HTTP PUT.
            - Setting to patch will override that behavior to use HTTP PATCH.
        default: put
        choices: ["put", "patch"]
    avi_api_patch_op:
        description:
            - Patch operation to use when using avi_api_update_method as patch.
        choices: ["add", "replace", "delete"]
    addrs:
        description:
            - Configure ip address(es).
    apic_epg_name:
        description:
            - Populate ip addresses from members of this cisco apic epg.
    country_codes:
        description:
            - Populate the ip address ranges from the geo database for this country.
    description:
        description:
            - User defined description for the object.
    ip_ports:
        description:
            - Configure (ip address, port) tuple(s).
    marathon_app_name:
        description:
            - Populate ip addresses from tasks of this marathon app.
    marathon_service_port:
        description:
            - Task port associated with marathon service port.
            - If marathon app has multiple service ports, this is required.
            - Else, the first task port is used.
    name:
        description:
            - Name of the ip address group.
        required: true
    prefixes:
        description:
            - Configure ip address prefix(es).
    ranges:
        description:
            - Configure ip address range(s).
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Uuid of the ip address group.
extends_documentation_fragment:
    - avi
'''



############################################################################
 # 
 # AVI CONFIDENTIAL
 # __________________
 # 
 # [2013] - [2017] Avi Networks Incorporated
 # All Rights Reserved.
 # 
 # NOTICE: All information contained herein is, and remains the property
 # of Avi Networks Incorporated and its suppliers, if any. The intellectual
 # and technical concepts contained herein are proprietary to Avi Networks
 # Incorporated, and its suppliers and are covered by U.S. and Foreign
 # Patents, patents in process, and are protected by trade secret or
 # copyright law, and other laws. Dissemination of this information or
 # reproduction of this material is strictly forbidden unless prior written
 # permission is obtained from Avi Networks Incorporated.
 ###

EXAMPLES = '''
  - name: Create an IP Address Group configuration
    avi_ipaddrgroup:
      controller: ''
      username: ''
      password: ''
      name: Client-Source-Block
      prefixes:
      - ip_addr:
          addr: 10.0.0.0
          type: V4
        mask: 8
      - ip_addr:
          addr: 172.16.0.0
          type: V4
        mask: 12
      - ip_addr:
          addr: 192.168.0.0
          type: V4
        mask: 16
'''
RETURN = '''
obj:
    description: IpAddrGroup (api/ipaddrgroup) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from avi.sdk.utils.ansible_utils import avi_common_argument_spec
    from pkg_resources import parse_version
    import avi.sdk
    sdk_version = getattr(avi.sdk, '__version__', None)
    if ((sdk_version is None) or (sdk_version and
            (parse_version(sdk_version) < parse_version('17.1')))):
        # It allows the __version__ to be '' as that value is used in development builds
        raise ImportError
    from avi.sdk.utils.ansible_utils import avi_ansible_api
    HAS_AVI = True
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        addrs=dict(type='list',),
        apic_epg_name=dict(type='str',),
        country_codes=dict(type='list',),
        description=dict(type='str',),
        ip_ports=dict(type='list',),
        marathon_app_name=dict(type='str',),
        marathon_service_port=dict(type='int',),
        name=dict(type='str', required=True),
        prefixes=dict(type='list',),
        ranges=dict(type='list',),
        tenant_ref=dict(type='str',),
        url=dict(type='str',),
        uuid=dict(type='str',),
    )
    argument_specs.update(avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (avisdk>=17.1) is not installed. '
            'For more details visit https://github.com/avinetworks/sdk.'))
    return avi_ansible_api(module, 'ipaddrgroup',
                           set([]))

if __name__ == '__main__':
    main()
