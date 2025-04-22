import streamlit as st

# Page config
st.set_page_config(page_title="Recipe Finder", layout="centered")

# Styling for centered layout
st.markdown("""
    <style>
    .centered {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 20vh;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    st.title("🍽️ Find a Recipe")

    # Horizontal dropdown layout
    col1, col2, col3 = st.columns(3)

    with col1:
        diet = st.selectbox(
            "Diet",
            ["Any", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Paleo"]
        )

    with col2:
        ingredient = st.selectbox(
            "Ingredient",
            ["Any", "Chicken", "Beef", "Tofu", "Mushrooms", "Lentils", "Fish"]
        )

    with col3:
        time = st.selectbox(
            "Time",
            ["Any", "Under 15 minutes", "15–30 minutes", "30+ minutes"]
        )

    # Search button
    if st.button("Search Recipes"):
        st.success(f"Showing {diet.lower()} recipes with {ingredient.lower()} that take {time.lower()}.")

    st.markdown('</div>', unsafe_allow_html=True)
