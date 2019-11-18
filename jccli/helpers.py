# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.helpers.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a set of helper methods

"""

import json

def class_to_dict(class_object):
    """
    Convert a jumpcloud class to a dictionary
    """
    result = []
    for item in class_object:
        result.append(item.__dict__)

    return result

def get_users_from_file(data_file):
    """
    Get users from a data file
    :param data_file:
    :return: a list of SystemUsers
    """
    try:
        with open(data_file, 'r') as file:
            jc_config = json.load(file)
            users = jc_config['users']

        return users
    except (ValueError, TypeError, IOError) as error:
        raise error

def get_groups_from_file(data_file):
    """
    Get groups from a data file
    :param data_file: data file
    :return: a list of jumpcloud groups
    """
    try:
        with open(data_file, 'r') as file:
            jc_config = json.load(file)
            groups = jc_config['groups']

        return groups
    except (ValueError, TypeError, IOError) as error:
        raise error

def get_user_from_term(input):
    """
    Get user from an input string
    :param user_file:
    :return: a SystemUser
    """
    try:
        print(input)
        user = json.loads(input.replace("'", '"'))

        return user
    except (ValueError, TypeError, IOError) as error:
        raise error

def get_user_from_file(user_file):
    """
    Get users from a file
    :param user_file:
    :return: a list of SystemUsers
    """
    try:
        with open(user_file, 'r') as file:
            user = json.load(file)

        return user
    except (ValueError, TypeError, IOError) as error:
        raise error
