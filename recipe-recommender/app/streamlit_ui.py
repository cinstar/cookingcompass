import streamlit as st
from recommend import hybrid_recommendation

st.title("🍽 Smart Recipe Recommender")
diet = st.selectbox("Choose your diet:", ["vegan", "vegetarian", "gluten-free"])
ingredients = st.text_area("Enter ingredients you want to use:")

if st.button("Recommend"):
    results = hybrid_recommendation(diet, ingredients)
    for r in results:
        st.write(r["title"])
        st.write("Ingredients:", r["ingredients"])
