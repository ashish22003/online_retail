from utility import st, launch_connection,pd
import time

mc = launch_connection()
cur = mc.cursor()
# def set_item_to_cart( item_id ):
#     st.session_state.add_to_cart = item_id
# def set_item_to_wishlist( item_id ):
#     st.session_state.add_to_wishlist = item_id
def view_details( item_id ):
    st.session_state.product_to_be_viewed = item_id
print(st.session_state)
# if ( "add_to_cart" not in st.session_state ):
#     st.session_state.add_to_cart = None
if ( "product_to_be_viewed" not in st.session_state ):
    st.session_state.product_to_be_viewed = None

if "returning" not in st.session_state:
    st.session_state.returning = False


# Function to fetch product records from MySQL
def fetch_products(search_query):
    if cur is None:
        print("Database connection issue")
        return []

    query = f"""
    with Stock AS (
        SELECT I.Product_ID AS PID, SUM(I.Quantity) AS Quantity
        FROM Inventory I
        GROUP BY I.Product_ID
    )
    SELECT P.Product_ID, P.Name, P.Description, P.Price,
    P.Category1, P.Category2, P.Category3,
    P.Brand_Name, S.Quantity
    FROM products P, Stock S
    WHERE S.PID = P.Product_ID AND P.Name LIKE CONCAT('%','{search_query}','%')
    """

    cur.execute(query)
    products = cur.fetchall()

    return products

def star_rating(rating):
  """
  Creates a star rating component using a slider.
  """
  num_stars = 5
  full_stars = int(rating)
  partial_star = int(rating * 10) % 10

  # Create star display string
  stars = "★" * full_stars
  stars += "☆" if partial_star > 0 else ""
  stars += "☆" * (num_stars - full_stars - (partial_star > 0))

  st.write(f"Rating : {rating:.1f} {stars}")

    
if (st.session_state.product_to_be_viewed is not None) and (st.session_state.returning != True):
    st.switch_page('pages/product_detail.py')



def display_products(products):
    st.write("# Products")

    if not products:
        st.write("No products found.")
    else:
        for product in products:
            st.write(f"**{product[1]}**")
            st.write(f"Product Price: {product[3]}")

            query = "SELECT COALESCE(AVG(R.Rating), 0) AS Average_Rating FROM product_reviews R WHERE R.Product_ID = %s"
            cur.execute(query, (product[0],))
            rating = cur.fetchone()

            if rating:
                rating = rating[0]
                star_rating(rating)
            else:
                st.write("Rating: Not Rated Yet")
            st.session_state.returning = False
            st.button(f"View Details of {product[1]}", on_click = view_details, args = [product[0]] )

            st.write("-" * 50)
# Function to display Product Catalogue
def view_products():
    st.subheader("Product Catalogue")
    # Search bar and button
    search_query = st.text_input("Search", "")
    f1 = st.button("Search", key = "search_button")
    if f1:
        # Perform search logic here
        products = fetch_products(search_query)
        display_products( products)
    
# Function to fetch cart items for a given user ID
def fetch_cart_items(customer_id):
    cur.execute("SELECT c.Product_ID, p.Name, c.Quantity, p.Price FROM cart c INNER JOIN products p ON c.Product_ID = p.Product_ID WHERE c.Customer_ID = %s", (customer_id,))
    cart_items = cur.fetchall()
    return cart_items

# Function to update quantity for a given item in the cart
def update_quantity(customer_id, product_id, new_quantity):
    # Update quantity in the cart table
    cur.execute("UPDATE cart SET Quantity = %s WHERE Customer_ID = %s AND Product_ID = %s", (new_quantity, customer_id, product_id))
    mc.commit()

    # Retrieve the price of the product from the Products table
    cur.execute("SELECT Price FROM Products WHERE Product_ID = %s", (product_id,))
    product_price = cur.fetchone()[0]  # Assuming there's only one price per product

    # Calculate the new total amount
    total_amount = new_quantity * product_price

    # Update the total amount in the cart table
    cur.execute("UPDATE cart SET Total_Price = %s WHERE Customer_ID = %s AND Product_ID = %s", (total_amount, customer_id, product_id))
    mc.commit()

# Function to remove an item from the cart
def remove_item(customer_id, product_id):
    cur.execute("DELETE FROM cart WHERE Customer_ID = %s AND Product_ID = %s", (customer_id, product_id))
    mc.commit()

# Function to display Cart Details
def view_cart(record):
    customer_id = record[0]
    cart_items = fetch_cart_items(customer_id)
    
    if cart_items:
        st.write("### Cart Items")
        cart_data = []
        for item in cart_items:
            product_id, product_name, quantity, price = item
            total_price = quantity * price
            cart_data.append((product_name, quantity, price, total_price))

        cart_df = pd.DataFrame(cart_data, columns=["Product Name", "Quantity", "Price", "Total Price"])
        st.table(cart_df)
        
        st.write("### Update Cart")
        for item in cart_items:
            product_id, product_name, quantity, price = item
            radio_choice = st.radio(f"What would you like to do with {product_name}?", ('Remove', 'Modify Quantity'))
            if radio_choice == 'Remove':
                if st.button(f"Remove {product_name}"):
                    remove_item(customer_id, product_id)
                    st.success(f"{product_name} removed successfully from the cart.")
            elif radio_choice == 'Modify Quantity':
                new_quantity = st.number_input(f"New Quantity for {product_name}:", min_value=0, value=quantity, step=1)
                if new_quantity != quantity:
                    update_quantity(customer_id, product_id, new_quantity)
                    st.success(f"Quantity for {product_name} modified successfully.")
        
    st.write("### Checkout")
    # Check if the cart is empty
    if not cart_items:
        st.write("Your cart is empty.")
    else:
        # Display the total amount to be paid
        total_amount = sum([item[2] * item[3] for item in cart_items])
        st.write(f"Total Amount: Rs.{total_amount:.2f}")
        st.write("Would you like to proceed to checkout?")
        if st.button("Proceed to Checkout"):
            st.write("Redirecting to checkout page...")
            st.session_state.checkout = True
            st.switch_page("pages/order_checkout.py")

# Function to display Wishlist
def view_wishlist(record):
    st.markdown("# Wishlist")
    cur.execute("SELECT wishlist.Product_ID, products.Name, wishlist.Added_Date FROM wishlist INNER JOIN products ON wishlist.Product_ID = products.Product_ID WHERE wishlist.customer_id = %s", (int(record[0]),))
    data = cur.fetchall()

    if data:
        # Display the entire wishlist table in a tabular format
        st.write("Here is your wishlist:")
        wishlist_table = "<table><tr><th>Product ID</th><th>Product Name</th><th>Added Date</th></tr>"
        for item in data:
            wishlist_table += f"<tr><td>{item[0]}</td><td>{item[1]}</td><td>{item[2]}</td></tr>"
        wishlist_table += "</table>"
        st.write(wishlist_table, unsafe_allow_html=True)

        # Radio menu for selecting items to delete
        st.write("Select the item you want to remove:")
        selected_product_id = st.radio("", options=[item[0] for item in data])

        # Button to remove the selected item
        if st.button("Remove Selected Item"):
            cur.execute("DELETE FROM wishlist WHERE customer_id=%s AND product_id=%s;", (int(record[0]), selected_product_id))
            mc.commit()
            st.success("Item removed from wishlist successfully! ... Revisit the page to refresh list")
    else:
        st.write("Your wishlist is empty.")

# Function to display Customer Profile
def customer_profile(record, addresses):
    print(st.session_state)
    st.title("Customer Account Details")
    # Extract customer details
    first_name = record[1]
    middle_name = record[2] if record[2] else ""
    last_name = record[3]
    full_name = f"{first_name} {middle_name} {last_name}"
    email = record[4]
    phone = record[6]


    # Customer details section with columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Name:")
        st.write(full_name)
    with col2:
        st.subheader("Email:")
        st.write(email)

    # Phone number
    st.subheader("Phone:")
    st.write(phone)

    #Addresses
    st.subheader("Addresses:")
    for address in addresses:
        st.write(f"{address[1]}:  {address[2]}, {address[3]}, {address[4]}, {address[5]}, {address[6]} - {address[7]}")

#Function to edit customer profile
def edit_account(record, addresses):
    st.title("Edit Account Details")
    
    # Display options for editing
    options = ["Name", "Middle Name", "Last Name", "Email", "Address", "Phone"]
    selected_option = st.selectbox("Select option to edit:", options)

    # Input fields for the selected option
    if selected_option in ["Name", "Middle Name", "Last Name"]:
        if selected_option == "Name":
            label = "First Name"
            index = 1
        elif selected_option == "Middle Name":
            label = "Middle Name"
            index = 2
        elif selected_option == "Last Name":
            label = "Last Name"
            index = 3
        new_value = st.text_input(f"New {label}", record[index])
        column_name = f"First_Name" if selected_option == "Name" else selected_option.replace(" ", "_").upper()  # Column name in the database
    elif selected_option == "Email":
        new_value = st.text_input("New Email", record[4])  # Email_ID
        column_name = "Email_ID"
    elif selected_option == "Address":
        action = st.radio("Choose Action:", ["Modify Current Address", "Add New Address"])
        if action == "Modify Current Address":
            # Display current address to modify
            address_types = [addr[0] for addr in addresses]
            selected_address_type = st.selectbox("Select Address Type:", address_types)
            current_address = next((addr for addr in addresses if addr[0] == selected_address_type), None)
            if current_address:
                new_address = {
                    "House_No": st.text_input("House Number", current_address[2]),
                    "Street": st.text_input("Street", current_address[3]),
                    "Area": st.text_input("Area", current_address[4]),
                    "City": st.text_input("City", current_address[5]),
                    "State": st.text_input("State", current_address[6]),
                    "Pincode": st.text_input("Pincode", current_address[7]),
                    "Contact_Number": st.text_input("Contact Number", current_address[8])
                }
                column_name = "addresses"
            else:
                st.error("No addresses found to modify.")
                return
        else:  # Add New Address
            new_address_type = st.selectbox("Address Type", ['Home', 'Work', 'Other'])
            new_address = {
                "Address_Type": new_address_type,
                "House_No": st.text_input("House Number"),
                "Street": st.text_input("Street"),
                "Area": st.text_input("Area"),
                "City": st.text_input("City"),
                "State": st.text_input("State"),
                "Pincode": st.text_input("Pincode"),
                "Contact_Number": st.text_input("Contact Number")
            }
            # Check if an address of the same type already exists
            existing_address = next((addr for addr in addresses if addr[0] == new_address["Address_Type"]), None)
            if existing_address:
                st.error(f"An address of type '{new_address['Address_Type']}' already exists. Please edit the existing address.")
                return
            else:
                column_name = "addresses"
    elif selected_option == "Phone":
        new_value = st.text_input("New Phone", record[6])  # Contact_Number
        column_name = "Contact_Number"
    
    # Update button
    if st.button("Update"):
        # Check constraints before updating
        if selected_option == "Email":
            cur.execute("SELECT * FROM customer WHERE Email_ID = %s", (new_value,))
            existing_record = cur.fetchone()
            if existing_record and existing_record[0] != record[0]:
                st.error("Email already exists. Please choose a different email.")
                return
        elif selected_option == "Phone":
            cur.execute("SELECT * FROM customer WHERE Contact_Number = %s", (new_value,))
            existing_record = cur.fetchone()
            if existing_record and existing_record[0] != record[0]:
                st.error("Phone number already exists. Please choose a different number.")
                return

        # Update record in the database
        try:
            if column_name == "addresses":
                # Insert the new address into the database
                cur.execute("INSERT INTO addresses (Customer_ID, Address_Type, House_No, Street, Area, City, State, Pincode, Contact_Number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (record[0], new_address["Address_Type"], new_address["House_No"], new_address["Street"], new_address["Area"], new_address["City"], new_address["State"], new_address["Pincode"], new_address["Contact_Number"]))
            elif column_name != "Address":
                # Update customer details in the database
                cur.execute(f"UPDATE customer SET {column_name} = %s WHERE Customer_ID = %s", (new_value, record[0]))
            mc.commit()
            st.success("Account updated successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            mc.rollback()

def order_history(record):
    st.title("Recently Purchased Products")
    cur.execute(f"Select * from Orders O where O.Customer_ID = {record[0]}")
    res = cur.fetchall()
    if not res:
        st.write("You haven't purchased anything yet.")
    else:
        temp = []
        c1 = 1
        for item in res:
            cur.execute(f"Select * from OrderItems OT where OT.Order_ID = {item[0]};")
            order_details = cur.fetchall()
            for product in order_details:
                cur.execute(f"Select P.Name from Products P where P.Product_ID = {product[1]}")
                temp2 = []
                temp2.append(cur.fetchall()[0][0])
                temp2.append(product[2])
                temp2.append(item[2])
                temp.append(temp2)
                c1+=1
        
        cols = st.columns(min(len(temp), 3))
        i = 0
        for item in temp:
            with cols[i%3]:
                st.write(f"**{item[0]}**")
                st.write(f"Quantity: {item[1]}")
                st.write(f"Purchase Date: {item[2]}")
                st.write("-"*6)
            i+=1

# Function for Customer Homepage
def main():

    #get record from sql
    st.sidebar.page_link("Home.py", label="Logout",icon="🏠")
    record = st.session_state.record_details
    query = "SELECT * FROM addresses WHERE Customer_ID = %s"
    cur.execute(query, (record[0],))
    addresses = cur.fetchall()
    first_name = record[1]
    middle_name = record[2] if record[2] else ""
    last_name = record[3]
    full_name = f"{first_name} {middle_name} {last_name}"
    st.subheader(f"Welcome back, {full_name}!")
    menu = [
        "View Products",
        "View Cart",
        "My Wishlist",
        "Customer Profile",
        "Edit Profile",
        "Order History"
    ]
    selected_option = st.sidebar.radio("Select an Option :dart:", menu)
    if selected_option == "View Products":
        view_products()
    elif selected_option == "View Cart":
        view_cart(record)
    elif selected_option == "My Wishlist":
        view_wishlist(record)
    elif selected_option == "Customer Profile":
        customer_profile(record,addresses)
    elif selected_option == "Edit Profile":
        edit_account(record,addresses)
    elif selected_option == "Order History":
        order_history(record)
    

if __name__ == "__main__":
   main()