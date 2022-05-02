#!/bin/bash 

cd /myproject/yoyo-algorithm-deploy

cd fast-text-rank
chmod u+x build.sh
./build.sh
cd ..

cd google-translate-crack
chmod u+x build.sh
./build.sh
cd ..

cd gtts
chmod u+x build.sh
./build.sh
cd ..

cd paddle
chmod u+x build.sh
./build.sh
cd ..

cd domain-parse-location
chmod u+x build.sh
./build.sh
cd ..