-- **************************************************************************
-- PROJECT: TELECOM CHURN ANALYSIS - COMPLETE 10-QUESTION SUITE (FINAL)
-- AUTHOR: Çimen Artuger
-- DATE: 2026-04-27
-- **************************************************************************

use churn_analýzý;
go

-- Analiz 1: Müþteri Hizmetleri Aramalarýna Göre Churn Oranlarý
select t.Customer_service_calls, 
       count(*) as total_customers,
       AVG(case when T.Churn = 'true' then 1.0 else 0.0 end) as churn_rate
from [telecom churn dataset] as t
group by t.Customer_service_calls
order by t.Customer_service_calls ASC;

-- Analiz 2: Eyaletlere (State) Göre Müþteri Daðýlýmý ve Churn Alarmý
select t.state, 
       Count (*) as total_customers, 
       sum(case when t.churn = 'true' then 1 else 0 end) as churn_customers,
       AVg(case when t.churn = 'true' then 1.0 else 0.0 end) as churn_rate
from [telecom churn dataset] as t
group by t.State
order by churn_rate desc;

-- Analiz 3: Uluslararasý Planýn (International Plan) Churn Üzerindeki Etkisi
select T.International_plan, COUNT(*) as total_customers,
       AVG(CASE WHEN t.Churn = 'True' THEN 1.0 ELSE 0.0 END) AS Churn_Rate
from [telecom churn dataset] as t
group by t.International_plan
order by Churn_Rate desc;

-- Analiz 4: Hayal Kýrýklýðýna Uðramýþ Müþteriler (Planý Var Ama Dakikasý Yok)
SELECT COUNT(*) AS frustrated_customers
FROM [telecom churn dataset]
WHERE International_plan = 'yes' 
AND Total_intl_minutes = 0;

-- Analiz 5: Sesli Mesaj Planýnýn (Voice Mail Plan) Churn Oranýna Etkisi
select T.Voice_mail_plan, COUNT(*) as Voice_mail_plan_number,
       AVg(case when T.Churn = 'true' then 1.0 else 0.0 end) as churn_rate
from [telecom churn dataset] as t
group by t.Voice_mail_plan
order by churn_rate desc;

-- Analiz 6: Churn Durumuna Göre Gündüz ve Gece Dakika Ortalamalarý
SELECT t.Churn, 
       AVG(t.Total_day_minutes) AS avg_day_mins,
       AVG(t.Total_night_minutes) AS avg_night_mins
FROM [telecom churn dataset] AS t
GROUP BY t.Churn;

-- Analiz 7: Günlük Toplam Ücretlerin Churn Durumuna Göre Karþýlaþtýrýlmasý
select t.churn, avg(t.Total_day_charge) as total_day_charge_remote
from [telecom churn dataset] as t
group by t.Churn
order by total_day_charge_remote desc;

-- Analiz 8: Churn Oraný En Yüksek Ýlk 5 Eyalet
select top 5 t.[state],
       avg(case when t.Churn = 'true' then 1.0 else 0.0 end) as churn_rate
from [telecom churn dataset] as t
group by t.[State]
order by churn_rate desc;

-- Analiz 9: Eski müþteriler mi yoksa yeni müþteriler mi daha çok kaçýyor?
SELECT 
    CASE WHEN t.Account_length > 100 THEN 'Old Customer (100+)' 
         ELSE 'New Customer (0-100)' END AS Customer_Segment,
    COUNT(*) AS total_customers,
    AVG(CASE WHEN t.Churn = 'True' THEN 1.0 ELSE 0.0 END) AS churn_rate
FROM [telecom churn dataset] AS t
GROUP BY CASE WHEN t.Account_length > 100 THEN 'Old Customer (100+)' 
              ELSE 'New Customer (0-100)' END;

-- Analiz 10: Uluslararasý planý olan ve 3'ten fazla arayanlarýn durumu nedir?
select count(t.International_plan) as number_International_plan, 
       sum(T.Customer_service_calls) as total_Customer_service_calls,
       AVG(CASE WHEN t.Churn = 'True' THEN 1.0 ELSE 0.0 END) AS churn_rate
FROM [telecom churn dataset] AS t
where t.International_plan = 'yes' and t.Customer_service_calls > 3
group by t.International_plan;