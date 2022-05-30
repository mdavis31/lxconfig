#!/bin/sh

nmcli device wifi connect bustahcrib password classyship310

# touchpad
xinput set-prop "SynPS/2 Synaptics TouchPad" 310 1

# doom emacs
/usr/bin/emacs --daemon
