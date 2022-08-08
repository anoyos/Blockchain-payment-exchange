#!/bin/sh

DB_CONTAINER_NAME="wallet-service_mongo_db_1"
DB_NAME="wallets"
DUMP_FOLDER="./app/app/tests/.db_data"
rm -r "$DUMP_FOLDER/$DB_NAME"
CONTAINER_ID=$(docker ps -aqf "name=$DB_CONTAINER_NAME")
docker exec "$CONTAINER_ID" mongodump -d $DB_NAME -o /dump
docker cp "$CONTAINER_ID":/dump/$DB_NAME $DUMP_FOLDER