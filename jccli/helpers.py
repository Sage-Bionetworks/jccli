# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.helpers.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a set of helper methods

"""

import json
import yaml


# Total number of results to allow in one API request
PAGE_LIMIT = 100


def class_to_dict(class_object):
    """
    Convert a list of jumpcloud users to a list of dicts
    """
    new_obj = []
    for item in class_object:
        new_obj.append(item)

    return new_obj


def make_query_filter(filter):
    """
    Turn a filter (dict, e.g. {'field1': 'value1', 'field2': 'value2'}) into an AND-joined filter for search requests in
    the JumpCloud API (e.g. {'and': [{'field1': 'value1'}, {'field2': 'value2'}]}).
    """
    query_filter = None
    if filter:
        query_items = []
        for field, value in filter.items():
            query_items.append({field: value})
        query_filter = {'and': query_items}
    return query_filter


def get_users_from_file(data_file):
    """
    Get users from a data file
    :param data_file:
    :return: a list of SystemUsers
    """
    users = []
    try:
        with open(data_file, 'r') as file:
            jc_config = yaml.safe_load(file)
            users = jc_config['users']

    except (KeyError) as error:
        pass
    except Exception as error:
        raise error

    return users


def get_groups_from_file(data_file):
    """
    Get groups from a data file
    :param data_file: data file
    :return: a list of jumpcloud groups
    """
    groups = []
    try:
        with open(data_file, 'r') as file:
            jc_config = yaml.safe_load(file)
            groups = jc_config['groups']

    except (KeyError) as error:
        pass
    except Exception as error:
        raise error

    return groups


def get_user_from_term(input):
    """
    Get user from an input string
    example:
     jccli create-user \
     --json "{\"email\": \"jc.tester1@sagebase.org\", \"username\": \"jctester1\"}"
    :param user_file:
    :return: a SystemUser
    """
    user = {}
    if input != "":
        try:
            user = json.loads(input.replace("'", '"'))

        except Exception as error:
            raise error

    return user


def get_user_from_file(user_file):
    """
    Get users from a file
    :param user_file:
    :return: a list of SystemUsers
    """
    user = {}
    try:
        with open(user_file, 'r') as file:
            user = json.load(file)

    except Exception as error:
        raise error

    return user
