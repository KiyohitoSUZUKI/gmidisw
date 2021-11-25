#!/usr/bin/bash


cat pr-i.txt | sed '1,13d' | sed 's/^ *//g' |\
    awk '/^[0-9][0-9][0-9] .*$/{
         pg=$1
         val=substr($0,4)
         printf("%s\n%s\n",pg,val) 
      } !/^[0-9][0-9][0-9] .*$/ {print $0}' |\
    awk '
     (NR-1)%4 == 0 {pg=$0 - 1 }
     (NR-1)%4 == 1 {tname=$0}
     (NR-1)%4 == 2 {numtone=$0}
     (NR-1)%4 == 3 {gname=$0; 
                    printf("87,%d,%03d,\"%s\",\"%s\"\n",pg/128,pg%128,gname,tname)
     }' | sort
