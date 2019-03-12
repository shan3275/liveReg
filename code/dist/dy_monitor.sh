#!/bin/sh 
while [ true ] 
do
    procID=`pgrep main`
    if [ "" == "$procID" ];
    then
        echo '重启程序'
        date
        lpwd=`pwd`
        echo 'cd ' $lpwd > terminal.sh
        echo './main' >> terminal.sh
        echo 'sleep 10' >> terminal.sh
        chmod +x terminal.sh
        open -a Terminal.app terminal.sh
        sleep 5
        rm terminal.sh
    fi
    echo '延迟600秒'
    sleep 600
done
