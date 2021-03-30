#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import math

##################################################################################

class Dial(Gtk.Frame):
    def __init__(self,min=0,max=255,initial_value=0, meter_scale=16,label=""):
        super(Dial, self).__init__(label=label)

        self.min = int(min)
        self.max = int(max)
        self.value = int(initial_value)

        self.mouth_size = 60 # degree
        self.meter_scale = int(meter_scale)
        self.meter_begin = 2*math.pi*((90+self.mouth_size/2)/360)
        self.meter_end =   2*math.pi*((360+90-self.mouth_size/2)/360)
        self.meter_range = (self.meter_end-self.meter_begin)

        self.connect("draw", self.on_draw)

        self.evb = Gtk.EventBox()
        self.add(self.evb)

        self.evb.connect("button_press_event", self.on_changed)
        self.evb.connect("button_release_event", self.on_changed)
        self.evb.connect("motion_notify_event",self.on_changed)

    def _get_center(self):
        return (self.get_allocated_width()/2,self.get_allocated_height()/2)

    def on_draw(self, widget, cr):
        cx,cy = self._get_center()

        maxr = cx if cy > cx else cy

        # mk meter_scale
        cr.set_line_width(0.5)
        cr.arc(cx, cy, maxr*0.6, self.meter_begin, self.meter_end )
        cr.stroke()

        for i in range(self.meter_scale+1):
            rad_i = self.meter_begin+self.meter_range*(i/self.meter_scale)
            cr.move_to(cx+maxr*0.6*math.cos(rad_i),cy+maxr*0.6*math.sin(rad_i))
            cr.line_to(cx+maxr*0.7*math.cos(rad_i),cy+maxr*0.7*math.sin(rad_i))
            cr.stroke()

        # mk dial
        cr.set_line_width(2)
        cr.arc(cx, cy, maxr*0.5, 0, 2*math.pi)
        cr.stroke()

        # draw value
        cr.set_line_width(5)
        rad = self.meter_begin + self.meter_range*self.value/self.max
        cr.move_to(cx+maxr*0.2*math.cos(rad),cy+maxr*0.2*math.sin(rad))
        cr.line_to(cx+maxr*0.5*math.cos(rad), cy+maxr*0.5*math.sin(rad))
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

        val = ((radadj - self.meter_begin)/self.meter_range)*self.max
        return int(val)


    def on_changed(self, widget, ev):
        self.value = self._get_value_from_xy(ev.x, ev.y)
        self.queue_draw()
        

    def get_value(self):
        return int(self.value)

    def set_value(self,value):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min

        self.value = int(value)
        self.queue_draw()

##################################################################################
class DialWithSpin(Gtk.Box):
    def __init__(self,**kwargs):
        super(DialWithSpin, self ).__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.dial = Dial(**kwargs)
        self.dial.set_size_request(64,64)
        self.dial.connect("button_press_event",self.on_changed)
        self.dial.connect("button_release_event",self.on_changed)
        self.dial.connect("motion_notify_event",self.on_changed)
        self.pack_start(self.dial, True, True, 0)

        self.spin = Gtk.SpinButton.new_with_range(self.dial.min, self.dial.max,1)
        self.spin.set_value(self.dial.get_value())
        self.spin.connect("value_changed",self.on_spinbutton_changed)
        self.pack_start(self.spin, True, True,0)

    def on_changed(self,widget,ev):
        self.dial.on_changed(widget,ev)
        self.spin.set_value(self.dial.get_value())

    def on_spinbutton_changed(self, spinbutton_inst):
        self.dial.set_value(self.spin.get_value())

    def set_value(self, value):
        self.dial.set_value(value)
        self.spin.set_value(value)

    def get_value(self):
        return self.dial.get_value()


##################################################################################

if __name__=="__main__":
    def show_value(widget):
        print("value=%03d"%widget.get_value())

    top = Gtk.Window()
#    d = Dial(initial_value=127, label="Test")
    d2 = DialWithSpin(initial_value=127, label="Test2")
#    top.add(d)
    top.add(d2)
#    top.set_size_request(64,128)
    top.connect("destroy",Gtk.main_quit)
    d2.spin.connect("value_changed",show_value)
    top.show_all()
    Gtk.main()
    
