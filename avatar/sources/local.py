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

import os
import shutil

import avatar


class Local(object):
    def __init__(self):
        self.name = "local"

    def fetch(self, email, target_image):
        domain = avatar.EmailTools.get_domain_from_email(email)

        icon_file = "./icons/%s.png" % domain

        try:
            shutil.copyfile(
                icon_file,
                target_image)
            print("Using local icon for %s" % email)
            return True
        except IOError:
            return False
