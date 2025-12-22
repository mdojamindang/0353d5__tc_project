import duckdb

import pandas as pd
import numpy as np

import streamlit as st

conn = duckdb.connect("database/data.duckdb")

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

# col1, col2, col3 = st.columns(3)
# col1.metric("Restaurant Name", df_1["restaurant_names"])
# col2.metric("Total Customer Visits", df_1["count_customer"])
# col3.metric("Total Customers", df_1["count_unique_customer"])
st.subheader("Restaurant Traffic")
st.table(df_1)

st.subheader("Restaurant Income")
st.table(df_2)

st.subheader("Restaurant Popular Items")
st.table(df_3)

st.subheader("Restaurant Profitable Items")
st.table(df_4)

st.subheader("Restaurant Loyal Customer ")
st.table(df_5)

st.subheader("Best Restaurateur")
st.table(df_6)

