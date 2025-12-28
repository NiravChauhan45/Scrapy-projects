SELECT COUNT(*), STATUS FROM `geohash_data` GROUP BY STATUS;
SELECT COUNT(*), STATUS FROM `restaurant_links_2025_02_05` GROUP BY STATUS;	
SELECT COUNT(*), STATUS FROM `deliveroo_restaurant_2025_02_05` GROUP BY STATUS;

SELECT COUNT(*) FROM `data_menu_delivery_2025_02_05`;
SELECT COUNT(*) FROM `data_menu_pickup_2025_02_05`;
SELECT COUNT(*) FROM `data_be_20250205_001`;







SET GLOBAL max_connections=99999
PURGE BINARY LOGS BEFORE NOW()




