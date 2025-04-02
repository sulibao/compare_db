#!/bin/bash

MYSQL_HOST="xx.xx.xx.xx"
MYSQL_PORT="20307"
MYSQL_USER="root"
MYSQL_PASS="xxx"
DIR="source"

MYSQL_DBS="test-su"
IFS=',' read -ra DBS <<< "$MYSQL_DBS"

if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
    echo "目录 $DIR 创建成功"
else
    echo "目录 $DIR 已存在"
fi

for MYSQL_DB in "${DBS[@]}"; do
    OUTPUT_TABLE="${DIR}/${MYSQL_DB}.table"
    mysql -h${MYSQL_HOST} -P${MYSQL_PORT} -u${MYSQL_USER} -p${MYSQL_PASS} -D${MYSQL_DB} -e \
    "SELECT table_name FROM information_schema.tables WHERE table_schema='${MYSQL_DB}' ORDER BY table_name;" \
    | awk 'NR>1' > ${OUTPUT_TABLE}
    OUTPUT_FILE="${DIR}/${MYSQL_DB}.txt"
    >${OUTPUT_FILE}
    TABLES=(`cat $OUTPUT_TABLE`)
    for TABLE_NAME in "${TABLES[@]}"; do
        mysql -h${MYSQL_HOST} -P${MYSQL_PORT} -u${MYSQL_USER} -p${MYSQL_PASS} -D${MYSQL_DB} -e \
	"select '${TABLE_NAME}',count(1) from \`${TABLE_NAME}\`;" \
	| awk 'NR>1' >> ${OUTPUT_FILE}
    done
    echo "Query results for database ${MYSQL_DB} have been saved to: ${OUTPUT_FILE}"
done
