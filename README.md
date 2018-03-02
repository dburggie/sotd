# sotd

Shakespeare of the Day

## Introduction

`sotd` is a systemd service that writes to `/etc/motd` with a randomly 
selected shakespeare quote each day.

## Examples

to do

## Installation and Use

We'll get there when we get there. But in the interim, the plan is something
like this: 

    $ git clone https://github.com/dburggie/sotd.git
    $ cd sotd
    $ make
    $ sudo make install
    $ sudo systemctl enable sotd.timer
    $ sudo systemctl start sotd.timer

