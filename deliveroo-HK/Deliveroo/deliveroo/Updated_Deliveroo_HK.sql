-- Step - 1
-- Before fire thie insert ignore query we need to remove column id in both table
INSERT IGNORE INTO `data_menu_delivery_2025_02_05` (SELECT * FROM `data_menu_pickup_2025_02_05`)

-- Step - 2
UPDATE `data_menu_delivery_2025_02_05` AS p1, `data_menu_pickup_2025_02_05` AS p2 
SET p1.`original_price_pickup` = p2.`original_price_pickup` 
WHERE p1.`menu_id` = p2.`menu_id`;

-- Step - 3
UPDATE `data_menu_delivery_2025_02_05` AS p1, `data_menu_pickup_2025_02_05` AS p2 
SET p1.`discounted_price_pickup` = p2.`discounted_price_pickup` 
WHERE p1.`menu_id` = p2.`menu_id`;

-- Step - 4
UPDATE `data_menu_delivery_2025_02_05` AS p1, `data_menu_pickup_2025_02_05` AS p2 
SET p1.`discount_price_pickup` = p2.`discount_price_pickup` 
WHERE p1.`menu_id` = p2.`menu_id`;

-- Step - 5
UPDATE `data_menu_delivery_2025_02_05`  
SET menu_category= REPLACE(REPLACE(REPLACE(menu_category, CHAR(10), ''), CHAR(9), ''), CHAR(13), '');

-- Step - 6
UPDATE `data_menu_delivery_2025_02_05`  
SET menu_items= REPLACE(REPLACE(REPLACE(menu_items, CHAR(10), ''), CHAR(9), ''), CHAR(13), '');



-- Fire this below query if generating SQL any unnecessary error.
SET GLOBAL max_connections=99999
PURGE BINARY LOGS BEFORE NOW()
