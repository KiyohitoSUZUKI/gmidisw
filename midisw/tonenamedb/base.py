
import sqlite3

###########################################################################
class Base(object):
    TBLDEF="""
CREATE TABLE tone (
    bankmsb INTEGER, 
    banklsb INTEGER, 
    prog    INTEGER, 
    gname   TEXT NOT NULL, 
    tname   TEXT NOT NULL, 
    PRIMARY KEY (bankmsb, banklsb, prog)
);
"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute(self.TBLDEF)
        self.con.commit()

    ##------------------------------------------
    def create(self, bankmsb: int, banklsb: int, prog: int, gname: str, tname: str):
        self.cur.execute("INSERT INTO tone VALUES (?,?,?,?,?);",
                    (bankmsb,banklsb,prog,gname,tname) )
        return self


    def _clear_table(self):
        self.cur.execute("DELETE FROM tone;")
        self.con.commit()
        
    ##------------------------------------------
    def ls(self):
        self.cur.execute("select * FROM tone;")
        row = self.cur.fetchall()
        return row

    def get_tonename(self, bankmsb: int, banklsb: int, prog: int):
        self.cur.execute("SELECT tname FROM tone WHERE bankmsb = ? AND banklsb = ? AND prog = ? ;",(bankmsb, banklsb, prog))
        row = self.cur.fetchone()
        return str(row[0])


###########################################################################

        
