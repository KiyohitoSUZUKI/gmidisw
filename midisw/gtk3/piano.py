# -*- coding: utf-8 -*-
#
#
#
"""Piano widget module

   Generic Piano widget module

   Todo:
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.mididefs

#######################################################
class Piano(Gtk.EventBox):
    """Piano...base class of Piano widget
    
    Attributes:
        orientation (Gtk.Orientation): draw virtical or horizontal, default=horizontal
        octave (int): how many octaves to draw
        octave_offset(int): how many octaves to offset, to adjust MIDI note

        keys(int): number of keys in piano
        black_key_mig: magnification of black key width from white key width
    """

    def __init__(self, octave=8, octave_offset = 1, orientation = Gtk.Orientation.HORIZONTAL):
        super(Piano, self).__init__()

        self.orientation = orientation
        self.octave = octave
        self.octave_offset = octave_offset
        self.keys = self.octave * 12
        self.black_key_mig = 7/12

        self.connect("draw",self._on_draw)


    def _get_wh(self):
        w = self.get_allocated_width()
        h = self.get_allocated_height()
        if self.orientation == Gtk.Orientation.HORIZONTAL:
            w_white_key = w / (self.keys * 7/12) # 7/12 = number of white key
            h_white_key = h
            return (w, h, w_white_key, h_white_key)            
        else:
            w_white_key = h / (self.keys * 7/12) # 7/12 = number of white key
            h_white_key = w
            return (h, w, w_white_key, h_white_key)


    def draw_piano(self, widget, cr):
        w, h, w_white_key, h_white_key = self._get_wh()

        cr.set_line_width(5.0)
        cr.set_source_rgba(0,0,0,1)
        white_cnt = 0
        for i in range(0, self.keys):
            ofs = 0
            fill = False

            if midisw.mididefs.is_white(i):
                ofs = w_white_key * white_cnt
                white_cnt += 1
                ww = w_white_key
                hh = h_white_key
            else:
                ofs = white_cnt * w_white_key - w_white_key * self.black_key_mig /2
                ww = w_white_key * self.black_key_mig
                hh = h_white_key * self.black_key_mig
                fill = True

            if self.orientation == Gtk.Orientation.HORIZONTAL:
                cr.rectangle(ofs,0,ww,hh)
            else:
                if midisw.mididefs.is_white(i):
                    cr.rectangle(0,w-ofs-w_white_key,hh,ww)
                else:
                    cr.rectangle(0,w-ofs-w_white_key * self.black_key_mig, hh, ww)

            if fill == True:
                cr.fill()

            cr.stroke()

    def draw_marker(self,widget,cr):
        pass

    def _on_draw(self, widget, cr):
        self.draw_piano(widget,cr)
        self.draw_marker(widget,cr)




    def get_note_number_from_xy_raw(self, x, y):
        w, h,  w_white_key, h_white_key = self._get_wh()

        #
        # get position by white_key
        #
        if self.orientation == Gtk.Orientation.HORIZONTAL:
            num_of_white_key = x//w_white_key
        else:
            (x,y) = (y,x)
            num_of_white_key = (w - x)//w_white_key

        #
        # detect note by white_key
        #
        oct = int(num_of_white_key // 7)
        note_in_curoct = midisw.mididefs._NOTES_WHITE[int(num_of_white_key%7)]

        note = oct * 12 + note_in_curoct

        #
        # when pressd upperside of keyboard
        #
        if (y < (h_white_key * self.black_key_mig)):
            u_bx = w_white_key * (num_of_white_key+1) - w_white_key * self.black_key_mig // 2
            u_ex = w_white_key * (num_of_white_key+1)
            l_bx = w_white_key * num_of_white_key
            l_ex = w_white_key * num_of_white_key     + w_white_key * self.black_key_mig // 2

            if self.orientation != Gtk.Orientation.HORIZONTAL:
                u_bx, u_ex, l_bx, l_ex = w - u_ex, w - u_bx, w - l_ex, w - l_bx

            ### print("#### x=%d:upr=(%d,%d),lwr=(%d,%d)"%(x,u_bx,u_ex,l_bx,l_ex))
            if note_in_curoct in [0,5]:      # if C or F => check right side
                if u_bx < x and x < u_ex:
                    note += 1
            elif note_in_curoct in [4,6]:    # if E or B => check left side
                if l_bx < x and x < l_ex:
                    note -= 1
            else:                            # else => check right and left both
                if u_bx < x and x < u_ex:
                    note += 1
                elif l_bx < x and x < l_ex:
                    note -= 1

        return note

    def get_note_number_from_xy(self, x, y):
        return self.get_note_number_from_xy_raw(x,y) + self.octave_offset*12

        
#######################################################
class PianoNoteSelector(Piano):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("button_press_event", self._on_pressed)
        self.connect("button_release_event", self._on_released)
        self.connect("motion_notify_event", self._on_motion_notified)

        self.marker_note_raw = None

    def _mark(self,cr,note):
            w, h,  w_white_key, h_white_key = self._get_wh()
            num_of_white_key = int(7*(note // 12))

            if midisw.mididefs.is_white(note):
                num_of_white_key +=  midisw.mididefs._NOTES_WHITE.index(note % 12)
                bx = num_of_white_key * w_white_key
                #by = h*0.75
                by = 0
                ww = w_white_key
                #hh = h*0.25
                hh = h
            else:
                num_of_white_key += midisw.mididefs._NOTES_WHITE.index((note+1) % 12)
                bx = num_of_white_key * w_white_key - w_white_key * self.black_key_mig / 2
                #by = h*0.75 * self.black_key_mig
                by = 0
                ww = w_white_key * self.black_key_mig
                #hh = h*0.25 * self.black_key_mig
                hh = h * self.black_key_mig

            cr.set_source_rgba(1,0,0,0.5)

            if self.orientation == Gtk.Orientation.HORIZONTAL:
                cr.rectangle(bx,by,ww,hh)
                retx, rety = bx, by
            else:
                if midisw.mididefs.is_white(note):  
                    cr.rectangle(by,w-bx-w_white_key,hh,ww)
                    retx, rety = by, w-bx-w_white_key
                else:                                        ## adjust when black-key
                    cr.rectangle(by, w-bx-w_white_key*self.black_key_mig,hh,ww)
                    retx, rety = by, w-bx-w_white_key*self.black_key_mig

            cr.fill()
            return retx,rety


    def draw_marker(self,widget,cr):
        if not self.marker_note_raw is None:
            self._mark(cr,self.marker_note_raw)

    def _on_pressed(self,widget,ev):
        self.marker_note_raw = self.get_note_number_from_xy_raw(ev.x,ev.y)
        self.queue_draw()

    def _on_motion_notified(self,widget,ev):
        if self.marker_note_raw is None:
            pass
        else:
            self.marker_note_raw = self.get_note_number_from_xy_raw(ev.x,ev.y)
            self.queue_draw()

    def _on_released(self,widget,ev):
        self.marker_note_raw = None
        self.queue_draw()

    def get_note_number(self):
        return self.marker_note_raw + self.octave_offset*12

    def get_note(self):
        return self.get_note_number()

#######################################################
class PianoNoteRangeSelector(PianoNoteSelector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("button_press_event", self._on_pressed)
        self.connect("button_release_event", self._on_released)
        self.connect("motion_notify_event", self._on_motion_notified)

        self.marker_note_raw = None
        self.marker_range_raw = [None,None]

    def draw_marker(self,widget,cr):
        if not (self.marker_range_raw[0] is None or self.marker_range_raw[1] is None):
            w,h,wk,hk = self._get_wh()

            bx,by = self._mark(cr,self.marker_range_raw[0])
            ex,ey = self._mark(cr,self.marker_range_raw[1])

            cr.set_line_width(10.0)

            if self.orientation == Gtk.Orientation.HORIZONTAL:
                cr.move_to(bx,by+h/2)
                cr.line_to(ex,ey+h/2)
            else:
                cr.move_to(bx+h/2,by)
                cr.line_to(ex+h/2,ey)

            cr.stroke()            

    def _adjust_range(self):
        if self.marker_note_raw is None:
            pass
        else:
            if self.marker_range_raw[0] is None:
                if self.marker_range_raw[1] is None:                   # when [None,None]
                    self.marker_range_raw[0] = self.marker_note_raw
                    self.marker_range_raw[1] = self.marker_note_raw
                else:                                                 # when [None,value]
                    if self.marker_range_raw[1] > self.marker_note_raw:
                        self.marker_range_raw[0] = self.marker_note_raw
                    else:
                        self.marker_range_raw[0] = self.marker_range_raw[1]
                        self.marker_range_raw[1] = self.marker_note_raw
            else:
                if self.marker_range_raw[1] is None:                   # when [value,None]
                    if self.marker_range_raw[0] > self.marker_note_raw:
                        self.marker_range_raw[1] = self.marker_range_raw
                        self.marker_range_raw[0] = self.marker_note_raw
                    else:
                        self.marker_range_raw[1] = self.marker_note_raw
                else:                                                 # when [value,value ]
                    diff_lwr = self.marker_range_raw[0] - self.marker_note_raw
                    diff_upr = self.marker_range_raw[1] - self.marker_note_raw
                    if abs(diff_lwr) < abs(diff_upr):                 # when cursor near by lower
                        self.marker_range_raw[0] = self.marker_note_raw
                    else:
                        self.marker_range_raw[1] = self.marker_note_raw


    def _on_pressed(self,widget,ev):
        self.marker_note_raw = self.get_note_number_from_xy_raw(ev.x,ev.y)
        self._adjust_range()
        self.queue_draw()

    def _on_motion_notified(self,widget,ev):
        if self.marker_note_raw is None:
            pass
        else:
            self.marker_note_raw = self.get_note_number_from_xy_raw(ev.x,ev.y)
            self._adjust_range()
            self.queue_draw()

    def _on_released(self,widget,ev):
        self.marker_note_raw = self.get_note_number_from_xy_raw(ev.x,ev.y)
        self._adjust_range()
        self.marker_note_raw = None
        self.queue_draw()

    def get_note_range(self):
        return self.marker_range_raw[0]+self.octave_offset*12, self.marker_range_raw[1]+self.octave_offset*12



#######################################################

if __name__=="__main__":
    pass
