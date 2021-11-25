import os
import subprocess
import xml.etree.ElementTree as ET

import logging

import midisw.tonenamedb as tonenamedb

class Zynaddsubfx(tonenamedb.Base):
    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.truncate()

        confxml = os.path.expanduser("~/.zynaddsubfx-bank-cache.xml")
        bankbase = "/usr/share/zynaddsubfx/banks/"
                
        cmd = f"cat {confxml} | grep -v '^$'"
        xmlstr = subprocess.check_output(cmd,shell=True, universal_newlines=True)
        root = ET.fromstring(xmlstr)

        ##========================
        banki=-1
        last_bank=""        
        for t in root[2]:
            progi = int(t.attrib["id"])

            gname = t.attrib["bank"].replace(bankbase,"").replace("/","")
            tname = t.attrib["name"]
        
            if gname != last_bank:
                banki += 1
                last_bank = gname
        
            self.create(banki / 128, banki % 128, progi,  gname, tname)

        self.con.commit()
        self.is_updated = False

        return self
