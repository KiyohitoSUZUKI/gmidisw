#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import math

import midisw.gtk3


if __name__=="__main__":
    def show_value(widget):
        print("w1:value=%03d"%widget.get_value())

    def show_value2(widget):
        print("w2:value=%03d"%widget.get_value())
        
    def show_value3(widget):
        print("w3:value=%03d"%widget.get_value())

    top = Gtk.Window()
    hb = Gtk.HBox()

    d = midisw.gtk3.Dial(initial_value=127)
    d.set_size_request(64,64)
    d.connect("value_changed",show_value)

    d2 = midisw.gtk3.DialWithSpin(initial_value=127,label="testOfLabel")
    d2.connect("value_changed",show_value2)

    adj = Gtk.Adjustment(lower=0,upper=127,step_increment=1)
    d3 = midisw.gtk3.DialWithSpin()
    d3.set_adjustment(adj)
    adj.connect("value_changed",show_value3)

    hb.add(d)
    hb.add(d2)
    hb.add(d3)

    top.add(hb)
    top.set_size_request(240,128)
    top.connect("destroy",Gtk.main_quit)

    top.show_all()
    Gtk.main()
    
