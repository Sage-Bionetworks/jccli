# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.jc_api_v2.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a utility library for the jumpcloud version 2 api

.. note::

    To learn more about the jumpcloud api 2
    `project website <https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv2>`_.
"""
from typing import List

import jcapiv2
from jcapiv2 import Group, GraphConnection
from jcapiv2.rest import ApiException

from jccli.errors import GroupNotFoundError, JcApiException
from jccli.helpers import PAGE_LIMIT


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

        if group_type == jcapiv2.GroupType.SYSTEM_GROUP:
            try:
                body = jcapiv2.SystemGroupData(name=group_name)
                api_response = \
                    self.system_groups_api.groups_system_post(content_type='application/json',
                                                              accept='application/json',
                                                              body=body,
                                                              x_org_id='')
                return api_response
            except ApiException as error:
                raise JcApiException("Exception when calling SystemGroupsApi:\n") from error
        elif group_type == jcapiv2.GroupType.USER_GROUP:
            try:
                body = jcapiv2.UserGroupPost(name=group_name)
                api_response = \
                    self.user_groups_api.groups_user_post(content_type='application/json',
                                                          accept='application/json',
                                                          body=body,
                                                          x_org_id='')
                return api_response
            except ApiException as error:
                raise JcApiException("Exception when calling UserGroupsApi:\n") from error
        else:
            raise ValueError("group type must be system or user")

    def delete_group(self, group_id, group_type):
        """
        Delete a Jumpcloud group
        :param name: The group name
        :return: API response
        """
        if group_type == 'system_group':
            try:
                api_response = \
                    self.system_groups_api.groups_system_delete(group_id,
                                                                content_type='application/json',
                                                                accept='application/json',
                                                                x_org_id='')
                return api_response
            except ApiException as error:
                raise JcApiException("Exception when calling SystemGroupsApi:\n") from error
        elif group_type == 'user_group':
            try:
                api_response = \
                    self.user_groups_api.groups_user_delete(group_id,
                                                            content_type='application/json',
                                                            accept='application/json',
                                                            x_org_id='')
                return api_response
            except ApiException as error:
                raise JcApiException("Exception when calling UserGroupsApi:\n") from error

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
            raise JcApiException("Exception when calling GraphApi:\n") from error

    def unbind_user_from_group(self, user_id, group_id):
        body = jcapiv2.UserGroupMembersReq(id=user_id,
                                           op="remove",
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
            raise JcApiException("Exception when calling GraphApi:\n") from error

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
            raise JcApiException("Exception when calling GraphApi-:\n") from error

    def get_group(self, group_name, group_type, limit=100, skip=0, sort='', fields='', filter='') -> dict:
        # pylint: disable-msg=too-many-locals
        # pylint: disable-msg=too-many-arguments
        """
        Get the jumpcloud group info from a Jumpcloud group name
        :param group_name: name of the JC group
        :return:  The jumpcloud group id and type, NONE group is not found
        """
        groups = self.get_groups()
        for group in groups:
            if group['name'] == group_name and group['type'] == group_type:
                return group

    def get_groups(self, type=None) -> List[Group]:
        # pylint: disable-msg=too-many-locals
        # pylint: disable-msg=too-many-arguments
        """
        Get all jumpcloud groups
        :param group_name: name of the JC group
        :return: A list of jumpcloud groups
        """
        if type:
            # `filter` is poorly-documented (see https://github.com/TheJumpCloud/jcapi-python/issues/46) and possibly
            # not generalizable, but as long as the only thing we are filtering on is type, I suppose this will work
            # okay.
            filter = ['type:eq:%s' % (type,)]
        else:
            filter = ''
        try:
            # Iteratively make API calls until the API response is empty
            groups = []
            while True:
                results: List[Group] = self.groups_api.groups_list(
                    content_type='application/json',
                    accept='application/json',
                    filter=filter,
                    limit=PAGE_LIMIT,
                    skip=len(groups)
                )
                if len(results) == 0:
                    return groups
                groups.extend([group.to_dict() for group in results])
        except ApiException as error:
            raise JcApiException("Exception when calling GroupsApi:\n") from error

    def list_group_users(self, group_id):
        """Return a list of user IDs associated with the group ID
        """
        user_ids = []
        while True:
            results: List[GraphConnection] = self.user_groups_api.graph_user_group_members_list(
                group_id=group_id,
                content_type='application/json',
                accept='application/json',
                limit=PAGE_LIMIT,
                skip=len(user_ids)
            )
            if len(results) == 0:
                break
            user_ids.extend([result.to_dict()['to']['id'] for result in results])

        return user_ids
