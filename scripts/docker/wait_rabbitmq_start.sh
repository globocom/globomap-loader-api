#!/bin/bash
# Check rabbitmq service
INTERVAL=5
MAX_ATTEMPTS=30
CHECK_COMMAND="curl -sL -w "%{http_code}" http://globomap_loader_queue:15672 -o /dev/null"
ATTEMPTS=1
HTTP_RET_CODE=`${CHECK_COMMAND}`
while [ "000" = "${HTTP_RET_CODE}" ] && [ ${ATTEMPTS} -le ${MAX_ATTEMPTS} ]; do
    echo "Error connecting to rabbitmq. Attempt ${ATTEMPTS}. Retrying in ${INTERVAL} seconds ..."
    sleep ${INTERVAL}
    ATTEMPTS=$((ATTEMPTS+1))
    HTTP_RET_CODE=`${CHECK_COMMAND}`
done

if [ "000" = "${HTTP_RET_CODE}" ]; then
        echo "Error connecting to rabbitmq. Aborting ..."
        exit 2
fi

make run
