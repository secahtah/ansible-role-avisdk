#!/usr/bin/python
#
# Created on Aug 25, 2016
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
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
module: avi_ipamdnsproviderprofile
author: Gaurav Rastogi (grastogi@avinetworks.com)

short_description: Module for setup of IpamDnsProviderProfile Avi RESTful Object
description:
    - This module is used to configure IpamDnsProviderProfile object
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
    allocate_ip_in_vrf:
        description:
            - If this flag is set, only allocate ip from networks in the virtual service vrf.
            - Field introduced in 17.2.4.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
    aws_profile:
        description:
            - Provider details if type is aws.
    azure_profile:
        description:
            - Provider details if type is microsoft azure.
            - Field introduced in 17.2.1.
    custom_profile:
        description:
            - Provider details if type is custom.
            - Field introduced in 17.1.1.
    gcp_profile:
        description:
            - Provider details if type is google cloud.
    infoblox_profile:
        description:
            - Provider details if type is infoblox.
    internal_profile:
        description:
            - Provider details if type is avi.
    name:
        description:
            - Name for the ipam/dns provider profile.
        required: true
    openstack_profile:
        description:
            - Provider details if type is openstack.
    proxy_configuration:
        description:
            - Field introduced in 17.1.1.
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    type:
        description:
            - Provider type for the ipam/dns provider profile.
            - Enum options - IPAMDNS_TYPE_INFOBLOX, IPAMDNS_TYPE_AWS, IPAMDNS_TYPE_OPENSTACK, IPAMDNS_TYPE_GCP, IPAMDNS_TYPE_INFOBLOX_DNS, IPAMDNS_TYPE_CUSTOM,
            - IPAMDNS_TYPE_CUSTOM_DNS, IPAMDNS_TYPE_AZURE, IPAMDNS_TYPE_INTERNAL, IPAMDNS_TYPE_INTERNAL_DNS, IPAMDNS_TYPE_AWS_DNS, IPAMDNS_TYPE_AZURE_DNS.
        required: true
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Uuid of the ipam/dns provider profile.
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
  - name: Create IPAM DNS provider setting
    avi_ipamdnsproviderprofile:
      controller: ''
      username: ''
      password: ''
      internal_profile:
        dns_service_domain:
        - domain_name: ashish.local
          num_dns_ip: 1
          pass_through: true
          record_ttl: 100
        - domain_name: guru.local
          num_dns_ip: 1
          pass_through: true
          record_ttl: 200
        ttl: 300
      name: Ashish-DNS
      tenant_ref: Demo
      type: IPAMDNS_TYPE_INTERNAL
'''
RETURN = '''
obj:
    description: IpamDnsProviderProfile (api/ipamdnsproviderprofile) object
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
        allocate_ip_in_vrf=dict(type='bool',),
        aws_profile=dict(type='dict',),
        azure_profile=dict(type='dict',),
        custom_profile=dict(type='dict',),
        gcp_profile=dict(type='dict',),
        infoblox_profile=dict(type='dict',),
        internal_profile=dict(type='dict',),
        name=dict(type='str', required=True),
        openstack_profile=dict(type='dict',),
        proxy_configuration=dict(type='dict',),
        tenant_ref=dict(type='str',),
        type=dict(type='str', required=True),
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
    return avi_ansible_api(module, 'ipamdnsproviderprofile',
                           set([]))

if __name__ == '__main__':
    main()
