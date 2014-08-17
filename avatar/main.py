#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import re

import avatar
import avatar.sources.favico
import avatar.sources.google
import avatar.sources.gravatar
import avatar.sources.local

import notmuch
import PIL.Image


def main():

    sources = [
        avatar.sources.google.Google(),
        avatar.sources.gravatar.Gravatar(),
        avatar.sources.local.Local(),
        avatar.sources.favico.Favico()
    ]

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

            for source in sources:
                print("Fetching using %s" % source.name)
                if source.fetch(email, target_image + '.temp') is True:
                    # Resizing the image
                    img = PIL.Image.open(target_image + '.temp')
                    img_small = img.resize((64, 64), PIL.Image.ANTIALIAS)
                    img_small.save(target_image, "PNG", quality=10,
                                   optimize=True, progressive=True)
                    os.remove(target_image + '.temp')
                    os.remove(target_image + '.lock')
                    break


if __name__ == '__main__':
    main()
