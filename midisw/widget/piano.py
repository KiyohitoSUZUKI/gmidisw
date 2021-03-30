#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import math

#######################################################
class Piano(Gtk.Bin):
    def __init__(self, orientation = Gtk.Orientation.HORIZONTAL):
        super(Piano, self).__init__()

        self.orientation = orientation
        self.connect("draw",self.on_draw)

    def on_draw(self, widget, cr):
        #if self.orientation == Gtk.Orientation.HORIZONTAL:
            w = self.get_allocated_width()
            h = self.get_allocated_height()
        #else:
        #    h = self.get_allocated_width()
        #    w = self.get_allocated_height()


        cr.rectangle(0,0,w,h)
        cr.line_to(w,h)
        cr.stroke()

        
#######################################################
if __name__=="__main__":
    def show_value(widget):
        print("value=%03d"%widget.get_value())

    top = Gtk.Window()

    p1 = Piano()
    p2 = Piano(orientation=Gtk.Orientation.VERTICAL)

    b = Gtk.VBox()
    
    b.add(p1)
    b.add(p2)
    top.add(b)
    top.set_size_request(640,120)
    top.connect("destroy",Gtk.main_quit)

    top.show_all()
    Gtk.main()
    