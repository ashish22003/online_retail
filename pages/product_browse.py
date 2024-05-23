from utility import st, display_header as dh, launch_connection
from streamlit.components.v1 import html

db = launch_connection()
mc = db.cursor()

# Function to fetch product records from MySQL
def fetch_products(search_query):
    if mc is None:
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

    mc.execute(query)
    products = mc.fetchall()

    return products

def star_rating(rating,label="Rating"):
  """
  Creates a star rating component using a slider.
  """
  num_stars = 5
#   rate = st.slider(label, 0, num_stars, 1, key="Rating")
  full_stars = int(rating)
  partial_star = int(rating * 10) % 10

  # Create star display string
  stars = "★" * full_stars
  stars += "☆" if partial_star > 0 else ""
  stars += "☆" * (num_stars - full_stars - (partial_star > 0))

  st.write(f"Rating : {rating:.1f} {stars}")



# Display products in an organized manner
def display_products(products):
    st.write("# Products")
    if not products:
        st.write("No products found.")
    else:
        cols = st.columns(min(len(products), 3))  # Adjust columns based on screen size
        for i, product in enumerate(products):
            with cols[i%3]:
                st.write(f"**{product[1]}**")  # Assuming 'name' is a product property
                # st.image(product.image, width=200)  # Assuming 'image_url' is a product property
                st.write(f"Product Price: {product[3]}")
                query = f"SELECT COALESCE(AVG(R.Rating), 0) AS Average_Rating FROM product_reviews R GROUP BY R.Product_ID HAVING R.Product_ID = {product[0]}"
                mc.execute(query)
                rating = mc.fetchall()
                if rating:
                    rating = rating[0][0]
                    star_rating(rating,"Rating")
                else: st.write(f"Rating: Not Rated Yet")
                if(st.button("View Product", key = "view"+str(product[1]))):
                    query1 = f"SELECT C.Customer_ID, R.Product_ID, C.Name, R.Review, R.Rating, R.Review_Date from product_reviews R, Customers C WHERE C.Customer_ID = R.Customer_ID AND R.Product_ID = {product[0]}"
                    mc.execute(query1)
                    reviews = mc.fetchall()
                    st.session_state.product = product
                    st.session_state.reviews = reviews
                    st.session_state.rating = rating
                    st.switch_page("pages/product_detail.py")
                st.write("-"*6)

# Main function
def main():
    # dh()
    st.markdown("<h3 style='color: green;'>Croma</h3>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="position:fixed;bottom:10px;text-align:center;width:100%;">
        <p style="color:#666666;">© 2024 Croma. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Search bar and button
    search_query = st.text_input("Search", "")
    items_per_page = 10
    if st.button("Search"):
        # Perform search logic here
        products = fetch_products(search_query)
        display_products(products)
        # total_products = len(products)
        # index = 0
        # high = 0
        # for i in total_products/10 + total_products%10 != 0:
        #     if(index + 10 > total_products): high = total_products-index
        #     else: high = index+10
        #     display_products(products, index, high, i+1, items_per_page)
        #     index+=10


if __name__ == "__main__":
    main()
