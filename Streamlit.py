import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title("My Mom's New healthy dinner.")
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

streamlit.dataframe(my_fruit_list)


fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("The fruit load list contains:")
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
  fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("PLease select a fruit to get inof")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()




#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
##my_cur.execute("use warehouse pc_rivery_wh") 
#my_cur.execute("select * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contain:")
#streamlit.dataframe(my_data_rows)

#add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
#streamlit.write('Thanks for adding ', add_my_fruit)

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as mycur:
       mycur.execute("use warehouse pc_rivery_wh") 
       mycur.execute("select * from fruit_load_list")
       return mycur.fetchall()

if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#my_cur.execute("insert into fruit_load_list values ('from streamlit')")

streamlit.header("View Our Fruit List- Add your Favourites!")

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("use warehouse pc_rivery_wh") 
    my_cur.execute("insert into fruit_load_list values ('"+fruit_name+"')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add A fruit'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowflake(add_my_fruit)
   my_cnx.close()
   streamlit.text(back_from_function)
streamlit.stop()
