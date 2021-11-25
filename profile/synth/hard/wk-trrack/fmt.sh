#!/usr/bin/bash

cat TR-Rack-20211122-names.txt | grep Combination |\
    awk -F '\t' '
    BEGIN {
      bank2lsb["A"] = 0
      bank2lsb["B"] = 1
      bank2lsb["C"] = 2
      bank2lsb["D"] = 3
    }
    {
       tname=$1
       id=$4
       bank=substr(id,1,1)
       prog=substr(id,2)
       gname=$6
       printf("0,%d,%d,\"%s\",\"%s\"\n", bank2lsb[bank], prog, gname, tname);
    }'
