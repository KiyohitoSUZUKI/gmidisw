#!/usr/bin/bash

  cat gm.txt | sed '1,17d' | sed 's/^ *//g' |\
    awk '/^[0-9][0-9][0-9] .*$/{
         pg=$1
         val=substr($0,4)
         printf("%s\n%s\n",pg,val) 
      } !/^[0-9][0-9][0-9] .*$/ {print $0}' |\
    awk '
     (NR-1)%5 == 0 {num=$0}
     (NR-1)%5 == 1 {tname=$0}
     (NR-1)%5 == 2 {numvoice=$0}
     (NR-1)%5 == 3 {lsb=$0}
     (NR-1)%5 == 4 {pg=$0 - 1; 
              printf("121,%d,%03d,\"GM2\",\"%s\"\n",lsb, pg, tname)
     }'   > gm.txt.csv

