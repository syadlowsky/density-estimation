DROP TABLE cell_data_tower_voronoi;
CREATE TABLE cell_data_tower_voronoi AS SELECT * FROM voronoi('cell_data_tower', 'location') AS (id integer, geom geometry);
UPDATE cell_data_tower w SET geom = sq.geom FROM (SELECT v.geom AS geom, w.id AS w_id FROM cell_data_tower w, cell_data_tower_voronoi v WHERE ST_Contains(v.geom, w.location)) AS sq WHERE w_id = w.id;
