import csv

import midisw.tonenamedb as tonenamedb

class CSVFile(tonenamedb.Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self, csvfname: str):
        self._clear_table()

        with open(csvfname,"r") as fd:
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

        return self

