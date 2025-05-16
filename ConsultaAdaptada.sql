

-- Contagem de visitas na geladeira por smn:

select Id_SenP, date(Dt_SenP) dia, count(Oc_Sens) from sensorpresenca
WHERE Dt_SenP BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() and Oc_Sens = 0
group by Id_SenP, dia
order by Id_SenP, dia;

-- Contagem de visitas na geladeira por mes:
select Id_SenP, date(Dt_SenP) dia, count(Oc_Sens) from sensorpresenca
WHERE Dt_SenP BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW() and Oc_Sens = 0
group by Id_SenP, dia
order by Id_SenP, dia;

-- Fluxo horario comercial da ultima semana
SELECT Id_SenF, SUM(Dt_SenF) / 7 AS entrantes FROM sensorpassagem
WHERE EXTRACT(HOUR FROM Dt_SenF) BETWEEN 9 AND 18 AND Dt_SenF BETWEEN DATE_SUB(NOW(), INTERVAL 8 DAY) AND DATE_SUB(NOW(), INTERVAL 1 DAY)
AND Id_SenF = 2
GROUP BY Id_SenF
ORDER BY Id_SenF;	

-- Fluxo de hj:

select Id_SenF, sum(En_SenF) entrantes from sensorpassagem
where date(Dt_SenF) = date(now()) and Id_SenF = 2
group by Id_SenF
order by Id_SenF;

-- Fluxo por hr de ontem:

select Id_SenF, hour(Dt_SenF) hora, sum(En_SenF) from sensorpassagem
WHERE Dt_SenF = DATE_SUB(NOW(), INTERVAL 1 DAY) and Id_SenF = 2
group by Id_SenF, hora
order by Id_SenF, hora;

SELECT Id_SenF, HOUR(Dt_SenF) AS hora, SUM(En_SenF)
FROM sensorpassagem
WHERE DATE(Dt_SenF) = CURDATE() - INTERVAL 1 DAY
  AND Id_SenF = 2
GROUP BY Id_SenF, hora
ORDER BY Id_SenF, hora;

-- Fluxo por hr de hj:
select Id_SenF, hour(Dt_SenF) hora, sum(En_SenF) from sensorpassagem
WHERE date(Dt_SenF) = date(NOW()) and Id_SenF = 2
group by Id_SenF, hora
order by Id_SenF, hora;

-- Fluxo por hr de hj:

select Id_SenF, hour(Dt_SenF) hora, sum(En_SenF) from sensorpassagem
WHERE Dt_SenF BETWEEN DATE_SUB(NOW(), INTERVAL 7 DAY) AND NOW() and Id_SenF = 2
group by Id_SenF, hora
order by Id_SenF, hora;



