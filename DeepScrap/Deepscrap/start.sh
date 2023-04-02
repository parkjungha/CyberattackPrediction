#!/bin/bash
filename="./search_list.txt"
number=20
while read line; do
    if [ "$line" == "" ]; then
        echo "finish"
    else
        del=$IFS
        IFS=',' read -a n <<< $line
        array=(${n[@]})
        size=$((${#array[@]}/$number))

        for index in $(seq 0 $size)
        do
            spl=$(($index*$number))
            ar=${array[@]:$spl:$number}
            ar=${ar// /,}
            echo $ar
            eval "scrapy crawl_many -a $ar -o output.json -t json"
        done
   fi
done < $filename



