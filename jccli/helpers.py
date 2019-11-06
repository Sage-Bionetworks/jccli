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
    Get users from a file
    :param data_file:
    :return: a list of users
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
    Get groups from a file
    :param file:
    :return: a list of groups
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
    Get users from a file
    :param user_file:
    :return: a list of users
    """
    try:
        print(input)
        users = json.loads(input.replace("'", '"'))

        return users
    except (ValueError, TypeError, IOError) as error:
        raise error

def get_user_from_file(user_file):
    """
    Get users from a file
    :param user_file:
    :return: a list of users
    """
    try:
        with open(user_file, 'r') as file:
            users = json.load(file)

        return users
    except (ValueError, TypeError, IOError) as error:
        raise error
