#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Quick and Ugly script to fetch sender avatar.
# Copyright 2014 Gonéri Le Bouder <goneri@lebouder.net>
#
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
##
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

import re


class EmailTools(object):
    @staticmethod
    def extract_email_from_string(string):
        result = []
        try:
            for (m) in re.findall('([0-9a-zA-Z._-]+@[0-9a-zA-Z.-]+)',
                                  string):
                result.append(m.lower())
        except AttributeError:
            pass
        return result

    @staticmethod
    def get_domain_from_email(email):
        result = re.match('.*@([a-z0-9\.-]+)$', email)
        return(result.group(1))
