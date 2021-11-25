
import subprocess
import os

import midisw.tonenamedb as tonenamedb
import midisw.util

class SoundFont(tonenamedb.Base):
    def __init__(self, *args):
        super().__init__()
        if len(args) > 0:
            self.load(args[0])

    def load(self, sfpath: str):
        self.truncate()

        sfpathex = os.path.expanduser(sfpath)
        if midisw.util.is_jack_active():
            engine = 'jack'
        else:
            engine = 'alsa'
        cmd = f" echo 'inst 1' | fluidsynth -a '{engine}'  \"{sfpathex}\" | grep '^[0-9]' | grep -v '^$' | cat - "
        rslt = subprocess.check_output(cmd,
                                       shell=True,
                                       universal_newlines=True,
                                       stderr=subprocess.DEVNULL)

        for line in rslt.split("\n"):
            if line == "":
                continue
            banks_progs = line[:7]
            banks,progs = banks_progs.split("-")
            banki = int(banks)
            progi = int(progs)
            gname = midisw.util.sfpath2sfname(sfpath)
            tname = line[8:]

            self.create(banki/128,banki%128,progi,gname, tname)

        self.con.commit()
        self.is_updated = False
        
        return self        
