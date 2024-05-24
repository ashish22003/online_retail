
from utility import st, launch_connection, pd, np, plt,ms

from menu import menu_with_redirect

# from Home import launch_connection;
db = launch_connection()
cur=db.cursor()

def place_shipment_orders():
    st.header("Place Shipment Orders")
    cur.execute(f"Select W.Warehouse_ID, W.Name from warehouses W")
    temp = cur.fetchall()
    warehouse_options = {}
    for item in temp:
        warehouse_options[item[1]] = item[0]
    selected_option1 = st.selectbox("Select Warehouse to Restock:",warehouse_options.keys())
    cur.execute(f"Select S.Supplier_ID, S.Name from Suppliers S")
    res = cur.fetchall()
    supplier_options = {}
    for item in res:
        supplier_options[item[1]] = item[0]
    selected_option2 = st.selectbox("Select Supplier:",supplier_options.keys())
    cur.execute(f"Select T.Product_ID, P.Name from Product_supplier T, Products P where T.Supplier_ID = ({supplier_options[selected_option2]}) AND P.Product_ID = T.Product_ID")
    res2 = cur.fetchall()
    product_options = {}
    for item in res2:
        product_options[item[1]] = item[0]
    selected_option3 = st.selectbox("Select Product to be Ordered:",product_options.keys())
    quantity = st.text_input("Quantity of Product to be ordered: ",key = str(warehouse_options[selected_option1])+str(supplier_options[selected_option2])+str(product_options[selected_option3]))
    if(st.button("Place Order")):
        cur.execute(f"Insert INTO Restock_details (Warehouse_ID,Supplier_ID, Product_ID, Quantity, Date_Of_Purchase) VALUES ({warehouse_options[selected_option1]},{supplier_options[selected_option2]},{product_options[selected_option3]},{quantity},CURDATE())") 
        st.success("Order Placed Successfully!")
        db.commit()
        # Add more records into tables Purchase Order and Shipments and alter the table structure to have a forign key named "Restock_ID" in the table "Purchase_Order" to delete an extra table "Restock_per_po"


def view_registered_accounts():
    st.subheader("View Registered Accounts")
    df = pd.read_sql("SELECT Customer_ID, First_Name, Last_Name FROM customer;", con=db)
    st.table(df.style.format({"Customer_ID": "{:05d}"}))  # Format Customer_ID with leading zeros

# Function to view order statistics
def view_order_statistics():
    st.markdown("# Order Statistics")
    
    order_df = pd.read_sql("SELECT Order_ID, Customer_ID, Order_Placement_Date FROM orders;", con=db) 
    product_df = pd.read_sql("SELECT Product_ID, COUNT(Order_ID) AS Num_Orders, SUM(Quantity) AS Total_Quantity FROM OrderItems GROUP BY Product_ID;", con=db) 
    cart_df = pd.read_sql("SELECT Customer_ID, SUM(Total_Price) AS Total_Price FROM cart GROUP BY Customer_ID;", con=db) 
    address_df = pd.read_sql("SELECT State, COUNT(Customer_ID) AS Num_Customers FROM addresses GROUP BY State;", con=db) 

    # Display order data 
    st.markdown("## Placed Orders:") 
    st.table(order_df.style.format({"Order_ID": "{:06d}", "Customer_ID": "{:05d}"}))  # Format IDs 

    # Display product statistics 
    st.markdown("## Product Statistics:") 
    st.table(product_df) 

    # Display unplaced orders (cart) 
    st.markdown("# Unplaced Order(Cart):") 
    st.table(cart_df) 

    # Display state-wise orders distribution 
    st.markdown("## State-wise Orders Distribution") 
    st.write(address_df) 
    plot_statewise_orders(address_df)

# Function to plot state-wise orders distribution
def plot_statewise_orders(address_df):
    plt.figure(figsize=(10, 6))
    plt.plot(address_df['State'], address_df['Num_Customers'], marker='o', color='b', linewidth=2)
    plt.xlabel('State')
    plt.ylabel('Number of Customers')
    plt.title('State-wise Customers Distribution')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.gca().set_facecolor('black')  # Set background color to black
    plt.grid(True, linestyle='--', color='gray', alpha=0.5)  # Add gridlines
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    st.pyplot(plt.gcf())  # Get current figure and pass it to st.pyplot()


def inventory_details():
    st.markdown("# Inventory Details")

    # displaying inventory details
    cur.execute("select  Product_ID,Warehouse_ID,Quantity,Supplier_ID from inventory;")
    result=cur.fetchall()
    temp=[("Product_ID","Warehouse_ID","Quantity","Supplier_ID")] + (list)(result)
    st.table(temp)

    # purchase details
    st.markdown("# Inventory Purchase Details:")
    cur.execute("select * from PURCHASE_ORDER;")
    result=cur.fetchall()
    temp=[("Purchase_ID","Payment_Mode","Total_Amount","Payment Status","Payment Date","Payment Time")] + (list)(result)
    st.table(temp)
    
    #Shipments Details
    st.markdown("# Shipment Details:")
    cur.execute("select * from Shipment_Supplier_Index;")
    result=cur.fetchall()
    temp=[("Supplier_ID", "Product_ID", "Shipment_ID","Quantity")] + (list)(result)
    st.table(temp)

def modify_product_add():
    st.markdown("# Add product")
    # product_id=st.text_input("product_ID")
    name=st.text_input("Name")
    category1=st.text_input("Category1")
    category2=st.text_input("Category2")
    category3=st.text_input("Categor3")
    brand=st.text_input("Brand_Name")

    price=st.text_input("price")
    desc=st.text_area("Product Desc")
    
    # Starting_Date=st.text_input("Starting_Date")
    submit=st.button("Add")
    

    if(submit==True):
        
        
        if(price==""):
            st.error("Invalid Price!")
        else:
            cur.execute("INSERT INTO products (Name, Category1, Category2, Category3, Brand_Name, Price, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)",(name,category1,category2,category3,brand,price,desc))
            
            # cur.execute("update products set name=%s,category1=%s,category2=%s,category3=%s,brand_name=%s,price=%s where product_ID=%s;",(name,category1,category2,category3,brand,price,product_id))
            db.commit()
            st.success("Record added successfully!")

def modify_product_delete():
    st.markdown("# Delete Product")
    product_id=st.text_input("Product_ID")
    if(st.button("Delete")):
        product_id=int(product_id)
        # price=float(price)
        cur.execute("set sql_safe_updates=0;")
        cur.execute("select  product_ID from products;")
        result=cur.fetchall()
        l=[]
        # checking whether the user gave correct product id
        for i in result:
            l.append(i[0])
        if (product_id not in l):
            # if incorrect product_id then error

            st.error("Incorrect Product_Id")
        else:

            cur.execute("delete from products where product_id=%s",(product_id))
            db.commit()
            st.success("Record updated successfully!")
        
def modify_product_update():
    submit=False
    # st.subheader("Update Product details")
    st.markdown("### Update Product details:")
    product_id=st.text_input("product_ID")
    name=st.text_input("Name")
    category1=st.text_input("Category1")
    category2=st.text_input("Category2")
    category3=st.text_input("Categor3")
    brand=st.text_input("Brand_Name")

    price=st.text_input("price")
    
    # Starting_Date=st.text_input("Starting_Date")
    submit=st.button("update")
    

    if(submit==True):
        product_id=int(product_id)
        # price=float(price)
        cur.execute("select  product_ID from products;")
        result=cur.fetchall()
        l=[]
        for i in result:
            l.append(i[0])
        # print(l)
        
        if (product_id not in l):
            st.error("Incorrect Product_Id")
        elif(price==""):
            st.error("Invalid Price!")
        else:
            
            cur.execute("update products set name=%s,category1=%s,category2=%s,category3=%s,brand_name=%s,price=%s where product_ID=%s;",(name,category1,category2,category3,brand,price,product_id))
            db.commit()
            st.success("Record updated successfully!")



def modify_product_catalogue():
    st.markdown("## Modify Product Catalogue")
    selected_option=st.sidebar.radio("Select",["Add Product","Delete Product","Modify Product"])
    if(selected_option=="Delete Product"):
        modify_product_delete()
    elif(selected_option=="Modify Product"):
        modify_product_update()
    elif(selected_option=="Add Product"):
        modify_product_add()


def update_warehouse_details():
    submit=False
    st.subheader("Update Warehouse details")
    warehouse_id=st.text_input("warehouse_ID")
    name=st.text_input("Name")
    contact=st.text_input("Contact_No")
    area=st.text_input("Area")
    city=st.text_input("City")
    country=st.text_input("Country")
    state=st.text_input("State")
    Pincode=st.text_input("Pincode")
    # Starting_Date=st.text_input("Starting_Date")
    submit=st.button("update")
    

    if(submit==True):
        warehouse_id=int(warehouse_id)
        Pincode=int(Pincode)
        cur.execute("select  warehouse_ID from warehouses;")
        result=cur.fetchall()
        l=[]
        for i in result:
            l.append(i[0])
        print(l)
        
        if (int(warehouse_id) not in l):
            st.error("Incorrect Warehouse Id")
        else:
            cur.execute("update warehouses set name=%s,contact_no=%s,area=%s,City=%s,State=%s,Country=%s,pincode=%s where warehouse_ID=%s;",(name,contact,area,city,state,country,Pincode,warehouse_id))
            db.commit()
            st.success("Record updated successfully!")

def custom_query():
    st.markdown("# Custom Query")
    query = st.text_input("Enter your custom query:")

    if st.button("Run Query"):
        if query.strip() == "":
            st.warning("Please enter a query.")
        else:
            cur.execute(query)
            results = cur.fetchall()
            if results:
                st.write("Query executed successfully.")
                st.table(results)
            else:
                st.warning("No results returned.")

def admin_page():
    selected_option = st.sidebar.radio("Select an Option:", ["View Order Statistics", "View Registered Accounts", "Inventory Details", "Modify Product Catalogue", "Update Warehouse details","Submit Custom Query","Place Shipment Order"])
    
    if selected_option == "View Registered Accounts":
        view_registered_accounts()
    elif selected_option == "View Order Statistics":
        view_order_statistics()
    elif selected_option == "Inventory Details":
        inventory_details()
    elif selected_option == "Modify Product Catalogue":
        modify_product_catalogue()
    elif selected_option == "Update Warehouse details":
        update_warehouse_details()
    elif selected_option == "Submit Custom Query":
        custom_query()
    elif selected_option == "Place Shipment Order":
        place_shipment_orders()
    else:
        # If no option is selected, you can display a default message or leave it blank
        pass


# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# Verify the user's role
if st.session_state.role not in ["Admin"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("Manage Croma Database")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
admin_page()
