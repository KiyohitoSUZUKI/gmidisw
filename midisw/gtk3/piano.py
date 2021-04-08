# -*- coding: utf-8 -*-
#
#
#
"""Piano widget module

   Generic Piano widget module

   Todo:
     * fix Piano.get_note_number_from_xy(self, x, y):
        => some bug when note detaction 
     * add add to draw pressed-note mark when button_pressed event
     * add range selectable Piano widget class
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
        else:
            w_white_key = h / (self.keys * 7/12) # 7/12 = number of white key
            h_white_key = w

        return (w, h, w_white_key, h_white_key)            


    def _on_draw(self, widget, cr):
        w, h, w_white_key, h_white_key = self._get_wh()

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
                ww = w_white_key * (7 /12)
                hh = h_white_key * (7/12)
                fill = True

            if self.orientation == Gtk.Orientation.HORIZONTAL:
                cr.rectangle(ofs,0,ww,hh)
            else:
                if midisw.mididefs.is_white(i):
                    cr.rectangle(0,h-ofs-w_white_key,hh,ww)
                else:
                    cr.rectangle(0,h-ofs-w_white_key * self.black_key_mig - 1,hh,ww)

            if fill :
                cr.fill()

            cr.stroke()

    def get_note_number_from_xy(self, x, y):
        w, h,  w_white_key, h_white_key = self._get_wh()

        #
        # get normalized position
        #
        if self.orientation == Gtk.Orientation.HORIZONTAL:
            pos_normalized = x/w
        else:
            pos_normalized = (h - y)/h
            (x,y) = (y,x)

        #
        # get note value in float(num_keys * normalized position)  -> int
        #
        note_f = self.octave * 12 * pos_normalized    
        note = int(note_f)

        #
        # when pressd lowerside of keyboard
        #
        if (y > (h_white_key * self.black_key_mig)):
            #
            # when detected note == black, turn to white key
            #
            if midisw.mididefs.is_black(note):
                bx = w_white_key * (note - 1) * 7/12
                ex = w_white_key * (note - 1) * 7/12 + w_white_key 
                if  bx < x and x < ex:
                    note -= 1
                else:
                    note += 1

        return note + self.octave_offset*12

        
#######################################################
if __name__=="__main__":
    pass
