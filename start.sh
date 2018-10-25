docker-compose up -d

echo 'PostgreSQL terminal session starting'
echo 'Default password is `uclh`'
echo 'type \q if you want to quit'

docker exec -it omop-uclh_db_1 /usr/local/bin/psql -h postgres -U uclh OMOP-UCLH