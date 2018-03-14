# sotd

Shakespeare of the Day

## Introduction

`sotd` outputs a randomly selected Shakespeare quote when invoked. It is also
a systemd service and writes it's output to /etc/motd once each day as well.

## Examples

JULIET - The Tragedy of Romeo and Juliet - Act II, Scene II

  Hist! Romeo, hist! O, for a falconer's voice,
  To lure this tassel-gentle back again!
  Bondage is hoarse, and may not speak aloud;
  Else would I tear the cave where Echo lies,
  And make her airy tongue more hoarse than mine,
  With repetition of my Romeo's name.


CORIOLANUS - The Tragedy of Coriolanus - Act III, Scene I

                    Thou wretch, despite o'erwhelm thee!
  What should the people do with these bald tribunes?
  On whom depending, their obedience fails
  To the greater bench: in a rebellion,
  When what's not meet, but what must be, was law,
  Then were they chosen: in a better hour,
  Let what is meet be said it must be meet,
  And throw their power i' the dust.


GONERIL - The Tragedy of King Lear - Act I, Scene III

  By day and night he wrongs me; every hour
  He flashes into one gross crime or other,
  That sets us all at odds: I'll not endure it:
  His knights grow riotous, and himself upbraids us
  On every trifle. When he returns from hunting,
  I will not speak with him; say I am sick:
  If you come slack of former services,
  You shall do well; the fault of it I'll answer.

## Installation and Use

Get the source and then make and install it (installation will overwrite
your `/etc/motd`):

    $ git clone https://github.com/dburggie/sotd.git
    $ cd sotd
    $ make
    $ sudo make install

Or, you can forego the installation and run it locally after building:

    $ git clone https://github.com/dburggie/sotd.git
    $ cd sotd
    $ make
    $ ./sotd

The latter case will not write to `/etc/motd`. After installation, invoking
`sotd` will print a random entry to `stdout`.

## Disabling the Systemd service

To disable the systemd service that writes to motd while keeping the program
installed to `/usr/bin`:

    $ sudo systemctl stop sotd.timer
    $ sudo systemctl disable sotd.timer

## Uninstall

To uninstall and disable the program and service:

    $ sudo make disable
    $ sudo make uninstall

