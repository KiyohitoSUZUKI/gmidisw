
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
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute(self.TBLDEF)
        self.con.commit()
        self.is_updated = False

    ##------------------------------------------
    def create(self, bankmsb: int, banklsb: int, prog: int, gname: str, tname: str):
        self.cur.execute("INSERT INTO tone VALUES (?,?,?,?,?);",
                    (bankmsb,banklsb,prog,gname,tname) )
        self.con.commit()
        self.is_updated = True
        return self


    def truncate(self):
        self.cur.execute("DELETE FROM tone;")
        self.con.commit()
        self.is_updated = True
        return self
        
    ##------------------------------------------
    def get_tname(self, bankmsb: int, banklsb: int, prog: int):
        self.cur.execute("SELECT tname FROM tone WHERE bankmsb = ? AND banklsb = ? AND prog = ? ;",(bankmsb, banklsb, prog))
        row = self.cur.fetchone()

        return str(row[0])

    def set_name(self, bankmsb: int, banklsb: int, prog: int, column: str, newname: str):
        self.cur.execute(f"UPDATE tone SET {column} = ? WHERE bankmsb = ? AND banklsb = ? AND prog = ?",(newname, bankmsb, banklsb, prog))
        self.con.commit()
        self.is_updated = True
        return self

    def ls(self, bankmsb = None, banklsb = None, prog = None,gname = None):
        w = {}
        if not bankmsb is None:
            w["bankmsb"] = "bankmsb = %u"%int(bankmsb)
        if not banklsb is None:
            w["banklsb"] = "banklsb = %u"%int(banklsb)
        if not prog is None:
            w["prog"] = "prog = '%u'"%int(prog)
        if not gname is None:
            w["gname"] = "gname = '%s'"%str(gname)

        sql = "SELECT * FROM tone "
        wcnt = 0
        for i in ["bankmsb", "banklsb", "prog", "gname"]:
            if i in w:
                if wcnt == 0:
                    sql += f"where {w[i]} "
                else:
                    sql += f"and  {w[i]} "
                wcnt += 1
        sql += "ORDER BY bankmsb asc ,banklsb asc ,prog asc;"

        self.cur.execute(sql)

        return self.cur.fetchall()
                
    def get_collection(self, column: str):
        self.cur.execute(f"SELECT {column} FROM tone GROUP BY {column};")
        return self.cur.fetchall()

###########################################################################

        
