#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.mididefs
import midisw.gtk3.synth_tone_selector

##################################

if __name__== "__main__":
    win = Gtk.Window()
    tonesel = mididefs.gtk3.ToneSelector()
    win.add(tonesel)
    win.set_size_request(200,64)
    win.show_all()
    connect("destroy",Gtk.main_quit)

    Gtk.main()
