import os
import csv

import midisw.tonenamedb as tonenamedb

class CSVFile(tonenamedb.Base):
    def __init__(self, *args):
        super().__init__()
        if len(args) > 0 :
            self.load(args[0])

    def load(self, csvfname: str):
        self.truncate()

        with open(os.path.expanduser(csvfname),"r") as fd:
            tdef = csv.DictReader(fd, delimiter=",",
                                  doublequote=True,
                                  quotechar='"',
                                  lineterminator="\n",
                                  skipinitialspace=True)
    
            for tone in tdef:
                self.create(int(tone["bankmsb"]),
                            int(tone["banklsb"]),
                            int(tone["prog"]),
                            tone["gname"],
                            tone["tname"]
                )

            self.con.commit()

        self.is_updated = False
        return self

