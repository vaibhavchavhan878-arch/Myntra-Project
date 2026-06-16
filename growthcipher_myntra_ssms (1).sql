-- ============================================
--   GrowthCipher — Sales & Revenue Analytics
--   Company Theme : Myntra (Fashion & Lifestyle)
--   Tool          : SQL Server Management Studio (SSMS)
--   Version       : SQL Server 2022
-- ============================================

-- Step 1: Database banao
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'growthcipher_myntra')
    CREATE DATABASE growthcipher_myntra;
GO

USE growthcipher_myntra;
GO

-- ============================================
-- TABLE 1: regions
-- ============================================
IF OBJECT_ID('regions', 'U') IS NOT NULL DROP TABLE regions;
GO

CREATE TABLE regions (
    region_id   INT IDENTITY(1,1) PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL,
    city        VARCHAR(50) NOT NULL
);
GO

INSERT INTO regions (region_name, city) VALUES
('North',   'Delhi'),
('South',   'Bangalore'),
('West',    'Mumbai'),
('East',    'Kolkata'),
('Central', 'Pune'),
('South',   'Chennai'),
('West',    'Ahmedabad'),
('North',   'Jaipur');
GO

-- ============================================
-- TABLE 2: customers
-- ============================================
IF OBJECT_ID('customers', 'U') IS NOT NULL DROP TABLE customers;
GO

CREATE TABLE customers (
    customer_id   INT IDENTITY(1,1) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email         VARCHAR(100),
    gender        VARCHAR(10),
    age           INT,
    region_id     INT,
    joined_date   DATE,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);
GO

INSERT INTO customers (customer_name, email, gender, age, region_id, joined_date) VALUES
('Aarav Sharma',    'aarav.sharma@gmail.com',    'Male',   28, 1, '2022-03-10'),
('Priya Mehta',     'priya.mehta@gmail.com',     'Female', 24, 2, '2022-05-18'),
('Rohan Verma',     'rohan.verma@yahoo.com',     'Male',   31, 3, '2022-06-22'),
('Sneha Patil',     'sneha.patil@gmail.com',     'Female', 26, 5, '2022-07-04'),
('Karan Das',       'karan.das@outlook.com',     'Male',   22, 4, '2022-08-15'),
('Anjali Singh',    'anjali.singh@gmail.com',    'Female', 29, 1, '2022-09-01'),
('Vikram Nair',     'vikram.nair@gmail.com',     'Male',   34, 2, '2022-10-11'),
('Pooja Joshi',     'pooja.joshi@yahoo.com',     'Female', 27, 3, '2022-11-20'),
('Suresh Kumar',    'suresh.kumar@gmail.com',    'Male',   30, 4, '2023-01-05'),
('Meena Iyer',      'meena.iyer@gmail.com',      'Female', 23, 6, '2023-02-14'),
('Arjun Kapoor',    'arjun.kapoor@gmail.com',    'Male',   25, 7, '2023-03-09'),
('Divya Reddy',     'divya.reddy@outlook.com',   'Female', 28, 6, '2023-04-17'),
('Nikhil Gupta',    'nikhil.gupta@gmail.com',    'Male',   33, 8, '2023-05-23'),
('Riya Chatterjee', 'riya.chatt@gmail.com',      'Female', 21, 4, '2023-06-30'),
('Manish Tiwari',   'manish.tiwari@yahoo.com',   'Male',   27, 5, '2023-07-12');
GO

-- ============================================
-- TABLE 3: brands
-- ============================================
IF OBJECT_ID('brands', 'U') IS NOT NULL DROP TABLE brands;
GO

CREATE TABLE brands (
    brand_id   INT IDENTITY(1,1) PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    country    VARCHAR(50)
);
GO

INSERT INTO brands (brand_name, country) VALUES
('H&M',         'Sweden'),
('Roadster',    'India'),
('Puma',        'Germany'),
('W for Woman', 'India'),
('Levi''s',     'USA'),
('Mango',       'Spain'),
('HRX',         'India'),
('Global Desi', 'India'),
('Nike',        'USA'),
('Biba',        'India');
GO

-- ============================================
-- TABLE 4: products
-- ============================================
IF OBJECT_ID('products', 'U') IS NOT NULL DROP TABLE products;
GO

CREATE TABLE products (
    product_id   INT IDENTITY(1,1) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category     VARCHAR(50),
    sub_category VARCHAR(50),
    brand_id     INT,
    unit_price   DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
);
GO

INSERT INTO products (product_name, category, sub_category, brand_id, unit_price) VALUES
('H&M Slim Fit Chinos',            'Men',   'Bottomwear',  1,  1499.00),
('Roadster Graphic Tee',           'Men',   'Topwear',     2,   799.00),
('Puma Running Shorts',            'Men',   'Activewear',  3,  1299.00),
('W Floral Kurta',                 'Women', 'Ethnicwear',  4,  1899.00),
('Levi''s 511 Slim Jeans',         'Men',   'Bottomwear',  5,  3499.00),
('Mango Wrap Dress',               'Women', 'Westernwear', 6,  2999.00),
('HRX Sports Jacket',              'Men',   'Activewear',  7,  2499.00),
('Global Desi Palazzo Set',        'Women', 'Ethnicwear',  8,  1699.00),
('Nike Air Zoom Running Shoes',    'Men',   'Footwear',    9,  6999.00),
('Biba Anarkali Suit',             'Women', 'Ethnicwear', 10,  2799.00),
('Puma Classic Sneakers',          'Women', 'Footwear',    3,  4499.00),
('H&M Oversized Hoodie',           'Women', 'Topwear',     1,  1799.00),
('Roadster Cargo Pants',           'Men',   'Bottomwear',  2,  1599.00),
('Mango Linen Blazer',             'Women', 'Westernwear', 6,  4999.00),
('Nike Dri-FIT T-Shirt',           'Men',   'Activewear',  9,  1999.00),
('W Embroidered Dupatta Set',      'Women', 'Ethnicwear',  4,  2299.00),
('Levi''s Denim Jacket',           'Men',   'Outerwear',   5,  4999.00),
('HRX Yoga Pants',                 'Women', 'Activewear',  7,  1299.00),
('Biba Cotton Kurti',              'Women', 'Ethnicwear', 10,   999.00),
('H&M Formal Shirt',               'Men',   'Topwear',     1,  1299.00);
GO

-- ============================================
-- TABLE 5: orders
-- ============================================
IF OBJECT_ID('order_items', 'U') IS NOT NULL DROP TABLE order_items;
IF OBJECT_ID('orders', 'U') IS NOT NULL DROP TABLE orders;
GO

CREATE TABLE orders (
    order_id      INT IDENTITY(1,1) PRIMARY KEY,
    customer_id   INT,
    order_date    DATE,
    delivery_date DATE,
    status        VARCHAR(20) DEFAULT 'Delivered',
    payment_mode  VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
GO

INSERT INTO orders (customer_id, order_date, delivery_date, status, payment_mode) VALUES
(1,  '2023-01-05', '2023-01-08', 'Delivered', 'UPI'),
(2,  '2023-01-18', '2023-01-22', 'Delivered', 'Credit Card'),
(3,  '2023-02-02', '2023-02-06', 'Delivered', 'COD'),
(4,  '2023-02-20', '2023-02-24', 'Delivered', 'Debit Card'),
(5,  '2023-03-07', '2023-03-11', 'Delivered', 'UPI'),
(6,  '2023-03-25', '2023-03-29', 'Delivered', 'Credit Card'),
(7,  '2023-04-10', '2023-04-14', 'Delivered', 'UPI'),
(8,  '2023-04-28', '2023-05-02', 'Delivered', 'COD'),
(9,  '2023-05-15', '2023-05-19', 'Delivered', 'Credit Card'),
(10, '2023-05-30', '2023-06-03', 'Delivered', 'UPI'),
(11, '2023-06-12', '2023-06-16', 'Delivered', 'Debit Card'),
(12, '2023-06-28', '2023-07-02', 'Delivered', 'UPI'),
(13, '2023-07-14', '2023-07-18', 'Delivered', 'Credit Card'),
(14, '2023-07-30', '2023-08-03', 'Delivered', 'COD'),
(15, '2023-08-16', '2023-08-20', 'Delivered', 'UPI'),
(1,  '2023-08-29', '2023-09-02', 'Delivered', 'Credit Card'),
(3,  '2023-09-14', '2023-09-18', 'Delivered', 'UPI'),
(5,  '2023-09-28', '2023-10-02', 'Delivered', 'COD'),
(7,  '2023-10-13', '2023-10-17', 'Delivered', 'UPI'),
(9,  '2023-10-27', '2023-10-31', 'Delivered', 'Credit Card'),
(2,  '2023-11-09', '2023-11-13', 'Delivered', 'Debit Card'),
(4,  '2023-11-20', '2023-11-24', 'Delivered', 'UPI'),
(6,  '2023-12-04', '2023-12-08', 'Delivered', 'Credit Card'),
(8,  '2023-12-18', '2023-12-22', 'Delivered', 'UPI'),
(10, '2024-01-06', '2024-01-10', 'Delivered', 'COD'),
(12, '2024-01-20', '2024-01-24', 'Delivered', 'UPI'),
(14, '2024-02-03', '2024-02-07', 'Delivered', 'Credit Card'),
(1,  '2024-02-17', '2024-02-21', 'Delivered', 'UPI'),
(11, '2024-03-05', '2024-03-09', 'Delivered', 'Debit Card'),
(13, '2024-03-22', '2024-03-26', 'Delivered', 'UPI');
GO

-- ============================================
-- TABLE 6: order_items
-- ============================================
CREATE TABLE order_items (
    item_id    INT IDENTITY(1,1) PRIMARY KEY,
    order_id   INT,
    product_id INT,
    quantity   INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount   DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
GO

INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount) VALUES
(1,  5,  1, 3499.00, 10.00),
(1,  2,  2,  799.00,  5.00),
(2,  4,  1, 1899.00, 15.00),
(2,  6,  1, 2999.00, 20.00),
(3,  9,  1, 6999.00,  0.00),
(3,  3,  2, 1299.00, 10.00),
(4,  8,  1, 1699.00, 15.00),
(4, 10,  1, 2799.00, 10.00),
(5,  1,  2, 1499.00,  5.00),
(5, 15,  1, 1999.00,  0.00),
(6, 14,  1, 4999.00, 20.00),
(6, 12,  2, 1799.00, 10.00),
(7, 17,  1, 4999.00, 15.00),
(7, 20,  2, 1299.00,  5.00),
(8,  9,  1, 6999.00,  0.00),
(8, 18,  2, 1299.00, 10.00),
(9, 11,  1, 4499.00, 20.00),
(9, 16,  1, 2299.00, 15.00),
(10, 4,  2, 1899.00, 10.00),
(10,19,  3,  999.00,  5.00),
(11, 6,  1, 2999.00, 20.00),
(11, 7,  1, 2499.00, 10.00),
(12,10,  1, 2799.00, 15.00),
(12,12,  2, 1799.00,  5.00),
(13, 5,  1, 3499.00, 10.00),
(13,13,  1, 1599.00,  0.00),
(14, 9,  1, 6999.00,  0.00),
(14,18,  1, 1299.00, 10.00),
(15, 4,  2, 1899.00, 15.00),
(15, 8,  1, 1699.00, 10.00),
(16,17,  1, 4999.00, 20.00),
(16, 2,  3,  799.00,  5.00),
(17,11,  1, 4499.00, 15.00),
(17,16,  2, 2299.00, 10.00),
(18, 9,  1, 6999.00,  0.00),
(18,20,  2, 1299.00,  5.00),
(19, 6,  1, 2999.00, 20.00),
(19, 7,  2, 2499.00, 10.00),
(20,14,  1, 4999.00, 25.00),
(20,12,  1, 1799.00, 10.00),
(21, 5,  2, 3499.00, 10.00),
(21,15,  1, 1999.00,  0.00),
(22,10,  1, 2799.00, 15.00),
(22, 4,  2, 1899.00, 10.00),
(23, 9,  1, 6999.00,  0.00),
(23,13,  2, 1599.00,  5.00),
(24,18,  2, 1299.00, 10.00),
(24,19,  3,  999.00,  5.00),
(25, 6,  1, 2999.00, 20.00),
(25,11,  1, 4499.00, 15.00),
(26,17,  1, 4999.00, 20.00),
(26, 2,  2,  799.00,  5.00),
(27, 5,  1, 3499.00, 10.00),
(27,16,  1, 2299.00, 15.00),
(28, 9,  2, 6999.00,  0.00),
(28,20,  1, 1299.00,  5.00),
(29,14,  1, 4999.00, 25.00),
(29, 7,  1, 2499.00, 10.00),
(30, 4,  2, 1899.00, 15.00),
(30,12,  2, 1799.00, 10.00);
GO

-- ============================================
-- VERIFY: Sab tables check karo
-- ============================================
SELECT 'regions'     AS table_name, COUNT(*) AS total_rows FROM regions
UNION ALL
SELECT 'customers',   COUNT(*) FROM customers
UNION ALL
SELECT 'brands',      COUNT(*) FROM brands
UNION ALL
SELECT 'products',    COUNT(*) FROM products
UNION ALL
SELECT 'orders',      COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;
GO
