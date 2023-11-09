CREATE DATABASE sales;
USE sales;

CREATE TABLE sales_data(
    product_id INT,
    customer_id INT,
    price INT,
    quantity INT,
    timestamp DATETIME
);

SHOW TABLES;
SELECT COUNT(*) FROM sales_data;
CREATE INDEX ts on sales_data(timestamp);
SHOW INDEX FROM sales.sales_data;