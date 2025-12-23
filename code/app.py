import duckdb

import pandas as pd
import numpy as np

import streamlit as st

conn = duckdb.connect("database/data.duckdb", read_only=True)

# Dataframe for restaurant traffic
df_1 = conn.sql("""
    SELECT
        restaurant_names,
        COUNT(*) AS count_customer,
        COUNT(DISTINCT first_name) AS count_unique_customer
    FROM TABLE_CHECK_DATA
    GROUP BY restaurant_names
    ORDER BY count_customer desc
""").df()

#Dataframe for Restaurant income           
df_2 = conn.sql("""
    SELECT
        restaurant_names,
        sum(food_cost) as sum_food_cost,
    FROM TABLE_CHECK_DATA
    GROUP BY restaurant_names
    ORDER BY sum_food_cost desc
""").df()

# Dataframe for modes 

df_3 = conn.sql("""
    WITH freq as (
        SELECT 
            restaurant_names,
            food_names,
            count(*) as count_
        FROM TABLE_CHECK_DATA
        GROUP BY restaurant_names,food_names 
        ),
        modes as (
        SELECT 
            a.restaurant_names,
            a.food_names,
            count_
        FROM freq a
        WHERE count_ = (
        Select max(count_) from freq b 
            where b.restaurant_names = a.restaurant_names 
            )
        ),
    final as (
    SELECT
        a.restaurant_names,
        a.food_names as mode_food_names,
        sum(a.food_cost) as sum_food_cost,
    FROM TABLE_CHECK_DATA a
    join modes b
        on a.restaurant_names = b.restaurant_names
        and a.food_names = b.food_names
    GROUP BY a.restaurant_names,a.food_names
    ORDER BY sum_food_cost desc
    )
    select * from modes
""").df()

# DataFrame for Most profitable 
df_4 = conn.sql("""
    WITH freq as (
        SELECT 
            restaurant_names,
            food_names,
            sum(food_cost) as sum_food_cost
        FROM TABLE_CHECK_DATA
        GROUP BY restaurant_names,food_names 
        ),
        modes as (
        SELECT 
            a.restaurant_names,
            a.food_names,
            sum_food_cost
        FROM freq a
        WHERE sum_food_cost = (
        Select max(sum_food_cost) from freq b 
            where b.restaurant_names = a.restaurant_names 
            )
        ),
        final as (select * from modes)
        
        select * from final
""").df()

# Favorite Customer 
df_5 = conn.sql("""
    WITH freq as (
        SELECT 
            restaurant_names,
            first_name,
            count(*) as count_
        FROM TABLE_CHECK_DATA
        GROUP BY restaurant_names,first_name 
        ),
        modes as (
        SELECT 
                a.restaurant_names,
            a.first_name,
            count_
        FROM freq a
        WHERE count_ = (
        Select max(count_) from freq b 
            where b.restaurant_names = a.restaurant_names 
            )
        ),
    final as (
    SELECT
        a.restaurant_names,
        a.first_name as mode_first_name,
        sum(a.food_cost) as sum_food_cost,
        count(a.first_name) as number_of_visit
    FROM TABLE_CHECK_DATA a
    join modes b
        on a.restaurant_names = b.restaurant_names
        and a.first_name = b.first_name
    GROUP BY a.restaurant_names,a.first_name
    ORDER BY a.first_name desc
    )
    select * from final
""").df()


#Dataframe for Restaurant income           
df_6 = conn.sql("""
    SELECT
        first_name,
        count(*) as count_,
    FROM TABLE_CHECK_DATA
    GROUP BY first_name
    ORDER BY count_ desc
    LIMIT 1
""").df()

restaurant_names = df_1['restaurant_names'].sort_values().unique().tolist()
idx = restaurant_names.index("the-restaurant-at-the-end-of-the-universe")

st.subheader("Restaurant Traffic")
st.text("Description: This table shows the number of customer visits for each shop and the number of unique customers the visited each restaurant")
df_1.columns = ["Restaurant","Customer Visits", "Customers"]
st.dataframe(df_1 , use_container_width=True , hide_index=True)


st.text("  ")
st.text("  ")
st.text("  ")

col_value = st.selectbox(
    "Select Restaurant to View",
    restaurant_names,
    index = idx
)

df_tempt = conn.execute("""
    SELECT
        restaurant_names,
        COUNT(*) AS count_customer,
        COUNT(DISTINCT first_name) AS count_unique_customer
    FROM TABLE_CHECK_DATA
    WHERE restaurant_names = ?
    GROUP BY restaurant_names
""",[col_value]).df()

st.text("Description: This component displays customer traffic for a specific restaurant")
df_tempt.columns = ["Restaurant","Customer Visits", "Customers"]
st.dataframe(df_tempt, use_container_width=True, hide_index=True)


st.divider()

st.subheader("Restaurant Income")

df_2.columns = ["Restaurant", "Income"]
st.text("Description: This component is for showing the restaurant incomes")
st.dataframe(df_2 , use_container_width=True , hide_index=True)

st.text("  ")
st.text("  ")
st.text("  ")

st.text("Description: This component is a graphical representation of each restaurant incomes")
st.bar_chart(
    df_2.set_index("Restaurant")["Income"])

st.divider()

st.subheader("Restaurant Popular Items")
st.text("Description: This component is for showing the most popular items per restaurant")
df_3.columns = ["Restaurant","Menu", "Number of Orders"]
st.dataframe(df_3 , use_container_width=True , hide_index=True)

st.text("  ")
st.text("  ")
st.text("  ")

st.subheader("Restaurant Profitable Items")
st.text("Description: This component is for showing the most profitable items per restaurant")
df_4.columns = ["Restaurant","Menu", "Total Income"]
st.dataframe(df_4 , use_container_width=True , hide_index=True)

st.divider()

st.subheader("Restaurant Loyal Customers")
st.text("Description: This component is for showing the most frequent visitor per restaurant")
df_5.columns = ["Restaurant","Customer Name", "Total Customer Spending", "Total Number of Visits"]
st.dataframe(df_5 , use_container_width=True , hide_index=True)

st.subheader("Best Restaurateur")
st.text("Description: This component is for showing the customer that frequented restaurants the most")
df_6.columns = ["Customer Name","Number of Restaurant Visits"]

st.dataframe(df_6 , use_container_width=True , hide_index=True)

conn.close()