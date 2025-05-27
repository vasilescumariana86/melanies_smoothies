# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your smoothie
  """
)
name_on_order = st.text_input("Name on smoothie: ")
st.write("Name is ",name_on_order)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)

options = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections= 5
    
)
if options:
    # st.write(options)
    st.text(options)
    ingredients_string=''
    for each_fruit in options:
        ingredients_string+=each_fruit +' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on,'.')
        st.subheader(each_fruit + ' Nutrition facts')
      
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ each_fruit)
        sf_df =  st.dataframe( data=smoothiefroot_response.json(), use_container_width=True )

    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


