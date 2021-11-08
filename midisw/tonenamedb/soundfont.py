
import subprocess

import midisw.tonenamedb as tonenamedb

class SoundFont(tonenamedb.Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self, sfpath: str):
        self._clear_table()

        cmd = f" echo 'inst 1' | fluidsynth -a 'alsa'  \"{sfpath}\" | grep '^[0-9]' | grep -v '^$' "
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
            gname = ""
            tname = line[8:]

            self.create(banki/128,banki%128,progi,"", tname)

        self.con.commit()

        
