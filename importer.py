import json
import settings
import geojson
import psycopg2
import logging


logging.debug('Starting to import...')
connection = psycopg2.connect(
    host=settings.PG_HOST,
    database="fields",
    user="postgres")
cur = connection.cursor()
logging.debug('Connection created')

with open(settings.PATH_TO_GJSON_FILE) as file:
    for line in file.readlines():
        line = geojson.loads(line.strip('\n'))
        props = line['properties']
        geom_type = line['geometry']['type']
        geom_obj = json.dumps(line['geometry'])
        if geom_type == 'MultiPolygon':
            cur.execute("""
                INSERT INTO fields_field (id, crop, productivity, area_ha, region, geom) 
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))""",
                (
                    props['id'], props['crop'], props['productivity'], 
                    props['area_ha'], props['region'], geom_obj,
                )
            )
        else:
            cur.execute("""
                INSERT INTO fields_field (id, crop, productivity, area_ha, region, geom_p) 
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))""",
                (
                    props['id'], props['crop'], props['productivity'], 
                    props['area_ha'], props['region'], geom_obj,
                )
            )
    logging.debug('Done.')

connection.commit()
logging.debug('Commited.')
cur.close()
connection.close()
logging.debug('Connection closed.')