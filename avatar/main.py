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
import os
import re
import shutil
import urllib

import avatar

from lxml import html
import notmuch
import PIL.Image
import requests
import simplejson


def get_avatar_url_from_google(email):
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
        return None

    avatar_url = json['entry']['gphoto$thumbnail']['$t']

    size_of_empty_avatar = '1223'
    content_length = requests.head(avatar_url).headers['content-length']
    if content_length == size_of_empty_avatar:
        return None

    return avatar_url


def get_avatar_url_from_gravatar(email):
    size = 64

    avatar_url = "http://www.gravatar.com/avatar/"
    avatar_url += hashlib.md5(email.lower()).hexdigest() + "?"
    avatar_url += urllib.urlencode({'s': str(size)})

    size_of_empty_avatar = '2174'
    content_length = requests.head(avatar_url).headers['content-length']

    if content_length == size_of_empty_avatar:
        return None
    return avatar_url


def get_avatar_url_from_favico(email):
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
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
        print('Failed to query domain %s' % domain)
        return
    tree = html.fromstring(page.text.encode(encoding='UTF-8'))

    def get_icon_location():
        try:
            element = tree.xpath('/html/head/meta[@property="og:image"]')
            return(element[0].attrib['content'])
        except IndexError:
            pass

        try:
            element = tree.xpath('/html/head/link[@rel="apple-touch-icon"]')
            return(element[0].attrib['href'])
        except IndexError:
            pass

        try:
            element = tree.xpath(
                '/html/head/link[@rel="apple-touch-icon-precomposed"]')
            return(element[0].attrib['href'])
        except IndexError:
            pass

    icon_location = get_icon_location()

    if not icon_location:
        print("Failed to find icon for domain %s" % domain)
        return
    print(icon_location)
    if re.match('^//.*', icon_location):
        return("http:%s" % icon_location)
    elif re.match('^/.*', icon_location):
        return("http://%s%s" % (domain, icon_location))
    elif not re.match('^http.*', icon_location):
        return("http://%s/%s" % (domain, icon_location))
    else:
        return icon_location


def main():
    db = notmuch.Database()
    msgs = notmuch.Query(db, 'date:12months..today').search_messages()

    seen = []

    for msg in msgs:
        for email in avatar.EmailTools.extract_email_from_string(
                msg.get_header('From') +
                msg.get_header('Cc')):

            if email in seen:
                continue
            seen.append(email)

            if re.match('.*novalocal$', email):
                continue

            target_image = "%s/.emacs.d/avatar/%s.png" % (
                os.environ['HOME'], email)

            if os.path.exists(target_image + ".lock"):
                continue
            else:
                open(target_image + '.lock', 'a').close()

            print(" >%s" % email)

            avatar_url = get_avatar_url_from_google(email)
            if not avatar_url:
                avatar_url = get_avatar_url_from_gravatar(email)

            if not avatar_url:
                print("No URL for email: %s" % email)
                domain = avatar.EmailTools.get_domain_from_email(email)

                try:
                    shutil.copyfile(
                        "./icons/%s.png" % domain,
                        target_image + '.temp')
                    print("Using local icon for %s" % email)
                except Exception:
                    avatar_url = get_avatar_url_from_favico(email)

            if avatar_url:
                print("fetching %s from %s" % (email, avatar_url))
                try:
                    urllib.urlretrieve(avatar_url, target_image + '.temp')
                except IOError:
                    print("Failed to download %s" % avatar_url)
                    continue

            if os.path.exists(target_image + '.temp'):
                img = PIL.Image.open(target_image + '.temp')
                img_small = img.resize((64, 64), PIL.Image.ANTIALIAS)
                img_small.save(target_image, "PNG", quality=10,
                               optimize=True, progressive=True)
                os.remove(target_image + '.temp')
                os.remove(target_image + '.lock')

if __name__ == '__main__':
    main()
