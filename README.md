# Online_Retail_Store

# Database Management System

## Croma - Online Retail DBMS

### Group Members
- Ashish Bargoti (2022114)
- Debjit Banerji (2022146)
- Kartikeya Sehgal (2022244)

## Introduction
Our project aims to build a database management system for Croma’s online retail store. Croma is a popular retail store for electronics and other related consumer goods. Our database application will focus solely on its online platform and exclude its offline stores from further discussions. This project's scope encompasses the management of the products, user profiles, procurement of electronic goods from suppliers, and inventory. This project will also aid in the administration of the distribution of the items, which includes the orders placed by the users and by Croma for stock replenishment. Focusing solely on the online platform makes the database system implementation precise and easily manageable. Separating back-end functions into distinct entities, like inventory, distribution, and procurement, ensures a modular design, enhancing scalability.

## Features Implemented

### 1) Login Page
On the login page, users can choose to “Login” or “Register” as a Customer or “Login” as an Admin.

If the user wishes to “Login” or “Register” as a Customer, he/she has to select the “Customer” option from the given choices.

Then, he/she will be redirected to a screen where the customer needs to select one of the available options: “Login” or “Register”.

If the customer chooses the “Register” option, he/she will be redirected to fill in his/her details and create an account.

For the purpose of this explanation, we’ll be logging into an existing account. This is done by selecting the “Login” option from the previous screen and entering the details of the existing account.

(Note: The customer will have the choice to select between “Phone Number” and “Email-ID” as options to login.)

Finally, for logging into the website as an Admin, on the first screen, the user should choose the “Admin” option on the first screen.

### 2) Customer Home Page
After logging into the Customer Side, the customer will be greeted with the following screen:

The features include “View Products”, “View Cart”, “My Wishlist”, “Customer Profile”, “Edit Profile”, and “Order History”, along with the “Logout” option to return to the “Login Page”.

(Note: The features accessible to the customer are all visible on the navigation bar on the left side of the screen.)

#### i) View Products
In this section, the customer is given the option to search for all products containing the keyword he/she searched for in the search bar. The relevant results are then displayed:

When the customer clicks on the “View Details” button, the customer will be given an option to view the details of the selected product on the left navigation pane. 

The “Product_Details” Page will allow the user to view the details of the selected product like description, price, rating, reviews about the product, product name and other details.

From the “Product_Details” page, the user will be able to add the product he/she is viewing to his cart or to his wishlist.

#### ii) View Cart
In this section, the customer can view and edit the quantities of items saved in his cart. He can also press the “Place Order” button to move to the checkout page to place his order. After the order gets placed, the products in the customer’s cart will be truncated. The customer will only be able to move to the “Proceed to Checkout” Page if the quantity of each product in his cart can be satisfied by the total quantity of products available in the inventory.

#### iii) My Wishlist
In this section, the customer will be able to view the products he/she has added to his wishlist to be purchased later along with the date when he/she added the items to his/her wishlist.

#### iv) Customer Profile
In this section, the customer will be able to view the details of his account like Name, Contact No., Email, and Addresses.

#### v) Edit Profile
In this section, the customer can edit his profile details like Name, Contact No, Email, and Address. The customer can choose which field to edit by choosing the appropriate option from the dropdown menu.

#### vi) Order History
In this section, the customer can view his/her previously purchased products along with the quantity purchased and their last purchase date.

### 3) Admin Home Page
After logging into the Admin Side, the admin will be greeted with the following screen:

The features include “View Order Statistics”, “View Registered Accounts”, “Inventory Details”, “Modify Product Catalogue”, “Update Warehouse Details”, “Submit Custom Query” and “Place Shipment Order”, along with the “Logout” option to return to the “Login Page”.

(Note: The features accessible to the admin are all visible on the navigation bar on the left side of the screen.)

#### i) View Order Statistics
This feature presents statistics related to orders, such as Order ID, Customer ID, and Order Placement Date. Additionally, it displays the distribution of customers by state in the form of a line graph.

#### ii) View Registered Accounts
View Registered Accounts functionality accesses the database to fetch and exhibit essential details of registered customer accounts, comprising Customer ID, First Name, and Last Name, facilitating effective management and analysis.

#### iii) Inventory Details
The Inventory Details feature offers comprehensive insights into inventory management. It furnishes crucial details such as Product ID, Warehouse ID, Quantity, and Supplier ID, alongside comprehensive data on purchase orders and shipment details for enhanced operational oversight.

#### iv) Modify Product Catalogue
This feature allows administrators to add, delete, or update product details in the product catalogue. It includes options to add a new product, delete an existing product, or modify the details of an existing product.

#### v) Update Warehouse Details
Update Warehouse Details empowers administrators to maintain warehouse records efficiently. It facilitates the modification of key information like Name, Contact Number, Area, City, State, Country, and Pincode, ensuring accurate and up-to-date warehouse management.

#### vi) Submit Custom Query
This section allows the admin to write a custom query to query the database in a specific way to retrieve specialised information.

#### vii) Place Shipment Order
In this section, the admin can place shipment orders to restock the inventory in various warehouses by ordering particular products from particular suppliers. The admin can choose the “Warehouse”, “Supplier” and “Product” for the shipment order by using the options displayed in the drop-down menus. The admin also needs to enter the quantity of the products to be shipped.

## Instructions to Run
Clone the repository<br>
Run cromaScript.sql on mysql<br>
Edit Mysql local password inside launch_connection() method inside utility.py <br>
Run `Streamlit run Home.py` on the terminal.
