import settings
import psycopg2
import json


class ValuesExtractor():

    def _run_sql(self, sql):
        with psycopg2.connect(host=settings.PG_HOST, database="fields", user="postgres") as conn:
            with conn.cursor() as curs:
                curs.execute(sql)
                return self._fetch_to_json(curs.fetchall())

    def _fetch_to_json(self, sql_result):
        data = {'type': 'FeatureCollection', 'features': []}
        for row in sql_result:
            props = {
                'crop': row[1],
                'productivity': row[2],
                'area_ha': row[3],
                'region': row[4],
            }
            feature = {
                'type': 'Feature',
                'id': row[0],
                'geometry': json.loads(row[5]),
                'properties': props,
            }
            data['features'].append(feature)

        return data

    def equidistant_point(self, coords, distance):
        sql = """
            SELECT id, crop, productivity, area_ha, region, ST_AsGeoJSON(geom) FROM fields_field WHERE 
            ST_Intersects(
                geom::geography, 
                ST_Buffer(ST_MakePoint(%s)::geography, 
                %s, 'quad_segs=8')
            ) IS True;
        """ % (coords, distance)
        return self._run_sql(sql)
