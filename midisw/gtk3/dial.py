# -*- coding: utf-8 -*-
#
#
#
"""Dial widget module

   Dial/knob widget module

   Todo:
"""


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import math

##################################################################################


class Dial(Gtk.Range):


    def __init__(self,min=0,max=127,initial_value=0, meter_scale=12):
        super().__init__()

        self.set_adjustment( Gtk.Adjustment(value=initial_value,lower=min,upper=max,step_increment=1) )
        self.button_pressed = False

        self.mouth_size = 60 # degree
        self.meter_scale = int(meter_scale)
        self.meter_begin = 2*math.pi*((90+self.mouth_size/2)/360)
        self.meter_end =   2*math.pi*((360+90-self.mouth_size/2)/360)
        self.meter_range = (self.meter_end-self.meter_begin)

        self.connect("draw", self._on_draw)
        self.connect("button_press_event", self._on_pressed)
        self.connect("button_release_event", self._on_released)
        self.connect("motion_notify_event",self._on_motion_notified)

    def _get_center(self):
        return (self.get_allocated_width()/2,self.get_allocated_height()/2)

    def _on_draw(self, widget, cr):
        cx,cy = self._get_center()

        maxr = cx if cy > cx else cy

        # mk meter_scale
        cr.set_line_width(0.5)
        cr.arc(cx, cy, maxr*0.6, self.meter_begin, self.meter_end)
        cr.stroke()

        for i in range(self.meter_scale+1):
            rad_i = self.meter_begin+self.meter_range*(i/self.meter_scale)
            c = math.cos(rad_i)
            s = math.sin(rad_i)
            cr.move_to(cx+maxr*0.6*c,cy+maxr*0.6*s)
            cr.line_to(cx+maxr*0.7*c,cy+maxr*0.7*s)
            cr.stroke()

        # mk dial
        cr.set_line_width(2)
        cr.arc(cx, cy, maxr*0.5, 0, 2*math.pi)
        cr.stroke()

        # draw value
        cr.set_line_width(5)
        rad = self.meter_begin + self.meter_range*self.get_adjustment().get_value()/self.get_adjustment().get_upper()
        c = math.cos(rad)
        s = math.sin(rad)
        cr.move_to(cx+maxr*0.2*c,cy+maxr*0.2*s)
        cr.line_to(cx+maxr*0.5*c, cy+maxr*0.5*s)
        cr.stroke()

    def _get_value_from_xy(self, posx, posy):
        cx,cy = self._get_center()
        vx,vy = (posx-cx,posy-cy)

        radadj =  math.atan2(vy,vx ) 

        if radadj < 0 :
            radadj += 2*math.pi
        if radadj > 0 and radadj < (1./2.)*math.pi:
            radadj += 2*math.pi
        
        if radadj <= self.meter_begin:
            radadj = self.meter_begin
        if radadj > self.meter_end:
            radadj = self.meter_end

        val = ((radadj - self.meter_begin)/self.meter_range)*self.get_adjustment().get_upper()
        return int(val)

    def _set_and_queue_draw(self, widget, ev):
        self.set_value( self._get_value_from_xy(ev.x, ev.y) )
        self.queue_draw()
    
    def _on_pressed(self, widget, ev):
        self.button_pressed = True
        self._set_and_queue_draw(widget, ev)

    def _on_released(self, widget, ev):
        self.button_pressed = False
        self._set_and_queue_draw(widget, ev)

    def _on_motion_notified(self, widget, ev):
        if self.button_pressed is True:
            self._set_and_queue_draw(widget,ev)


##################################################################################
class DialWithSpin(Gtk.VBox):
    def __init__(self,**kwargs):
        super().__init__()

        if "label" in kwargs.keys():
            self.label = Gtk.Label(label=kwargs["label"])
            self.pack_start(self.label,False,False,0)
            del(kwargs["label"])

        self.dial = Dial(**kwargs)
        self.pack_start(self.dial, True, True, 0)

        self.spin = Gtk.SpinButton()
        self.spin.set_adjustment(self.dial.get_adjustment())
        self.pack_start(self.spin, False, False,0)

    """
    なんぼhas-a関係とはいえ、以下の実装はダサいけど、とりあえずそのままにする
    """
    def connect(self,signame,func):
        self.dial.connect(signame,func)
        self.spin.connect(signame,func)

    def set_adjustment(self, adjustment):
        self.dial.set_adjustment(adjustment)
        self.spin.set_adjustment(adjustment)

    def get_adjustment(self):
        return self.dial.get_adjustment()

    def set_value(self, value):
        self.dial.set_value(value)

    def get_value(self):
        return self.dial.get_value()


##################################################################################

if __name__=="__main__":
    pass
