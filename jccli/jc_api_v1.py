# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.jc_api_v1.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a utility library for the jumpcloud version 1 api

.. note::

    To learn more about the jumpcloud api 1
    `project website <https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv1>`_.
"""
from distutils.util import strtobool

import jcapiv1
from jcapiv1 import Systemuserput, Systemput
from jcapiv1.rest import ApiException
from jccli.errors import SystemUserNotFoundError, JcApiException
from jccli.helpers import class_to_dict, make_query_filter


# pylint: disable=too-many-arguments
class JumpcloudApiV1:
    """
        Wrapper for Jumpcloud API v1
    """
    def __init__(self, api_key):
        configuration = jcapiv1.Configuration()
        configuration.api_key['x-api-key'] = api_key
        self.system_users_api = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))
        self.systems_api = jcapiv1.SystemsApi(jcapiv1.ApiClient(configuration))
        self.search_api = jcapiv1.SearchApi(jcapiv1.ApiClient(configuration))

    def retrieve_users(self, user_ids=[]):
        """
        Retrieve a list of users corresponding to ids
        """
        # FIXME: This is not an ideal way to do this, but search_systemusers_post doesn't seem to allow filtering on ID
        all_users = self.get_users()
        return [user for user in all_users if user['id'] in user_ids]

    def search_users(self, filter={}):
        """
        Search for users on JumpCloud. `filter` can contain values for multiple fields, which will be combined with an
        AND operator.

        :param filter: (dict) an object used to filter search results for various fields. E.g.: `{"firstname": "David",
                       "lastname": "Smith"}` will search for a user with first name "David" and last name "Smith".
        :return: List[SystemUser]
        """
        query_filter = make_query_filter(filter)

        try:
            api_response = self.search_api.search_systemusers_post(
                content_type='application/json',
                accept='application/json',
                body={
                    'filter': query_filter
                }
            )
            users = [user.to_dict() for user in api_response.results]
            return users
        except ApiException as error:
            raise JcApiException("Exception when calling SystemusersApi:\n") from error

    def get_users(self, limit='100', skip=0, search='', filter='', sort='', fields=''):
        """
        Get users from jumpcloud
        :param limit:
        :param skip:
        :param search:
        :param filter:
        :param sort:
        :param fields:
        :return: a list of users with dict of settings
        """
        try:
            api_response = self.system_users_api.systemusers_list(content_type='application/json',
                                                                  accept='application/json',
                                                                  limit=limit,
                                                                  skip=skip,
                                                                  sort=sort,
                                                                  fields=fields,
                                                                  x_org_id='',
                                                                  search=search,
                                                                  filter=filter)
            users = [user.to_dict() for user in class_to_dict(api_response.results)]
            return users
        except ApiException as error:
            raise JcApiException("Exception when calling SystemusersApi:\n") from error

    def create_user(self, systemuser):
        """
        Create a new user in jumpcloud
        :param systemuser: a dictoionary of Systemuser properties
               https://github.com/TheJumpCloud/jcapi-java/blob/master/jcapiv1/docs/Systemuser.md
        :return: The api response
        """
        body = jcapiv1.Systemuserputpost(username=systemuser['username'],
                                         email=systemuser['email'],
                                         firstname=systemuser.get('firstname', ''),
                                         lastname=systemuser.get('lastname', ''),
                                         allow_public_key=strtobool(
                                             systemuser.get('allow_public_key', 'True')),
                                         ldap_binding_user=strtobool(
                                             systemuser.get('ldap_binding_user', 'False')),
                                         passwordless_sudo=strtobool(
                                             systemuser.get('passwordless_sudo', 'False')),
                                         sudo=strtobool(systemuser.get('sudo', 'False')))
        try:
            api_response = self.system_users_api.systemusers_post(content_type='application/json',
                                                                  accept='application/json',
                                                                  body=body,
                                                                  x_org_id='')
            return api_response.to_dict()
        except ApiException as error:
            # FIXME: What should this behavior actually be?
            raise JcApiException("Exception when calling SystemusersApi->systemusers_post: %s\n" % error)

    def delete_user(self, username):
        """
        Delete a user from jumpcloud
        :param id: The jumpcloud id of the user
        :return:
        """
        user_id = self.get_user_id(username)
        if user_id is None:
            raise SystemUserNotFoundError(f"System user {username} not found")

        try:
            api_response = self.system_users_api.systemusers_delete(user_id,
                                                                    content_type='application/json',
                                                                    accept='application/json',
                                                                    x_org_id='')
            return api_response
        except ApiException as error:
            raise JcApiException("Exception when calling SystemusersApi\n") from error

    def get_user_id(self, username):
        """
        Get the jumpcloud user id from the user name
        :param username
        :return:  the user id
        """
        users = self.get_users(limit='', fields="username")

        for user in users:
            if user['username'] == username:
                return user['id']

        raise SystemUserNotFoundError('No user found for username: %s' % (username,))

    def get_user(self, username):
        """
        Get detail view of a user object.
        :param user_id:
        :return: user properties dict
        """
        # FIXME: As soon as we figure out how the `filter` parameter works on systemusers_list(), we should start
        #  filtering based on username
        users = self.system_users_api.systemusers_list(
            accept='application/json',
            content_type='application/json'
        ).results

        for user in users:
            if user.username == username:
                return user.to_dict()

        raise SystemUserNotFoundError('No user found for username: %s' % (username,))

    def set_user(self, username, attributes):
        user_id = self.get_user_id(username)
        api_response = self.system_users_api.systemusers_put(
            accept='application/json',
            content_type='application/json',
            id=user_id,
            body=Systemuserput(**attributes)
        )
        return api_response.to_dict()

    def search_systems(self, filter={}):
        """
        Search for systems on JumpCloud. `filter` can contain values for multiple fields, which will be combined with an
        AND operator.

        :param filter: (dict) an object used to filter search results for various fields. E.g.: `{"active":
                       True, "os": "ubuntu-20.04"}` will search for a system that is active and has the operating system
                       "ubuntu-20.04".
        :return: List[System]
        """
        query_filter = make_query_filter(filter)

        try:
            api_response = self.search_api.search_systems_post(
                content_type='application/json',
                accept='application/json',
                body={
                    'filter': query_filter
                }
            )
            systems = [system.to_dict() for system in api_response.results]
            return systems
        except ApiException as error:
            raise JcApiException("Exception when calling SearchApi:\n") from error

    def get_system(self, system_id):
        """
        Get detail view of a system.
        :param system_id: the id of the system
        :return: system properties dict
        """
        system = self.systems_api.systems_get(
            content_type='application/json',
            accept='application/json',
            id=system_id
        )

        return system.to_dict()

    def set_system(self, system_id, attributes):
        """
        Set attributes of system with the given system ID.
        :param system_id: the id of the system
        :param attributes: dictionary of attributes to be updated
        :return: system properties dict
        """
        response = self.systems_api.systems_put(
            id=system_id,
            accept='application/json',
            content_type='application/json',
            body=Systemput(**attributes)
        )
        return response.to_dict()

    def delete_system(self, system_id):
        """
        Delete a system with the given ID.
        :param system_id: the id of the system
        :return: System object that was deleted
        """
        try:
            response = self.systems_api.systems_delete(
                id=system_id,
                accept='application/json',
                content_type='application/json'
            )
            return response
        except ApiException as error:
            raise JcApiException("Exception when calling SystemApi:\n") from error
