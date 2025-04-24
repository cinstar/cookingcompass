import streamlit as st
import pandas as pd
import ast

# Load the DataFrame
recipe_data = pd.read_csv("recipe_data.csv")

# Function to categorize ratings
def categorize_rating(r):
    try:
        r = float(r)
        if r >= 4.0:
            return "4.0 and above"
        elif r >= 3.0:
            return "3.0–3.9"
        else:
            return "Below 3.0"
    except:
        return "Missing"

# Apply categorization
recipe_data["rating_category"] = recipe_data["rating"].apply(categorize_rating)

# Convert ingredient_list from string to list
recipe_data['ingredient_list'] = recipe_data['ingredient_list'].apply(ast.literal_eval)

# Streamlit app config
st.set_page_config(page_title="Recipe Finder", layout="centered")
st.title("🍽️ Find a Recipe")

# Replace NaN with readable string for dropdowns
recipe_data.fillna("Missing", inplace=True)

# Get unique values for dropdowns
all_ingredients = sorted(
    set(ingredient for sublist in recipe_data['ingredient_list'] for ingredient in sublist)
)
cook_times = sorted(recipe_data["cook_time"].unique())
total_times = sorted(recipe_data["total_time"].unique())
dietary_labels = sorted(recipe_data["Dietary Label"].dropna().unique())
prep_times = sorted(recipe_data["prep_time"].unique())
rating_categories = ["Any", "4.0 and above", "3.0–3.9", "Below 3.0"]






# UI layout
col1, col2, col3 = st.columns(3)

with col1:
    selected_ingredients = st.multiselect("Ingredients", all_ingredients)
    selected_prep = st.selectbox("Prep Time", ["Any"] + prep_times)

with col2:
    selected_diet = st.selectbox("Dietary Label", ["Any"] + dietary_labels)
    selected_cook = st.selectbox("Cook Time", ["Any"] + cook_times)

with col3:
    selected_rating = st.selectbox("Rating Category", rating_categories, key="rating_category")
    selected_total = st.selectbox("Total Time", ["Any"] + total_times)



# with col1:
#     selected_ingredients = st.multiselect("Ingredients", all_ingredients)

# with col2:
#     selected_cook = st.selectbox("Cook Time", ["Any"] + cook_times)
#     selected_total = st.selectbox("Total Time", ["Any"] + total_times)

# Filter button
if st.button("Search Recipes"):
    filtered = recipe_data.copy()

    if selected_ingredients:
        filtered = filtered[filtered['ingredient_list'].apply(lambda x: all(i in x for i in selected_ingredients))]
    if selected_cook != "Any":
        filtered = filtered[filtered["cook_time"] == selected_cook]
    if selected_prep != "Any":
        filtered = filtered[filtered["prep_time"] == selected_prep]
    if selected_total != "Any":
        filtered = filtered[filtered["total_time"] == selected_total]
    if selected_diet != "Any":
        filtered = filtered[filtered["Dietary Label"] == selected_diet]
    if selected_rating != "Any":
        filtered = filtered[filtered["rating_category"] == selected_rating]


    filtered = filtered.sort_values(by="rating", ascending=False)


    # st.subheader("🍏 Matching Recipes")
        

    if not filtered.empty:
        st.subheader(f"🍏 Found {len(filtered)} Recipe(s):")

        for _, row in filtered.iterrows():
            st.markdown("---")

            # Centered, smaller image
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <img src="{row['img_src']}" style='max-width: 300px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;' />
                </div>
                """,
                unsafe_allow_html=True
            )

            # Recipe name as clickable link
            st.markdown(f"### [{row['recipe_name']}]({row['url']})")

            # Time info
            time_parts = []
            if row.get("prep_time") != "Missing":
                time_parts.append(f"🕒 **Prep:** {row['prep_time']}")
            if row.get("cook_time") != "Missing":
                time_parts.append(f"🔥 **Cook:** {row['cook_time']}")
            if row.get("total_time") != "Missing":
                time_parts.append(f"⏱️ **Total:** {row['total_time']}")
            st.markdown(" &nbsp; | &nbsp; ".join(time_parts))

    else:
        st.markdown(
            "<div style='color: #ff8800; font-size: 1.2rem;'>"
            "🍽️ Nothing matched! Maybe try fewer ingredients or a different cook time?"
            "</div>",
            unsafe_allow_html=True
        )
