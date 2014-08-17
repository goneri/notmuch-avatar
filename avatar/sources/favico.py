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

from lxml import html
import requests

import avatar


class Favico(object):
    def __init__(self):
        self.name = "favico"

    def fetch(self, email, target_image):
        domain = avatar.EmailTools.get_domain_from_email(email)
        if not domain:
            return

        try:
            result = re.match('.*[@\.]([a-z0-9-]+\.[a-z0-9-]+)$', email)
            domain = result.group(1)
        except AttributeError:
            print("Failed to get domain from email %s" % email)
            return

        try:
            page = requests.get('http://www.%s' % domain)
        except (requests.exceptions.SSLError):
            print('SSLError on %s' % domain)
            return
        except (requests.exceptions.ConnectionError):
            print('Failed to query domain %s' % domain)
            return
        tree = html.fromstring(page.text.encode(encoding='UTF-8'))

        def get_raw_icon_location():
            try:
                el = tree.xpath('/html/head/meta[@property="og:image"]')
                return(el[0].attrib['content'])
            except IndexError:
                pass

            try:
                el = tree.xpath('/html/head/link[@rel="apple-touch-icon"]')
                return(el[0].attrib['href'])
            except IndexError:
                pass

            try:
                element = tree.xpath(
                    '/html/head/link[@rel="apple-touch-icon-precomposed"]')
                return(element[0].attrib['href'])
            except IndexError:
                pass

        raw_icon_location = get_raw_icon_location()

        if not raw_icon_location:
            print("Failed to find icon for domain %s" % domain)
            return

        print(raw_icon_location)
        if re.match('^//.*', raw_icon_location):
            icon_location = "http:%s" % raw_icon_location
        elif re.match('^/.*', icon_location):
            icon_location = "http://%s%s" % (domain, raw_icon_location)
        elif not re.match('^http.*', icon_location):
            icon_location = "http://%s/%s" % (domain, raw_icon_location)
        else:
            icon_location = raw_icon_location

        print("fetching %s from %s" % (email, icon_location))
        try:
            urllib.urlretrieve(icon_location, target_image + '.temp')
            return True
        except IOError:
            print("Failed to download %s" % icon_location)
