CREATE DATABASE fields;
CREATE EXTENSION postgis;

CREATE TABLE fields_field ("id" serial NOT NULL PRIMARY KEY,"crop" varchar(255),"productivity" varchar(255),"area_ha" numeric(20, 16),"history" varchar(255),"region" varchar(255),"score" integer);

SELECT AddGeometryColumn ('fields_field', 'geom', 4326, 'MultiPolygon', 2);
SELECT AddGeometryColumn ('fields_field', 'geom_p', 4326, 'Polygon', 2);