from utility import st, launch_connection,pd
from pages.customer_homepage import star_rating
import time
db = launch_connection()
cur = db.cursor()
if "returning" not in st.session_state:
    st.session_state.returning = False

def display_product_details():

    product_id = st.session_state['product_to_be_viewed']

    #fetch record with product id 
    cur.execute(f"Select * from Products P where P.Product_ID = {product_id}")
    product_record = cur.fetchall()[0]

    # Description
    st.subheader(f"Description  of { product_record[1] }:")
    st.write(product_record[7])
    st.write(f"**Price:** Rs.{product_record[6]:.2f}")

    query = "SELECT COALESCE(AVG(R.Rating), 0) AS Average_Rating FROM product_reviews R WHERE R.Product_ID = %s"
    cur.execute(query, (product_record[0],))
    product_rating = cur.fetchone()[0]

    # Rating (assuming 'Rating' is a key with average rating)
    stars = "★" * int( product_rating )  # Convert average to full stars
    stars += "☆" if ( product_rating - int( product_rating )) > 0 else ""
    st.write(f"Rating: { product_rating:.1f} {stars}")
    cur.execute("SELECT * FROM product_reviews WHERE Product_ID = %s", (product_id,))
    reviews = cur.fetchall()
    # st.subheader("Reviews")
    # with st.expander("See Reviews"):  # Use expander for optional viewing
    #     for review in reviews:
    #         st.write(f"**Reviewer:** {name}")
    #         star_rating(review[3])
    #         st.write(f"Review: {review[4]}")
    #         st.write(f"Review Date: {review[5]}")
    #         st.write("-" * 20)  # Separator between reviews
    df_reviews = pd.DataFrame(reviews, columns=["Review_ID", "Customer_ID", "Product_ID", "Rating", "Review", "Review_Date"])
    st.subheader("Reviews")
    with st.expander("See Reviews"):  # Use expander for optional viewing
        st.write(df_reviews)
    f1 = False
    customer_id = st.session_state.record_details[0]
    option = st.radio("Choose Action:", ("Add to Cart", "Add to Wishlist"))

    if option == "Add to Cart":
        # Add product ID to cart list (implementation depends on your cart logic)
        query = f"Select P.Price FROM Products P WHERE P.Product_ID = {product_record[0]}"
        cur.execute(query)
        res = cur.fetchall()[0]
        print(f"res = {res}")
        inp = st.text_input("Enter desired quantity:", "0")
        cur.execute(f"SELECT SUM(I.Quantity) FROM Inventory I WHERE I.Product_ID = {product_record[0]}")
        stock = cur.fetchone()[0]
        qty = int( inp )
        time.sleep(10)
        confirm = st.checkbox("Confirm")
        if confirm and stock >= qty:
            query = f"INSERT INTO Cart VALUES({customer_id}, {product_record[0]}, {qty}, {qty * float(res[0])}, NOW())"
            cur.execute(query)
            db.commit()
            st.success("Product added to cart!")
        elif stock < qty:
            st.error("Please input a valid quantity to be added to the cart! The current input exceeds the current stock of the product!")
    elif option == "Add to Wishlist" and not f1:
        # Check if the record already exists in the wishlist
        cur.execute("SELECT COUNT(*) FROM wishlist WHERE Customer_ID = %s AND Product_ID = %s", (customer_id, product_record[0]))
        record_count = cur.fetchone()[0]

        if record_count == 0:
            # Add product ID to wishlist list
            cur.execute("INSERT INTO wishlist (Customer_ID, Product_ID, Added_date) VALUES (%s, %s, NOW())", (customer_id, product_record[0]))
            db.commit()
            st.success("Product added to wishlist!")
            f1 = True
        else:
            st.warning("Product already exists in the wishlist!")

def main():
    st.session_state.returning = True
    st.sidebar.page_link("pages/customer_homepage.py", label="Go Back", icon="⬅️")
    display_product_details()

if __name__ == "__main__":
    main()
