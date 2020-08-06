The examples are in the Endpoint specification.pdf file.

To start the app:
`docker-compose up`

To fill up the DB:
  `docker-compose exec db bash -c psql -U postgres`

  In psql shell copypaste the commands from init.sql file.

  Copy geojson file into docker container(assuming that file is in /tmp dir):
  docker cp /tmp/fr-subset.geojsons  [container name(could be fetched from `docker ps`)]:/mnt


  `docker-compose exec app bash`
  
  `python importer.py`
  
  Take a cup of coffee, the command will take around 15min.
