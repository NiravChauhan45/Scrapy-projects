CREATE TABLE orders(
   order_id INT,
   order_date DATETIME,
   order_customer_id INT,
   order_status VARCHAR(45)
);

-- worked
INSERT INTO orders VALUES(1,'2013-07-25 00:00:00','11599','CLOSED');

-- failed
INSERT INTO orders VALUES(2,'2013-07-25 00:00:00','1159-A12','CLOSED');

-- worked
INSERT INTO orders VALUES(3,'2013-07-25','11599','CLOSED');

SELECT * FROM orders ORDER BY order_id;
