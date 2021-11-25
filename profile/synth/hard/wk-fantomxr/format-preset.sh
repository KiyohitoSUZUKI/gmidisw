#!/usr/bin/bash

declare -A ofsdic=(
   ["pr-ab.txt"]=64
   ["pr-cd.txt"]=66
   ["pr-ef.txt"]=68
   ["pr-gh.txt"]=70
)

for f in pr-ab.txt pr-cd.txt pr-ef.txt pr-gh.txt; do 
  cat $f | sed '1,14d' | sed 's/^ *//g' |\
    awk '/^[0-9][0-9][0-9] .*$/{
         pg=$1
         val=substr($0,4)
         printf("%s\n%s\n",pg,val) 
      } !/^[0-9][0-9][0-9] .*$/ {print $0}' |\
    awk -v ofs="${ofsdic[$f]}" '
     BEGIN{ ofsl = ofs; ofsh = ofs+1}
     (NR-1)%4 == 0 {pg=$0 - 1 }
     (NR-1)%4 == 1 {tname=$0}
     (NR-1)%4 == 2 {numtone=$0}
     (NR-1)%4 == 3 {gname=$0; 
     	      if (NR < 928) {
                  if (((NR-1)%16 == 3) || ((NR-1)%16 == 7)) {
                    ofsi = ofsl;
                  } else {
                    ofsi = ofsh;
                  }
   	      }	else {
                  if ((NR-1)%8 == 3) {
                    ofsi = ofsl;
                  } else {
                    ofsi = ofsh;
                  }
              }
              printf("87,%d,%03d,\"%s\",\"%s\"\n",ofsi+pg/128,pg%128,gname,tname)
     }'   > ${f}.csv
done
