import streamlit
import snowflake.connector
import pandas as pd  # Using "as pd" for pandas alias

# Set the title
streamlit.title("Zena's Amazing Athleisure Catalog")

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Run a Snowflake query and fetch data
my_cur.execute("SELECT color_or_style FROM catalog_for_website")
my_catalog = my_cur.fetchall()

# Create a DataFrame
df = pd.DataFrame(my_catalog, columns=["Color or Style"])

# Get a list of colors/styles
color_list = df["Color or Style"].tolist()

# Selectbox for color/style
option = streamlit.selectbox("Pick a sweatsuit color or style:", color_list)

# Fetch additional product information
my_cur.execute(
    "SELECT direct_url, price, size_list, upsell_product_desc FROM catalog_for_website WHERE color_or_style = %s;",
    (option,),
)
df2 = my_cur.fetchone()

# Display product information
if df2:
    product_caption = f"Our warm, comfortable, {option} sweatsuit!"
    streamlit.image(df2[0], width=400, caption=product_caption)
    streamlit.write("Price:", df2[1])
    streamlit.write("Sizes Available:", df2[2])
    streamlit.write(df2[3])
else:
    streamlit.write("No information found for the selected color/style.")

# Close the cursor and connection
my_cur.close()
my_cnx.close()


