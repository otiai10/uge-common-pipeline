#!/bin/sh

#$ -S /bin/sh

echo "This is hello_01!! `date`"
echo "Has env var 'COOKER_SPAWN_INDEX': ${COOKER_SPAWN_INDEX}"
i=0
while [ ${i} -lt 5 ]
do
	sleep 1
	printf "."
	i=$(( i + 1 ))
done
echo ""
echo "END: hello_01 `date`"
