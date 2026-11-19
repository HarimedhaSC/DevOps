CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer VARCHAR(100) NOT NULL,
    item VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL
);

INSERT INTO orders (order_id, customer, item, status)
VALUES
    (1, 'Rahul', 'Masala Dosa', 'Preparing'),
    (2, 'Priya', 'Paneer Dosa', 'Out for Delivery'),
    (3, 'Arjun', 'Idli Vada', 'Delivered');
