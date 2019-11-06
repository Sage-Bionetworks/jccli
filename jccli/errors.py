# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.errors.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

Exceptions

"""

class SystemUserNotFoundError(Exception):
    """
    Jumpcloud system user is not found
    """

class UerGroupNotFoundError(Exception):
    """
    Jumpcloud user group is not found
    """

class MissingRequiredArgumentError(Exception):
    """
    Required arguments are missing
    """
