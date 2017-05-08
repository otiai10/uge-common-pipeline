#!/bin/sh

#$ -S /bin/sh

echo "This is hello04."
echo "FOOBAR=${FOOBAR}, HOGE=${HOGE}"
date
sleep 1
date
echo "END: hello_04"
