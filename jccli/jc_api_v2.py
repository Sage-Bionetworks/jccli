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
from jccli.errors import UerGroupNotFoundError

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
        :param type: The group type
        :return: API response
        """
        group_name = name
        group_type = type
        content_type = 'application/json'
        accept = 'application/json'
        x_org_id = ''

        if group_type == "system":
            try:
                body = jcapiv2.SystemGroupData(name=group_name)
                api_response = self.system_groups_api.groups_system_post(content_type,
                                                                         accept,
                                                                         body=body,
                                                                         x_org_id=x_org_id)
                return api_response
            except ApiException as error:
                raise "Exception when calling SystemGroupsApi->groups_system_post: %s\n" % error
        else:
            try:
                body = jcapiv2.UserGroupPost(name=group_name)
                api_response = self.user_groups_api.groups_user_post(content_type,
                                                                     accept,
                                                                     body=body,
                                                                     x_org_id=x_org_id)
                return api_response
            except ApiException as error:
                raise "Exception when calling UserGroupsApi->groups_user_post: %s\n" % error

    def delete_group(self, name):
        """
        Delete a Jumpcloud group
        :param name: The group name
        :return: API response
        """
        group_name = name
        content_type = 'application/json'
        accept = 'application/json'
        x_org_id = ''
        group_id, group_type = self.get_group(group_name, limit=100)

        if group_id is None:
            raise UerGroupNotFoundError("User group {} not found".format(name))

        if group_type == "system_group":
            try:
                api_response = self.system_groups_api.groups_system_delete(group_id,
                                                                           content_type,
                                                                           accept,
                                                                           x_org_id=x_org_id)
                return api_response
            except ApiException as error:
                raise "Exception when calling UserGroupsApi->groups_user_delete: %s\n" % error
        else:
            try:
                api_response = self.user_groups_api.groups_user_delete(group_id,
                                                                       content_type,
                                                                       accept,
                                                                       x_org_id=x_org_id)
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
        content_type = 'application/json'
        accept = 'application/json'
        body = jcapiv2.UserGroupMembersReq(id=user_id,
                                           op="add",
                                           type="user")
        x_org_id = ''

        try:
            api_response = self.graph_api.graph_user_group_members_post(group_id,
                                                                        content_type,
                                                                        accept,
                                                                        body=body,
                                                                        x_org_id=x_org_id)
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
        content_type = 'application/json'
        accept = 'application/json'
        body = jcapiv2.GraphManagementReq()
        x_org_id = ''

        try:
            api_response = self.graph_api.graph_ldap_server_associations_post(ldapserver_id,
                                                                              content_type,
                                                                              accept,
                                                                              body=body,
                                                                              x_org_id=x_org_id)
            return api_response
        except ApiException as error:
            raise "Exception when calling \
                   GraphApi->graph_ldap_server_associations_post: %s\n" % error

    def get_group(self, group_name, limit=10):
        # pylint: disable-msg=too-many-locals
        """
        Get the jumpcloud group info from a Jumpcloud group name
        :param group_name:
        :param limit:
        :return:  The jumpcloud group id and type, NONE group is not found
        """
        content_type = 'application/json'
        accept = 'application/json'
        fields = ['[]']
        filter = ['[]']
        skip = 0
        sort = ['[]']
        x_org_id = ''

        group_id = None
        group_type = None
        try:
            results = self.groups_api.groups_list(content_type,
                                                  accept,
                                                  fields=fields,
                                                  filter=filter,
                                                  limit=limit,
                                                  skip=skip,
                                                  sort=sort,
                                                  x_org_id=x_org_id)

            groups = class_to_dict(results)

            for group in groups:
                if group['_name'] == group_name:
                    group_id = group['_id']
                    group_type = group['_type']

            return group_id, group_type
        except ApiException as error:
            raise "Exception when calling GroupsApi->groups_list: %s\n" % error
