CREATE DATABASE IF NOT EXISTS mercadinho DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- Todos os deltas estão em segundos

USE mercadinho;

-- topic v3/espm/devices/presence01/up
-- topic v3/espm/devices/presence02/up
-- topic v3/espm/devices/presence03/up
-- topic v3/espm/devices/presence04/up
-- topic v3/espm/devices/presence05/up
-- topic v3/espm/devices/presence06/up
-- topic v3/espm/devices/presence07/up
-- topic v3/espm/devices/presence08/up
-- { "end_device_ids": { "device_id": "presence01" }, "uplink_message": { "rx_metadata": [{ "timestamp": 2040934975 }], "decoded_payload": { "battery": 99, "occupancy": "vacant" } } }
CREATE TABLE presenca (
  id bigint NOT NULL AUTO_INCREMENT,
  data datetime NOT NULL,
  id_sensor tinyint NOT NULL,
  delta int NOT NULL,
  bateria tinyint NOT NULL,
  ocupado tinyint NOT NULL,
  PRIMARY KEY (id),
  KEY presenca_data_id_sensor (data, id_sensor),
  KEY presenca_id_sensor (id_sensor)
);

-- topic v3/espm/devices/passage01/up
-- topic v3/espm/devices/passage02/up
-- { "end_device_ids": { "device_id": "passage01" }, "uplink_message": { "rx_metadata": [{ "timestamp": 2040934975 }], "decoded_payload": { "battery": 0, "period_in": 0, "period_out": 0 } } }
CREATE TABLE passagem (
  id bigint NOT NULL AUTO_INCREMENT,
  data datetime NOT NULL,
  id_sensor tinyint NOT NULL,
  delta int NOT NULL,
  bateria tinyint NOT NULL,
  entrada int NOT NULL,
  saida int NOT NULL,
  PRIMARY KEY (id),
  KEY passagem_data_id_sensor (data, id_sensor),
  KEY passagem_id_sensor (id_sensor)
);

-- Query para monitorar em tempo real
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 1 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 2 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 3 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 4 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 5 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 6 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 7 order by id desc limit 1)
union all
(select id_sensor, ocupado, time_to_sec(timediff(now(), data)) delta_agora from presenca where id_sensor = 8 order by id desc limit 1)
;

-- Query com a média de presença por dia
select id_sensor, date(data) dia, avg(delta) presenca_media from presenca
where data between '2025-03-10 00:00:00' and '2025-03-14 23:59:59' and ocupado = 0
group by id_sensor, dia
order by id_sensor, dia
;

------- Nossas
-- Contagem de visitas na geladeira por smn:

select id_sensor, date(data) dia, count(ocupado) from presenca
WHERE data BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() and ocupado = 0
group by id_sensor, dia
order by id_sensor, dia
;

-- Contagem de visitas na geladeira por mes:

select id_sensor, date(data) dia, count(ocupado) from presenca
WHERE data BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW() and ocupado = 0
group by id_sensor, dia
order by id_sensor, dia
;

-- Fluxo do horário comercial da última semana:

SELECT id_sensor, SUM(entrada) / 7 AS entrantes FROM passagem
WHERE EXTRACT(HOUR FROM data) BETWEEN 9 AND 18 AND data BETWEEN DATE_SUB(NOW(), INTERVAL 8 DAY) AND DATE_SUB(NOW(), INTERVAL 1 DAY)
AND id_sensor = 2
GROUP BY id_sensor
ORDER BY id_sensor;


-- Fluxo de hj:

select id_sensor, sum(entrada) entrantes from contagem
where date(data) = date(now()) and id_sensor = ?
group by id_sensor
order by id_sensor
;

-- Fluxo por hr de ontem:

select id_sensor, hour(data) hora, sum(entrada) from contagem
WHERE data = DATE_SUB(NOW(), INTERVAL 1 DAY) and id_sensor = ?
group by id_sensor, hora
order by id_sensor, hora
;

-- Fluxo por hr de hj:

select id_sensor, hour(data) hora, sum(entrada) from contagem
WHERE date(data) = date(NOW()) and id_sensor = ?
group by id_sensor, hora
order by id_sensor, hora
;

-- Fluxo por hr de hj:

select id_sensor, hour(data) hora, sum(entrada) from passagem
WHERE data BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() and id_sensor = ?
group by id_sensor, hora
order by id_sensor, hora
;
