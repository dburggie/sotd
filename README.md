# sotd

Shakespeare of the Day

## Introduction

`sotd` outputs a randomly selected Shakespeare quote when invoked. This project
also includes a `.timer` file that will write `sotd`'s output to `/etc/motd`
once per day.

## Installation and Use

Get the source and then build the project:

    $ git clone https://github.com/dburggie/sotd.git
    $ cd sotd
    $ make

From here, you can run the program locally:

    $ ./sotd
    
    JULIET - The Tragedy of Romeo and Juliet - Act II, Scene II
    
      Hist! Romeo, hist! O, for a falconer's voice,
      To lure this tassel-gentle back again!
      Bondage is hoarse, and may not speak aloud;
      Else would I tear the cave where Echo lies,
      And make her airy tongue more hoarse than mine,
      With repetition of my Romeo's name.
    

To install and run:

    $ sudo make install
    $ sotd
    
    CORIOLANUS - The Tragedy of Coriolanus - Act III, Scene I
     
                         Thou wretch, despite o'erwhelm thee!
      What should the people do with these bald tribunes?
      On whom depending, their obedience fails
      To the greater bench: in a rebellion,
      When what's not meet, but what must be, was law,
      Then were they chosen: in a better hour,
      Let what is meet be said it must be meet,
      And throw their power i' the dust.
    
    
To enable the systemd service files (this will write to `/etc/motd` immediately
and then again daily)

    $ sudo make enable
    $ cat /etc/motd
    
    GONERIL - The Tragedy of King Lear - Act I, Scene III
    
      By day and night he wrongs me; every hour
      He flashes into one gross crime or other,
      That sets us all at odds: I'll not endure it:
      His knights grow riotous, and himself upbraids us
      On every trifle. When he returns from hunting,
      I will not speak with him; say I am sick:
      If you come slack of former services,
      You shall do well; the fault of it I'll answer.


## Disabling and Uninstallation

To disable the systemd service, you can use `make`:

    $ sudo make disable

Alternately, with `systemctl`:

    $ sudo systemctl disable sotd.timer
    $ sudo systemctl stop sotd.timer
    
To uninstall (be sure to disable first):

    $ sudo make uninstall
