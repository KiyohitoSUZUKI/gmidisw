import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import midisw.tonenamedb

class ToneSelector(Gtk.Window):
    WIDTH=320
    HEIGHT=768

    def __init__(self, label="", db=midisw.tonenamedb.Base(),selected=(0,0,0)):
        super().__init__()
        self.db = db
        self.sel_init = db.ls(selected[0],selected[1],selected[2])[0]
        self.sel = self.sel_init

        self.liststore = Gtk.ListStore(int,int,int,str,str)
        nth = 0
        for t in self.db.ls():
            self.liststore.append(t)
            if (t[0],t[1],t[2]) == (self.sel_init[0],self.sel_init[1],self.sel_init[2]):
                self.sel_init_nth = nth
            nth += 1

        self.set_size_request(self.WIDTH,self.HEIGHT)
        self.vbox = Gtk.VBox()
        self.add(self.vbox)

        self.label = Gtk.Label()
        self.label.set_text(label)
        self.vbox.pack_start(self.label, False,False, 0)

        self.label_selected = Gtk.Label()
        self.vbox.pack_start(self.label_selected, False, False, 0)

        self.scrollw = Gtk.ScrolledWindow()
        self.vbox.pack_start(self.scrollw, True,True, 0)

        self.treeview = Gtk.TreeView(model = self.liststore)
        self.scrollw.add(self.treeview)
        self.treeview.set_vexpand(True)
        self.treeview.set_hexpand(True)

        self.column = {}
        cno = 0
        for c in ["bankmsb","banklsb","prog","gname","tname"]:
            rend = Gtk.CellRendererText()
            if c in ["gname","tname"]:
                rend.set_property("editable", True)
                if c == "gname":
                    rend.connect("edited", self.on_gname_editted)
                else:
                    rend.connect("edited", self.on_tname_editted)

            self.column[c] = Gtk.TreeViewColumn(c)
            self.column[c].pack_start(rend,True)
            self.column[c].set_property("resizable", True)
            self.column[c].add_attribute(rend,"text",cno)
            self.treeview.append_column(self.column[c])

            cno += 1
        self.treeview.get_selection().connect("changed", self.on_changed)

        self.treeview.set_cursor(self.sel_init_nth)
        self.treeview.scroll_to_cell(str(self.sel_init_nth))

        self.hbox = Gtk.HBox()
        self.vbox.pack_end(self.hbox,False,False,0)

        self.btn_cancel = Gtk.Button.new_with_label("Cancel")
        self.hbox.add(self.btn_cancel)
        self.btn_cancel.connect("clicked",self.on_cancel_clicked)

        self.btn_ok = Gtk.Button.new_with_label("OK")
        self.hbox.add(self.btn_ok)
        self.btn_ok.connect("clicked",self.on_ok_clicked)

    # ==================================================
    def on_cancel_clicked(self,w):
        self.sel = self.sel_init
        self.emit("destroy")

    def on_ok_clicked(self,w):
        self.emit("destroy")

    # ==================================================
    def update_label(self):
        self.label_selected.set_text("%u,%u,%u:%s/%s"%(self.sel[0],
                                                       self.sel[1],
                                                       self.sel[2],
                                                       self.sel[3],
                                                       self.sel[4]))

    def on_changed(self, selection):
        m, it = selection.get_selected()
        self.sel = m[it]
        self.update_label()
        
    # ==================================================
    def on_gname_editted(self,rederer,path,new_text):
        self.liststore[path][3] = new_text
        self.sel[3] = new_text
        l = self.liststore[path]
        self.db.set_name(l[0],l[1],l[2], "gname",new_text)
        self.update_label()

    def on_tname_editted(self,rederer,path,new_text):
        self.liststore[path][4] = new_text
        self.sel[4] = new_text
        l = self.liststore[path]
        self.db.set_name(l[0],l[1],l[2], "tname",new_text)
        self.update_label()


##########################################################################
##########################################################################

if __name__=="__main__":
#    tndb = midisw.tonenamedb.SoundFont("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    tndb = midisw.tonenamedb.CSVFile("profile/synth/hard/trrack.csv")
    top = ToneSelector(label="soundfont:", db=tndb, selected = (0,0,53))
    top.show_all()

    top.connect("destroy", Gtk.main_quit)

    Gtk.main()
    
    print("is_updated=%s"%tndb.is_updated)
    print("selected = %u,%u,%u"%(top.sel[0],top.sel[1],top.sel[2]))
    for t in tndb.ls():
        print("%u,%u,%u,'%s','%s'"%(t[0],t[1],t[2],t[3],t[4]))

    pass
