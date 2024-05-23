DROP DATABASE croma_online;
CREATE DATABASE croma_online;
USE croma_online;

CREATE TABLE customer (
  Customer_ID INT PRIMARY KEY AUTO_INCREMENT,
  First_Name VARCHAR(255) NOT NULL,
  Middle_Name VARCHAR(255),
  Last_Name VARCHAR(255) NOT NULL,
  Email_ID VARCHAR(255) UNIQUE NOT NULL,
  Password VARCHAR(255) NOT NULL,
  Contact_Number VARCHAR(20) UNIQUE NOT NULL,
  Payment_Mode VARCHAR(50) NOT NULL
);

CREATE TABLE addresses (
  Customer_ID INT NOT NULL,
  Address_Type ENUM ('Home','Work','Other'),
  House_No VARCHAR(10) NOT NULL,
  Street VARCHAR(255) NOT NULL,
  Area VARCHAR(255) NOT NULL,
  City VARCHAR(50) NOT NULL,
  State VARCHAR(50) NOT NULL,
  Pincode INT NOT NULL,
  Contact_Number VARCHAR(20),
  PRIMARY KEY (Customer_ID, Address_Type, House_No ),
  FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID)
);

CREATE TABLE products (
  Product_ID INT PRIMARY KEY auto_increment,
  Name VARCHAR(255) NOT NULL,
  Category1 VARCHAR(50) NOT NULL,
  Category2 VARCHAR(50),
  Category3 VARCHAR(50), 
  Brand_Name VARCHAR(100) NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  Description TEXT NOT NULL
);

CREATE TABLE cart (
  Customer_ID INT NOT NULL,
  Product_ID INT NOT NULL, 
  Quantity INT NOT NULL,
  Total_Price DECIMAL(10,2) NOT NULL,
  Added_Date DATE,
  PRIMARY KEY (Customer_ID, Product_ID),
  FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

CREATE TABLE delivery_agents (
  Agent_ID INT PRIMARY KEY auto_increment,
  Name VARCHAR(255) NOT NULL,
  Contact_No VARCHAR(20) NOT NULL,
  Contract_Start_Date date DEFAULT NULL,
  Contract_End_Date date DEFAULT NULL,
  Description TEXT NOT NULL,
  Service_Type VARCHAR(100) NOT NULL  
);

CREATE TABLE warehouses (
  Warehouse_ID INT PRIMARY KEY auto_increment,
  Name VARCHAR(255) NOT NULL,
  Contact_No VARCHAR(20) NOT NULL,
  Area VARCHAR(255) NOT NULL,
  City VARCHAR(50) NOT NULL,
  State VARCHAR(50) NOT NULL,
  Country VARCHAR(50) NOT NULL,
  Pincode INT NOT NULL,
  Starting_Date date DEFAULT NULL
);

CREATE TABLE suppliers (
  Supplier_ID INT PRIMARY KEY auto_increment,
  Name VARCHAR(255) NOT NULL,
  Email_ID VARCHAR(255) UNIQUE NOT NULL,
  Contact_No VARCHAR(20) UNIQUE NOT NULL,
  Description TEXT NOT NULL,
  Contract_Start_Date date DEFAULT NULL,
  Contract_End_Date date DEFAULT NULL
);  

CREATE TABLE inventory (
  Product_ID INT NOT NULL,
  Warehouse_ID INT NOT NULL, 
  Quantity INT NOT NULL,
  Last_Supply_Date DATE NOT NULL, 
  Supplier_ID INT NOT NULL,
  PRIMARY KEY (Product_ID, Warehouse_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID),
  FOREIGN KEY (Warehouse_ID) REFERENCES warehouses(Warehouse_ID),
  FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID)
);

CREATE TABLE orders (
  Order_ID INT PRIMARY KEY AUTO_INCREMENT,
  Customer_ID INT NOT NULL,
  Order_Placement_Date DATE,
  Discount DECIMAL(10,2) NOT NULL,
  address_type ENUM ('Home','Work','Other'),
  house_no VARCHAR(10) NOT NULL,
  FOREIGN KEY (Customer_ID, address_type, house_no) REFERENCES ADDRESSES(customer_id, address_type, house_no),
  FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID)
);

CREATE TABLE OrderItems (
  Order_ID INT NOT NULL,
  Product_ID INT NOT NULL,
  Quantity INT NOT NULL,
  PRIMARY KEY (Order_ID, Product_ID),
  FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);
-- 'Restock_details': we are storing which order was placed for which warehouse
-- for which product to which supplier at what date and with what quantity
CREATE TABLE Restock_details (
  Restock_ID INT PRIMARY KEY auto_increment,
  Warehouse_ID INT,
  Supplier_ID INT,
  Product_ID INT,
  Quantity INT NOT NULL,
  Date_Of_Purchase DATE,
  foreign key (Warehouse_ID) references Warehouses(Warehouse_ID),
  FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

CREATE TABLE PURCHASE_ORDER (
  Purchase_Order_ID INT PRIMARY KEY AUTO_INCREMENT,
  Payment_Mode VARCHAR(50) NOT NULL,
  Total_Amount Decimal(10,2) NOT NULL,
  Payment_Status VARCHAR(25) NOT NULL DEFAULT 'Pending',
  Payment_Date DATE DEFAULT NULL,
  Payment_Time TIME DEFAULT NULL
);

CREATE TABLE RESTOCK_PER_PO(
  Purchase_Order_ID INT NOT NULL,
  Restock_ID INT NOT NULL,
  PRIMARY KEY( Purchase_Order_ID, Restock_ID ),
  foreign key (Restock_ID) references Restock_details(Restock_ID),
  foreign key (Purchase_Order_ID) references PURCHASE_ORDER(Purchase_Order_ID)
);

CREATE TABLE shipments (
  Shipment_ID INT AUTO_INCREMENT PRIMARY KEY,
  Mfg_Date DATE,
  Purchase_Order_ID INT NOT NULL,
  Shipment_Date DATE NOT NULL,
  Delivery_Date DATE DEFAULT NULL,
  FOREIGN KEY (Purchase_Order_ID) REFERENCES PURCHASE_ORDER(Purchase_Order_ID),
  CHECK (Delivery_Date IS NULL OR Delivery_Date > Shipment_Date),
  CHECK (Mfg_Date <= Shipment_Date)
);

CREATE TABLE product_returns (
  Return_ID INT PRIMARY KEY,
  Product_ID INT NOT NULL,
  Customer_ID INT NOT NULL,
  Return_Date DATE NOT NULL,
  Return_Status VARCHAR(50) NOT NULL DEFAULT 'Pending',
  Order_ID INT NOT NULL,
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID),
  FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID),
  FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID)
);

CREATE TABLE product_reviews (
  Review_ID INT PRIMARY KEY,
  Customer_ID INT NOT NULL,
  Product_ID INT NOT NULL,
  Rating INT NOT NULL,
  Review TEXT NOT NULL,
  Review_Date DATE,
  FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

CREATE TABLE Shipment_Supplier_Index (
  Supplier_ID INT NOT NULL,
  Product_ID INT NOT NULL,
  Shipment_ID INT NOT NULL,
  Quantity INT NOT NULL,
  PRIMARY KEY (Supplier_ID, Product_ID, Shipment_ID),
  foreign key (Shipment_ID) references shipments(Shipment_ID),
  FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

CREATE TABLE Product_supplier (
  Supplier_ID INT,
  Product_ID INT,
  PRIMARY KEY (Supplier_ID, Product_ID),
  FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

CREATE TABLE transactions (
  Transaction_ID INT PRIMARY KEY auto_increment,
  Order_ID INT NOT NULL UNIQUE,
  Payment_Mode VARCHAR(50) NOT NULL,
  Payment_Status VARCHAR(50) NOT NULL, 
  Amount_Paid DECIMAL(10,2) DEFAULT NULL,
  Transaction_Time TIMESTAMP,
  Transaction_Date DATE,
  FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID)
);

CREATE TABLE wishlist (
  Customer_ID INT NOT NULL,
  Product_ID INT NOT NULL,
  Added_Date DATE,
  PRIMARY KEY ( Customer_ID, Product_ID, Added_Date ), 
  FOREIGN KEY (Customer_ID) REFERENCES customer(Customer_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

CREATE TABLE delivery_details (
  Order_ID INT NOT NULL UNIQUE,
  Delivery_Agent_ID INT NOT NULL,
  Dispatch_Date DATE,
  Delivery_Status ENUM('Placed','Dispatched', 'Out for delivery') DEFAULT 'Placed',
  PRIMARY KEY( Order_ID, Delivery_Agent_ID ),
  FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID),
  FOREIGN KEY (Delivery_Agent_ID) REFERENCES delivery_agents(Agent_ID)
);

CREATE TABLE Shipment_Delivery (
  Shipment_ID INT NOT NULL,
  Warehouse_ID INT NOT NULL,
  Product_ID INT NOT NULL,
  Quantity_Received INT NOT NULL,
  Received_Date DATE,
  PRIMARY KEY (Shipment_ID, Warehouse_ID, Product_ID),
  FOREIGN KEY (Shipment_ID) REFERENCES shipments(Shipment_ID),
  FOREIGN KEY (Warehouse_ID) REFERENCES warehouses(Warehouse_ID),
  FOREIGN KEY (Product_ID) REFERENCES products(Product_ID)
);

INSERT INTO customer (Customer_ID, First_Name, Middle_Name, Last_Name, Email_ID, Password, Contact_Number, Payment_Mode) 
VALUES
(1, 'Rajesh', 'Kumar', 'Sharma', 'rajesh.sharma@example.com', 'password123', '9876543210', 'Credit Card'),
(2, 'Priya', 'Singh', 'Patel', 'priya.patel@example.com', 'password456', '1234567890', 'PayPal'),
(3, 'Amit', NULL, 'Verma', 'amit.verma@example.com', 'password789', '9876123450', 'Debit Card'),
(4, 'Sneha', 'Rani', 'Gupta', 'sneha.gupta@example.com', 'passwordabc', '9988776655', 'Cash'),
(5, 'Neha', 'Kumari', 'Jha', 'neha.jha@example.com', 'passwordxyz', '7755889966', 'Credit Card'),
(6, 'Vikas', NULL, 'Yadav', 'vikas.yadav@example.com', 'password1234', '6655443322', 'PayPal'),
(7, 'Shreya', 'Singh', 'Sharma', 'shreya.sharma@example.com', 'password5678', '9876541235', 'Debit Card'),
(8, 'Rohit', 'Kumar', 'Gupta', 'rohit.gupta@example.com', 'password9012', '9988778655', 'Cash'),
(9, 'Pooja', NULL, 'Mishra', 'pooja.mishra@example.com', 'password3456', '7755889066', 'Credit Card'),
(10, 'Anuj', 'Singh', 'Verma', 'anuj.verma@example.com', 'password7890', '6655403322', 'PayPal');

INSERT INTO addresses (Customer_ID, Address_Type, House_No, Street, Area, City, State, Pincode, Contact_Number) VALUES  
(1, 'Home','B-201', 'Main Street', 'Sector 15', 'Noida', 'Uttar Pradesh', 201301, '1234567890'),
(1, 'Work','H-611', 'DLF Avenue', 'Sector 34', 'Gurgaon', 'Haryana', 122006, '1234567890'),
(2, 'Home','A-402', 'Park Avenue', 'Sector 63', 'Noida', 'Uttar Pradesh', 201302, '0987654321' ),
(3, 'Home','13', 'High Street', 'Sector 31', 'Gurgaon', 'Haryana', 122001, '1112223333'), 
(4, 'Home','306', 'Central Street', 'Sector 15', 'Chandigarh', 'Punjab', 160031, '4445556666'),
(5, 'Home','P-7', 'Broadway', 'Sector 12', 'Kolkata', 'West Bengal', 700014, '7777888999'),
(6, 'Home','45', 'Main Road', 'Banaswadi', 'Bangalore', 'Karnataka', 560043, '333111222'),  
(7, 'Home','A-45', 'MG Road', 'Vasant Vihar', 'New Delhi', 'New Delhi', 110057, '5556667777'),
(8, 'Home','23', 'Church Street', 'Indiranagar', 'Bangalore', 'Karnataka', 560038, '9990008888'), 
(9, 'Home','15', 'Park Street', 'Salt Lake', 'Kolkata', 'West Bengal', 700064, '1231231234'),
(10, 'Home','402', 'Nehru Street', 'Dwarka', 'New Delhi', 'New Delhi', 121998, '3213213213'),
(10, 'Other','C-312', 'GF,Roy Avenue', 'Indiranagar', 'Bangalore', 'Karnataka', 560038, '3213213213');


INSERT INTO products (Name, Category1, Category2, Category3, Brand_Name, Price, Description) VALUES  
('iPhone 14', 'Mobiles', 'Smartphones', NULL, 'Apple', 89900.00, 'Latest iPhone model'),
('OnePlus 10T', 'Mobiles','Smartphones', NULL, 'OnePlus', 54999.00, 'Flagship OnePlus smartphone'),  
('Fire TV Stick', 'Electronics', 'Streaming Devices', NULL, 'Amazon', 3499.00, 'Streaming device by Amazon'),
('Boat Rockerz 335', 'Electronics', 'Headphones', 'Wireless', 'Boat', 1299.00, 'Wireless Bluetooth headphones'), 
('Mi Robot Vacuum', 'Appliances', 'Vacuum Cleaners', NULL, 'Xiaomi', 21999.00, 'Robot vacuum cleaner'),  
('IFB Washing Machine','Appliances', 'Washing Machines', NULL, 'IFB', 29999.00, 'Fully automatic washing machine'),
('Samsung Fridge', 'Appliances', 'Refridgerators', NULL, 'Samsung', 109999.00, 'Dual Inverter'),
('Smart LG TV', 'Appliances', 'Television', NULL,'LG', 100299.00, '75 inch OLED Screen'),
('HP 15 Laptop','Electronics', 'Laptops', NULL,'HP',41999.00, '15 inch screen laptop'), 
('Boat Airdopes 131', 'Electronics', 'Headphones', 'TWS Earbuds', 'Boat', 1299.00, 'Wireless bluetooth earbuds');

INSERT INTO cart (Customer_ID, Product_ID, Quantity, Total_Price, Added_Date) VALUES
(1, 1, 100, 8990000.00, '2023-02-10'),  
(3, 3, 2, 6998.00, '2023-02-11'),
(5, 7, 1, 109999.00, '2023-02-09'),
(2, 2, 1, 54999.00, '2023-02-12'),  
(7, 9, 1, 41999.00, '2023-02-11'),
(9, 4, 20, 25980.00, '2023-02-10'),
(4, 5, 1, 21999.00, '2023-02-08'), 
(10, 8, 3, 300897.00, '2023-02-07'),
(8, 6, 1, 29999.00, '2023-02-06'),  
(6, 10, 2, 2598.00, '2023-02-05');

INSERT INTO delivery_agents (Agent_ID, Name, Contact_No, Description, Service_Type) 
VALUES
(1, 'Rahul Kumar', '1112423344', 'Fast and reliable delivery service', 'Express Delivery'),
(2, 'Rohan yadav', '5544667688', 'Specialized in handling electronic gadgets', 'Standard Delivery'),
(3, 'ramesh kumar', '9988976655', 'Swift delivery service for electronics', 'Same-day Delivery'),
(4, 'neel yadav', '2233245566', 'Delivering electronic products with care', 'Standard Delivery'),
(5, 'rakesh', '7788991011', 'Expert in handling fragile electronic items', 'Standard Delivery'),
(6, 'rakesh kumar', '3322210099', 'Efficient delivery service for digital products', 'Standard Delivery'),
(7, 'vipul verma', '4455664788', 'Express delivery for electronic items', 'Express Delivery'),
(8, 'guru', '5566778849', 'Reliable transportation service for tech products', 'Standard Delivery'),
(9, 'gajendra', '6677489900', 'Swift and safe delivery of electronic gadgets', 'Express Delivery'),
(10, 'ramesh kumar', '7788994011', 'Expert handling of delicate electronic devices during delivery', 'Standard Delivery');

INSERT INTO warehouses (Name, Contact_No, Area, City, State, Country, Pincode, Starting_Date) VALUES
('A', '01242345678', 'Sector 63', 'Noida', 'Uttar Pradesh', 'India', 201304, '2017-01-01'),  
('B', '01248765432', 'Banaswadi', 'Bangalore', 'Karnataka', 'India', 560043, '2018-04-01'),
('C', '01243445566', 'Dwarka', 'New Delhi', 'New Delhi', 'India', 110075, '2020-07-15'),   
('D', '01248991122', 'Salt Lake', 'Kolkata', 'West Bengal', 'India', 700064, '2019-02-01'),  
('E', '01248765321', 'Bommanahalli', 'Bangalore', 'Karnataka', 'India', 560068, '2016-11-01'),
('F', '01242345321', 'Sector 31', 'Gurgaon', 'Haryana','India', 122001, '2015-06-01'),
('G', '01244512789', 'Vasant Kunj', 'New Delhi', 'New Delhi','India', 110070, '2022-03-01'),
('H', '01242446688', 'Kalamboli', 'Mumbai', 'Maharashtra','India', 410218, '2021-05-01'), 
('I', '01241122233', 'Sector 5', 'Manesar', 'Haryana', 'India', 122050, '2017-07-01'),
('J', '01248776655', 'Whitefield', 'Bangalore', 'Karnataka', 'India', 560066, '2020-01-15');

INSERT INTO suppliers (Name, Email_ID, Contact_No, Description, Contract_Start_Date, Contract_End_Date) VALUES 
('ABC Supplies', 'abc@example.com','01112345678', 'Leading supplier', '2022-01-01', '2024-12-31'),
('XYZ Distributors', 'xyz@example.com','01198765432', 'Reliable distributor','2021-01-01', NULL),
('Prime Products','prime@example.com','02233445566', 'Bulk supplier', '2023-01-01', NULL), 
('Max Wholesale', 'max@example.com','03388991122', 'Wholesale supplier', '2022-07-01', NULL),
('Swift Suppliers', 'swift@example.com','04498765321','Just-in-time supplier', '2020-01-01', NULL),  
('Shopsy', 'shopsy@example.com','05576849302','Marketplace for suppliers', '2022-04-01', NULL ),
('Kibo Commerce', 'kibo@example.com','06634512789','Dropshipping supplier', '2021-01-01', NULL), 
('Zest Supplies', 'zest@example.com','07722446688','Startup supplier', '2019-01-01', NULL),  
('Ace Distributors', 'ace@example.com', '08811122233','B2B distributors', '2021-05-01', NULL),
('Uni Suppliers', 'uni@example.com','09988776655','Unique products supplier', '2020-07-01', NULL);
                
INSERT INTO inventory (Product_ID, Warehouse_ID, Quantity, Last_Supply_Date, Supplier_ID) VALUES  
(1, 1, 4, '2023-02-10', 1),  
(1, 3, 10, '2023-02-10', 1),  
(2, 2, 50, '2023-02-12', 2),
(3, 3, 300, '2023-02-11', 3),
(4, 4, 10, '2023-02-09', 4), 
(5, 5, 100, '2023-02-08', 5),
(6, 6, 150, '2023-02-15', 6),  
(7, 7, 100, '2023-02-13', 7),  
(8, 8, 400, '2023-02-20', 8),
(9, 9, 200, '2023-02-17', 9),
(10, 10, 500, '2023-02-22', 10);

INSERT INTO orders (Order_ID, Customer_ID,  address_type, house_no, Order_Placement_Date, Discount) VALUES
(1001, 1, 'Home','B-201','2023-02-14', 1000.00),  
(1011, 1, 'Work','H-611', '2023-09-18', 1000.00),
(1004, 2, 'Home','A-402','2023-02-17', 800.00),  
(1002, 3, 'Home','13', '2023-02-15', 500.00),
(1003, 5, 'Home','P-7','2023-02-16', 0), 
(1005, 7, 'Home','A-45','2023-02-18', 1500.00),
(1006, 9, 'Home','15', '2023-02-19', 700.00),  
(1007, 4, 'Home','306', '2023-02-12', 2000.00),
(1008, 10, 'Home','402', '2023-10-14', 250.00),  
(1012, 10, 'Other','C-312', '2023-02-23', 250.00),  
(1009, 8, 'Home','23','2023-02-26', 0),
(1010, 6, 'Home','45', '2023-02-28', 1200.00);

INSERT INTO OrderItems (Order_ID, Product_ID, Quantity) VALUES 
(1001, 1, 1),(1001, 2, 1),(1001, 3, 1),(1001, 4, 5),(1001, 5, 2),
(1002, 3, 2),
(1003, 7, 1),
(1004, 2, 1), (1004, 5, 6),  (1004, 7, 3),  (1004, 1, 10),  (1004, 3, 1),   
(1005, 9, 1), 
(1006, 4, 2),
(1007, 5, 1), (1007, 4, 15), (1007, 3, 1), (1007, 2, 1), (1007, 1, 1), (1007, 6, 1),
(1008, 8, 3),
(1009, 6, 1),
(1011, 7, 1), (1011, 5, 3),
(1012, 2, 1), (1012, 9, 2),
(1010, 10, 2);

INSERT INTO product_reviews (Review_ID, Customer_ID, Product_ID, Rating, Review, Review_Date) VALUES 
(1, 1, 1, 5, 'Excellent phone with great camera and display', '2023-02-15'),
(2, 2, 2, 4, 'Very good performance but battery life could be better', '2023-02-18'),
(3, 3, 3, 5, 'Easy to setup and use streaming device', '2023-02-20'),  
(4, 5, 7, 3, 'Shoes are comfortable but not very durable', '2023-02-22'),
(5, 9, 4, 5, 'Clear sound quality, comfortable for long duration use','2023-02-24'),
(6, 10, 8, 4, 'Good quality tshirt with nice fit', '2023-02-26'),
(7, 6, 5, 5, 'Excellent phone with great camera and display', '2023-02-15'),
(8, 2, 2, 4, 'Very good performance but battery life could be better', '2023-02-18'),
(9, 3, 3, 5, 'Easy to setup and use streaming device', '2023-02-20'),  
(10, 5, 7, 3, 'Shoes are comfortable but not very durable', '2023-02-22');

INSERT INTO wishlist (Customer_ID, Product_ID, Added_Date) VALUES
(3, 5, '2023-02-14'), 
(7, 2, '2023-02-16'),
(4, 9, '2023-02-19'),
(8, 1, '2023-02-21'),
(6, 10, '2023-02-23'),
(3, 7, '2023-02-14'), 
(7, 3, '2023-02-16'),
(4, 6, '2023-02-19'),
(1, 5, '2023-06-19'),
(1, 4, '2023-05-19'),
(1, 3, '2023-04-19'),
(1, 2, '2023-03-19'),
(8, 2, '2023-02-21'),
(6, 8, '2023-02-23');


INSERT INTO transactions (Transaction_ID, Order_ID, Payment_Mode, Payment_Status, Transaction_Date) VALUES  
(101, 1001, 'Credit Card', 'Complete', '2023-02-15'),
(111, 1011, 'Debit Card', 'Complete', '2023-09-18'),

(102, 1002, 'Debit Card', 'Failed', '2023-02-18' ),  
(103, 1003, 'PayPal', 'Complete', '2023-02-20'),
(104, 1005, 'Credit Card', 'Complete', '2023-02-22'),
(105, 1007, 'Cash', 'Complete', '2023-02-25'),
(106, 1004, 'Credit Card', 'Complete', '2023-02-15'),
(107, 1006, 'Debit Card', 'Failed', '2023-02-18' ),  
(108, 1008, 'PayPal', 'Complete', '2023-02-20'),
(109, 1009, 'Credit Card', 'Complete',  '2023-02-22'),

(110, 1010, 'Cash', 'Complete', '2023-02-25'),
(112, 1012, 'PayPal', 'Complete', '2023-02-23');

INSERT INTO delivery_details (Order_ID, Delivery_Agent_ID, Dispatch_Date) VALUES
(1001, 1, '2023-02-16'),  
(1002, 2, '2023-02-20'), 
(1004, 3, '2023-02-23'),
(1006, 4, '2023-02-28'),
(1010, 5, '2023-03-03'),
(1003, 1, '2023-02-16'),  
(1005, 2, '2023-02-20'), 
(1007, 3, '2023-02-23'),
(1008, 4, '2023-02-28'),
(1011, 2, '2024-06-25'),
(1012, 5, '2024-07-25'),
(1009, 5, '2023-03-03');

INSERT INTO Restock_details (Restock_ID, Warehouse_ID, Supplier_ID, Product_ID, Quantity, Date_Of_Purchase) VALUES  
(1, 1, 1, 1, 100, '2023-02-10'),
(2, 2, 2, 2, 50, '2023-02-11'),
(3, 3, 3, 3, 300, '2023-02-15'), 
(4, 4, 4, 4, 200, '2023-02-18'),
(5, 5, 5, 5, 100, '2023-02-20'),
(6, 1, 1, 7, 100, '2023-02-22'),
(7, 2, 2, 8, 400, '2023-02-24'),  
(8, 3, 3, 9, 200, '2023-02-26'),
(9, 4, 4, 10, 500, '2023-02-28'),
(10, 5, 5, 6, 150, '2023-03-02'),
(11, 5, 8, 3, 1350, '2023-09-02');


INSERT INTO PURCHASE_ORDER (Purchase_Order_ID, Payment_Mode, Total_Amount ) VALUES
(501, 'Bank Transfer', 9000000),  
(502,'Credit Card', 2750000),
(503,'Debit Card', 10500000),  
(504, 'UPI', 7000000),
(505, 'Bank Transfer', 5500000),
(506, 'Credit Card', 6000000), 
(507,  'Debit Card', 10000000),
(508,  'UPI', 7500000),  
(509,  'Bank Transfer', 9500000),
(510,  'Credit Card', 6500000);

INSERT INTO RESTOCK_PER_PO( Purchase_Order_ID, Restock_ID ) VALUES
(501,1 ),  (501,11 ),   
(502,2),
(504,4),
(505, 5),
(506,6 ), 
(507, 7),
(508,8 ),  
(509, 9),
(510, 10 );

INSERT INTO shipments (Shipment_ID, Purchase_Order_ID, Mfg_Date, Shipment_Date) VALUES 
(1, 501, '2023-02-05', '2023-02-12'), 
(2, 502, '2023-02-07', '2023-02-15'),
(3, 503, '2023-02-10', '2023-02-18'), 
(4, 504, '2023-02-11', '2023-02-20'),
(5, 505, '2023-02-15', '2023-02-22'),  
(6, 506, '2023-02-16', '2023-02-24'),   
(7, 507, '2023-02-20', '2023-02-26'),
(8, 508, '2023-02-25', '2023-02-28'),
(9, 509, '2023-02-27', '2023-03-02'),
(10, 510, '2023-03-01', '2023-03-04'),
(11, 510, '2023-04-12', '2023-06-08');


INSERT INTO product_returns(Return_ID, Product_ID, Customer_ID, Return_Date, Order_ID ) VALUES  
(101, 1, 1, '2023-02-18', 1001),  
(102, 2, 2, '2023-02-22', 1004), 
(103, 4, 6, '2023-02-26', 1006),
(104, 5, 10, '2023-02-28', 1010),
(105, 7, 5, '2023-03-02', 1003),
(106, 8, 8, '2023-03-05', 1009),
(107, 9, 7, '2023-03-08', 1005),  
(108, 10, 3, '2023-03-11', 1002),
(109, 3, 9, '2023-03-15', 1006),
(110, 6, 4, '2023-03-18', 1007);

INSERT INTO Shipment_Supplier_Index(Supplier_ID, Product_ID,Shipment_ID, Quantity) VALUES
(1, 1, 1, 50),  
(2, 2, 2, 25), 
(3, 3, 3, 100),
(4, 4, 4, 100),
(5, 5, 5, 50), 
(1, 7, 6, 50),  
(2, 8, 7, 200),
(3, 9, 8, 50),
(4, 10,9, 200),
(5, 6, 10, 80);

INSERT INTO Product_supplier (Supplier_ID, Product_ID) VALUES  
(1,1), (1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
(2,2),(2,8),  
(3,3),(3,2),(3,5),(3,4), (3,9),  
(4,4), (4,10), 
(5,5), (5,6),
(6,3),
(7,4),
(8,1),
(9,2);

INSERT INTO Shipment_Delivery (Shipment_ID, Warehouse_ID, Product_ID, Quantity_Received, Received_Date) 
VALUES  
(1, 1, 1, 100, '2023-02-15'),
(2, 2, 2, 50, '2023-02-18'),  
(3, 3, 3, 200, '2023-02-20'),
(4, 4, 4, 150, '2023-02-22'),
(5, 5, 5, 80, '2023-02-24'),
(6, 6, 6, 120, '2023-02-26'),
(7, 1, 7, 90, '2023-02-28'),
(8, 2, 8, 250, '2023-03-02'),
(9, 3, 9, 100, '2023-03-05'),
(11, 3, 6, 145, '2024-01-03'),
(10, 4, 10, 350, '2023-03-10');
