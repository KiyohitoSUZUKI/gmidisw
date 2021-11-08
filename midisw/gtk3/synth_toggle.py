# -*- coding: utf-8 -*-
#
#
#
"""synth_toggle.py

   Yet another toggle button class

   Todo:
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import cairo
import math

######################################################################

class SynthToggle(Gtk.EventBox):
    
    def __init__(self, *args, **kwargs):
        super(SynthToggle, self).__init__(*args, **kwargs)

        self.toggle = False
        
        self.connect("button_press_event",self._on_button_pressed)
        self.connect("draw",self._on_draw)
        c = self.connect
        ca = self.connect_after

        self.connect = ca
        self.connect_after = c


    def _on_draw(self, widget, cr):
        w = self.get_allocated_width()
        h = self.get_allocated_height()

        if self.toggle:
            color_from = 1
            color_to = 0
        else:
            color_from = 0.4
            color_to = 0
            
        #
        # draw switch
        #
        cr.set_source_rgba(0,0,0, 0)
        ptn = cairo.LinearGradient(0,0, 0,h*0.75)
        ptn.add_color_stop_rgb(0,color_from+0.3,color_from+0.3,color_from+0.3)
        ptn.add_color_stop_rgb(1,color_to,color_to,color_to)
        cr.set_source(ptn)
        
        cr.rectangle(0,0,w,h*0.75)
        cr.fill()
        cr.stroke()

        #
        # draw ramp
        #
        #cr.rectangle(0,h*0.75,w,h*0.25)
        ptn = cairo.LinearGradient(0,h*0.75, w,h)
        cr.set_source(ptn)
        if self.toggle:
            color_from = 1
        ptn.add_color_stop_rgb(1,color_from,0,0)
        cr.arc(w/2,h*0.75 + h*0.20/2, (h*0.25/2)*0.6, 0 , math.pi*2)
        cr.fill()
        cr.stroke()

        #
        # draw edge
        #
        ptn = cairo.LinearGradient(0,0, w,h)
        cr.set_source(ptn)
        ptn.add_color_stop_rgb(1,0,0,0)
        cr.set_line_width(8.0)
        cr.rectangle(0,0,w,h)
        cr.stroke()


    def _on_button_pressed(self, widget,ev):
        self.toggle = not self.toggle
        self.queue_draw()

    def set_value(self, val):
        self.toggle = val
        self.queue_draw()

        return self

    def get_value(self):
        return self.toggle

######################################################################

class SynthToggleWithLabel(Gtk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.get_label_widget().set_line_wrap(True)

        self.btn = SynthToggle()
        self.add(self.btn)

    def set_value(self,val):
        self.btn.set_value(val)
        return self

    def get_value(self):
        return self.btn.get_value()

######################################################################

class SynthToggleBox(Gtk.Frame):
    SEPARATE_PAR = 4
    NEWLINE_PAR = 8

    def __init__(self, *args, **kwargs):
        if "labels" in kwargs:
            if isinstance(kwargs["labels"],list):
                labels = kwargs["labels"]
            else:
                labels = []
            del kwargs["labels"]

        super().__init__(*args, **kwargs)

        self.hboxes = []
        self.vbox = Gtk.VBox()
        self.add(self.vbox)
        
        self.buttons = []
        for lbl in labels:
            self.add_button(lbl)

        self.toggled_button = None

    def add_button(self, l):
        b = SynthToggleWithLabel(label=l)

        nth_hb = len(self.buttons) // self.NEWLINE_PAR

        if (len(self.buttons) % self.NEWLINE_PAR) == 0 :
            hb = Gtk.HBox()
            self.hboxes.append(hb)
            self.vbox.pack_start(hb,True,True,0)
        elif (len(self.buttons)  % self.SEPARATE_PAR) == 0:
           self.hboxes[nth_hb].pack_start(Gtk.VSeparator(),True,True,0)

        self.buttons.append(b)
        self.hboxes[nth_hb].pack_start(b,True,True,0)
        b.connect("button_press_event",self._on_button_pressed,len(self.buttons)-1)

        return self

    def _on_button_pressed(self,widget,ev,i):
        self.set_value(i)

        return self

    def set_value(self, num):
        if num == self.toggled_button:
            self.buttons[self.toggled_button].set_value(True)
            return self

        if not self.toggled_button is None:
            self.buttons[self.toggled_button].set_value(False)

        self.toggled_button = num
        self.buttons[num].set_value(True)

        return self

    def get_value(self):
        return self.toggled_button

##########################################

if __name__== "__main__":
    pass
