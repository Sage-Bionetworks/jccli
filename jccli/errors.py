# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.errors.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

Exceptions

"""

class JcCliError(Exception):
    """
    Base class for all JC CLI errors
    """

class SystemUserNotFoundError(JcCliError):
    """
    Jumpcloud system user is not found
    """

class GroupNotFoundError(JcCliError):
    """
    Jumpcloud group is not found
    """

class MissingRequiredArgumentError(JcCliError):
    """
    Required arguments are missing
    """
