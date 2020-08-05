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
            ) IS True LIMIT %s;
        """ % (coords, distance, settings.MAX_RES_SIZE)
        return self._run_sql(sql)

    def rectangle(self, coords):
        sql = """
            SELECT id, crop, productivity, area_ha, region, ST_AsGeoJSON(geom) FROM fields_field WHERE 
            ST_Intersects(
                geom::geography, 
                ST_MakeEnvelope(%s, 4326)::geography
            ) IS True LIMIT %s;
        """ % (coords, settings.MAX_RES_SIZE)
        return self._run_sql(sql)


class StatExtractor():

    def _run_sql(self, sql):
        with psycopg2.connect(host=settings.PG_HOST, database="fields", user="postgres") as conn:
            with conn.cursor() as curs:
                curs.execute(sql)
                return self._fetch_to_json(curs.fetchall())

    def _fetch_to_json(self, sql_result):
        data = {'crops': []}
        for row in sql_result:
            crop_stat = {
                'crop': row[0],
                'average_yield': row[1],
                'total_yield': row[2],
                'total_area': row[3],
            }
            data['crops'].append(crop_stat)

        return data

    def get_region(self, region):
        sql = """
            SELECT crop, AVG(productivity::numeric), SUM(productivity::numeric), SUM(area_ha), region FROM fields_field WHERE 
            region = '%s' GROUP BY region, crop;
        """ % (region)
        return self._run_sql(sql)
