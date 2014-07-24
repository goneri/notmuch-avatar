# notmuch-avatar

I use this script quick and derty with a hack in notmuch-emacs to show up the sender
avatar. It works even if I'm not proud of the code quality :).

Avaratar can be downloaded from:

* Google+
* Gravatar
* the domain large size favico

6620 icons use about 28MB of the hard drive.

### Screenshot

[An example of my emacs](notmuch.png)

### The patch

    diff --git a/emacs/notmuch-show.el b/emacs/notmuch-show.el
    index 529baa9..7456d8e 100644
    --- a/emacs/notmuch-show.el
    +++ b/emacs/notmuch-show.el
    @@ -947,6 +947,12 @@ useful for quoting in replies)."
             headers-start headers-end
             (bare-subject (notmuch-show-strip-re (plist-get headers :Subject))))
     
    +    (let* ((clean-address (notmuch-clean-address (plist-get headers :From)))
    +      (p-address (car clean-address))
    +      (p-name (cdr clean-address)))
    +      (insert-image (create-image (expand-file-name (concat "/home/goneri/.emacs.d/avatar/" p-address ".png" )) nil nil)))
    +
    +
         (setq message-start (point-marker))
     
         (notmuch-show-insert-headerline headers

## TODO

* code clean up
* configuration file
* use tox and unit-test

## blabla

Contact: Gonéri Le Bouder <goneri@lebouder.net>


            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004
    
     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
    
     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.
    
                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
    
      0. You just DO WHAT THE FUCK YOU WANT TO.
