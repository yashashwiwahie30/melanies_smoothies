# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("My Parenets new healthy diner.")
st.write("Choose the fruits you want in your custom Smoothie! :")

import streamlit as st

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")

option = st.selectbox(
    "What is your favorite fruit",
    ("Banana", "Strawberries", "Peaches"),
)

st.write("Your favorite fruit is:", option)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write (ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""

    # st.write(my_insert_stmt)
   
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
