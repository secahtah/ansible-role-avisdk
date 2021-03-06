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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: avi_useractivity
author: Gaurav Rastogi (grastogi@avinetworks.com)

short_description: Module for setup of UserActivity Avi RESTful Object
description:
    - This module is used to configure UserActivity object
    - more examples at U(https://github.com/avinetworks/devops)
requirements: [ avisdk ]
version_added: "2.3"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent","present"]
    concurrent_sessions:
        description:
            - Number of concurrent user sessions open.
            - Default value when not specified in API or module is interpreted by Avi Controller as 0.
    failed_login_attempts:
        description:
            - Number of failed login attempts before a successful login.
            - Default value when not specified in API or module is interpreted by Avi Controller as 0.
    last_login_ip:
        description:
            - Ip of the machine the user was last logged in from.
    last_login_timestamp:
        description:
            - Timestamp of last login.
    last_password_update:
        description:
            - Timestamp of last password update.
    logged_in:
        description:
            - Indicates whether the user is logged in or not.
    name:
        description:
            - Name of the user this object refers to.
    previous_password:
        description:
            - Stores the previous n passwords  where n is controllerproperties.max_password_history_count.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Unique object identifier of the object.
extends_documentation_fragment:
    - avi
'''

EXAMPLES = """
- name: Example to create UserActivity object
  avi_useractivity:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_useractivity
"""

RETURN = '''
obj:
    description: UserActivity (api/useractivity) object
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
        concurrent_sessions=dict(type='int',),
        failed_login_attempts=dict(type='int',),
        last_login_ip=dict(type='str',),
        last_login_timestamp=dict(type='str',),
        last_password_update=dict(type='str',),
        logged_in=dict(type='bool',),
        name=dict(type='str',),
        previous_password=dict(type='list',),
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
    return avi_ansible_api(module, 'useractivity',
                           set([]))

if __name__ == '__main__':
    main()
