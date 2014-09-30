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

import hashlib
import urllib

import requests


class Gravatar(object):
    def __init__(self):
        self.name = "Gravatar"

    def fetch(self, email, target_image):
        size = 64

        avatar_url = "http://www.gravatar.com/avatar/"
        avatar_url += hashlib.md5(email.lower()).hexdigest() + "?"
        avatar_url += urllib.urlencode({'s': str(size)})

        size_of_empty_avatar = ['2174', '2197']
        content_length = requests.head(avatar_url).headers['content-length']
	print("content_length:%s " % content_length)

        if content_length in size_of_empty_avatar:
            return None

        print("fetching %s from %s to %s" % (email, avatar_url, target_image))
        try:
            urllib.urlretrieve(avatar_url, target_image)
            return True
        except IOError:
            print("Failed to download %s" % avatar_url)
            return None
