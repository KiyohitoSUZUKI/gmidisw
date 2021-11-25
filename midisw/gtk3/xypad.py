# -*- coding: utf-8 -*-
#
#
#
"""synth_xy_pad.py

   standard XY Pad

   Todo:
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import math

###############################################################

class XYPad(Gtk.EventBox):
    def __init__(self, *args, **kwargs):
        super(XYPad, self).__init__(*args,**kwargs)

        self.adj_x = Gtk.Adjustment(value = 64, lower=0, upper=127, step_increment = 1)
        self.adj_y = Gtk.Adjustment(value = 64, lower=0, upper=127, step_increment = 1)
        self.is_clicked = False

        self.connect("draw", self._on_draw)
        self.connect("button_press_event",self._on_pressed)
        self.connect("button_release_event",self._on_released)
        self.connect("motion_notify_event",self._on_motion_notified)

    def _on_draw(self,widget,cr):
        w = self.get_allocated_width()
        h = self.get_allocated_height()

        cr.set_source_rgba(0,0,0, 1)
        cr.set_line_width(8.0)
        cr.rectangle(0,0,w,h)
        cr.stroke()

        cr.set_line_width(2.0)
        cr.move_to(0,h/2)
        cr.line_to(w,h/2)
        cr.stroke()
        cr.move_to(w/2,0)
        cr.line_to(w/2,h)
        cr.stroke()

        posx,posy = self.get_value()
        ux = self.adj_x.get_upper()
        uy = self.adj_y.get_upper()
        lx = self.adj_x.get_lower()
        ly = self.adj_y.get_lower()

        posx = w*(posx/(ux - lx))
        posy = h*(posy/(uy - ly))
        cr.set_source_rgba(1,0,0, 1)
        cr.arc(posx,posy,w*0.05,0,2*math.pi)
        cr.fill()
        cr.stroke()

    def _set_value_from_xy(self,x,y):
        w = self.get_allocated_width()
        h = self.get_allocated_height()

        ux = self.adj_x.get_upper()
        uy = self.adj_y.get_upper()
        lx = self.adj_x.get_lower()
        ly = self.adj_y.get_lower()

        new_x = (x/w)*(ux-lx)
        new_y = (y/h)*(uy-ly)

        self.adj_x.set_value(new_x)
        self.adj_y.set_value(new_y)
        self.queue_draw()

    def _on_pressed(self,widget,ev):
        self._set_value_from_xy(ev.x,ev.y)
        self.is_clicked = True

    def _on_released(self,widget,ev):
        self._set_value_from_xy(ev.x,ev.y)
        self.is_clicked = False

    def _on_motion_notified(self,widget,ev):
        if self.is_clicked:
            self._set_value_from_xy(ev.x,ev.y)

    def get_value(self):
        return self.adj_x.get_value(), self.adj_y.get_value()
#        return self.adj_x.get_value(), self.adj_y.get_upper() - self.adj_y.get_value()
