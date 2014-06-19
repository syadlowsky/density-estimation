BEGIN;
CREATE TEMP TABLE tmp (
  id bigint,
  network_id bigint,
  beg_node_id bigint,
  end_node_id bigint
);

SELECT AddGeometryColumn('tmp','geom', 4326, 'LINESTRING', 2);

ALTER TABLE tmp
ADD COLUMN length double precision,
ADD COLUMN link_name text,
ADD COLUMN lane_count integer,
ADD COLUMN link_type text,
ADD COLUMN speed_limit float;

\copy tmp FROM 'data/Links_I15.csv' DELIMITER ',' CSV HEADER;
-- UPDATE microsim_link SET geom_dist = ST_Transform(geom, 900913);
COMMIT;
