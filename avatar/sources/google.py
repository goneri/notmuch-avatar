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
import urllib

import requests
import simplejson


class Google(object):
    def __init__(self):
        self.name = "Google"

    def fetch(self, email, target_image):
        glogin = None
        try:
            result = re.match('(.+)@(gmail.com|enovance.com)', email)
            glogin = result.group(1)
            if result.group(2) != "gmail.com":
                glogin += "@"
                glogin += result.group(2)
            if not glogin:
                return
        except AttributeError:
            pass

        if not glogin:
            return

        response = requests.get(
            'http://picasaweb.google.com/data/entry/api/user/%s?alt=json'
            % glogin)
        try:
            json = response.json()
        except simplejson.scanner.JSONDecodeError:
            print("Failed to decode JSON for %s" % email)
            print("> %s" % response.text)
            return

        avatar_url = json['entry']['gphoto$thumbnail']['$t']

        size_of_empty_avatar = '1223'
        content_length = requests.head(avatar_url).headers['content-length']
        if content_length == size_of_empty_avatar:
            return None

        print("fetching %s from %s" % (email, avatar_url))
        try:
            urllib.urlretrieve(avatar_url, target_image + '.temp')
            return True
        except IOError:
            print("Failed to download %s" % avatar_url)
