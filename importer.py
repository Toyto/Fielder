import settings
import geojson


with open(settings.PATH_TO_GJSON_FILE) as file:
    for line in file.readlines():
        line = geojson.loads(line.strip('\n'))
        # TODO: insert data to DB here