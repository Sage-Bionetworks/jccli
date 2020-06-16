# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.jc_api_v2.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a utility library for the jumpcloud version 2 api

.. note::

    To learn more about the jumpcloud api 2
    `project website <https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv2>`_.
"""
import jcapiv2
from jcapiv2.rest import ApiException

from jccli.helpers import class_to_dict
from jccli.errors import GroupNotFoundError

VALID_USER_GROUP_TYPES = ['user', jcapiv2.GroupType.USER_GROUP]
VALID_SYSTEM_GROUP_TYPES = ['system', jcapiv2.GroupType.SYSTEM_GROUP]

class JumpcloudApiV2:
    """
        Wrapper for Jumpcloud API v2
    """
    def __init__(self, api_key):
        configuration = jcapiv2.Configuration()
        configuration.api_key['x-api-key'] = api_key
        self.graph_api = jcapiv2.GraphApi(jcapiv2.ApiClient(configuration))
        self.groups_api = jcapiv2.GroupsApi(jcapiv2.ApiClient(configuration))
        self.user_groups_api = jcapiv2.UserGroupsApi(jcapiv2.ApiClient(configuration))
        self.system_groups_api = jcapiv2.SystemGroupsApi(jcapiv2.ApiClient(configuration))
        self.bulk_job_requests_api = jcapiv2.BulkJobRequestsApi(jcapiv2.ApiClient(configuration))

    def create_group(self, name, type):
        """
        Create a Jumpcloud group
        :param name: The group name
        :param type: The group type, user or system
        :return: API response
        """
        group_name = name
        group_type = type

        if group_type in VALID_SYSTEM_GROUP_TYPES:
            try:
                body = jcapiv2.SystemGroupData(name=group_name)
                api_response = \
                    self.system_groups_api.groups_system_post(content_type='application/json',
                                                              accept='application/json',
                                                              body=body,
                                                              x_org_id='')
                return api_response
            except ApiException as error:
                raise "Exception when calling SystemGroupsApi->groups_system_post: %s\n" % error
        elif group_type in VALID_USER_GROUP_TYPES:
            try:
                body = jcapiv2.UserGroupPost(name=group_name)
                api_response = \
                    self.user_groups_api.groups_user_post(content_type='application/json',
                                                          accept='application/json',
                                                          body=body,
                                                          x_org_id='')
                return api_response
            except ApiException as error:
                raise "Exception when calling UserGroupsApi->groups_user_post: %s\n" % error
        else:
            raise ValueError("group type must be system or user")

    def delete_group(self, name):
        """
        Delete a Jumpcloud group
        :param name: The group name
        :return: API response
        """
        group_name = name
        group_id, group_type = self.get_group(group_name)

        if group_id is None:
            raise GroupNotFoundError("Group {} not found".format(name))

        if group_type == "system_group":
            try:
                api_response = \
                    self.system_groups_api.groups_system_delete(group_id,
                                                                content_type='application/json',
                                                                accept='application/json',
                                                                x_org_id='')
                return api_response
            except ApiException as error:
                raise "Exception when calling UserGroupsApi->groups_user_delete: %s\n" % error
        else:
            try:
                api_response = \
                    self.user_groups_api.groups_user_delete(group_id,
                                                            content_type='application/json',
                                                            accept='application/json',
                                                            x_org_id='')
                return api_response
            except ApiException as error:
                raise "Exception when calling UserGroupsApi->groups_user_delete: %s\n" % error

    def bind_user_to_group(self, user_id, group_id):
        """
        Associates a Jumpcloud user to a Jumpcloud group
        :param user_id:
        :param group_id:
        :return:
        """
        body = jcapiv2.UserGroupMembersReq(id=user_id,
                                           op="add",
                                           type="user")
        try:
            api_response = \
                self.graph_api.graph_user_group_members_post(group_id,
                                                             content_type='application/json',
                                                             accept='application/json',
                                                             body=body,
                                                             x_org_id='')
            return api_response
        except ApiException as error:
            raise "Exception when calling GraphApi->graph_user_group_members_post: %s\n" % error

    def bind_ldap_to_user(self, ldap_id):
        """
        Associates a Jumpcloud user to a Jumpcloud LDAP
        :param ldap_id:
        :return:
        """
        ldapserver_id = ldap_id
        body = jcapiv2.GraphManagementReq()
        try:
            api_response = \
                self.graph_api.graph_ldap_server_associations_post(ldapserver_id,
                                                                   content_type='application/json',
                                                                   accept='application/json',
                                                                   body=body,
                                                                   x_org_id='')
            return api_response
        except ApiException as error:
            raise "Exception when calling \
                   GraphApi->graph_ldap_server_associations_post: %s\n" % error

    def get_group(self, group_name, limit=100, skip=0, sort='', fields='', filter=''):
        # pylint: disable-msg=too-many-locals
        # pylint: disable-msg=too-many-arguments
        """
        Get the jumpcloud group info from a Jumpcloud group name
        :param group_name: name of the JC group
        :return:  The jumpcloud group id and type, NONE group is not found
        """
        groups = self.get_groups(limit, skip, sort, fields, filter)
        for group in groups:
            if group.name == group_name:
                return group.id, group.type
        return None, None

    def get_groups(self, limit=100, skip=0, sort='', fields='', filter=''):
        # pylint: disable-msg=too-many-locals
        # pylint: disable-msg=too-many-arguments
        """
        Get all jumpcloud groups
        :param group_name: name of the JC group
        :return: A list of jumpcloud groups
        """
        try:
            # response does not provide a total so set limit to max value
            results = self.groups_api.groups_list(content_type='application/json',
                                                  accept='application/json',
                                                  fields=fields,
                                                  filter=filter,
                                                  limit=limit,
                                                  skip=skip,
                                                  sort=sort,
                                                  x_org_id='')

            groups = class_to_dict(results)

            return groups
        except ApiException as error:
            raise "Exception when calling GroupsApi->groups_list: %s\n" % error
