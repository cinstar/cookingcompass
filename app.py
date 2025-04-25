import streamlit as st
import pandas as pd
import ast

# Load the DataFrame
recipe_data = pd.read_csv("recipe_data.csv")
recipe_data["rating"] = pd.to_numeric(recipe_data["rating"], errors="coerce")

#-------------------------------------------------------
#THE FOLLOWING CODE CATEGORIZES RECIPE RATINGS INTO THREE RANGES
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

#-------------------------------------------------------

#THE FOLLOWING CODE FORMATS THE DIETARY LABEL
# Normalize Dietary Label values
recipe_data["Dietary Label"] = recipe_data["Dietary Label"].str.strip().str.capitalize()
recipe_data["Dietary Label"] = recipe_data["Dietary Label"].fillna("None")

# Convert ingredient_list from string to list
recipe_data['ingredient_list'] = recipe_data['ingredient_list'].apply(ast.literal_eval)

# Streamlit app config
st.set_page_config(page_title="Recipe Finder", layout="centered")
st.title("🍳🧭 Cooking Compass")
st.subheader("🍽️ Find a Recipe")

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


# defining dropdown ranges for total_times
time_ranges = {
    "Any": (0, float("inf")),
    "0–29 mins": (0, 30),
    "30–59 mins": (30, 60),
    "1-2 hrs": (60, 120),
    "2-3 hrs": (120, 180),
    "3+ hrs": (180, float("inf"))
}




st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)
search_term = st.text_input("Search by Recipe Name")
st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)

# UI layout
col1, col2, col3 = st.columns(3)

with col1:
    selected_ingredients = st.multiselect("🧅 Ingredients", all_ingredients)
    # st.markdown("<br>", unsafe_allow_html=True)

    # Spacer to align vertically with Total Time
    st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)
    selected_prep = st.selectbox("⏳ Prep Time", ["Any"] + prep_times)

with col2:
    selected_diet = st.selectbox("🥗 Dietary Label", ["Any"] + dietary_labels)
    # st.markdown("<br>", unsafe_allow_html=True)

    # Spacer to align vertically with Total Time
    st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)
    selected_cook = st.selectbox("🔥 Cook Time", ["Any"] + cook_times)

with col3:
    min_rating, max_rating = st.slider(
        "⭐ Rating",
        min_value=0.0,
        max_value=5.0,
        value=(0.0, 5.0),
        step=0.1,
        format="%.1f"
    )
    # st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    selected_total_range_label = st.selectbox("⏱️ Total Time", list(time_ranges.keys()))

st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)

# Filter button
if st.button("🔍 Search Recipes"):
    filtered = recipe_data.copy()

    if search_term:
        filtered = filtered[filtered["recipe_name"].str.contains(search_term, case=False, na=False)]

    if selected_ingredients:
        filtered = filtered[filtered['ingredient_list'].apply(lambda x: all(i in x for i in selected_ingredients))]
    if selected_cook != "Any":
        filtered = filtered[filtered["cook_time"] == selected_cook]
    if selected_prep != "Any":
        filtered = filtered[filtered["prep_time"] == selected_prep]

    # changing total_time dropdown to cleaned_total_time slider
    # if selected_total != "Any":
    #     filtered = filtered[filtered["total_time"] == selected_total]

    # filtered = filtered[
    #     (filtered["cleaned_total_time"] >= selected_total_range[0]) &
    #     (filtered["cleaned_total_time"] <= selected_total_range[1])
    #     ]
    filtered['cleaned_total_time'] = pd.to_numeric(
    filtered['cleaned_total_time'], errors='coerce'
    )
    if selected_total_range_label != "Any":
        min_time, max_time = time_ranges[selected_total_range_label]
        filtered = filtered[
            (filtered['cleaned_total_time'] >= min_time) &
            (filtered['cleaned_total_time'] < max_time)
        ]



    if selected_diet != "Any":
        filtered = filtered[filtered["Dietary Label"] == selected_diet]
    
    filtered = filtered[
    (filtered["rating"] >= min_rating) & (filtered["rating"] <= max_rating)
    ]

    # if selected_rating != "Any":
    #     filtered = filtered[filtered["rating_category"] == selected_rating]


    filtered = filtered.sort_values(by="rating", ascending=False)

    if not filtered.empty:
        st.subheader(f"🍜 Found {len(filtered)} Recipe(s):")

        for _, row in filtered.iterrows():
            st.markdown("---")

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(row['img_src'], width=200)

            with col2:
                # Recipe name as clickable link
                st.markdown(f"### [{row['recipe_name']}]({row['url']})")

                # Time info
                time_parts = []
                if row.get("prep_time") != "Missing":
                    time_parts.append(f"⏳ **Prep:** {row['prep_time']}")
                if row.get("cook_time") != "Missing":
                    time_parts.append(f"🔥 **Cook:** {row['cook_time']}")
                if row.get("total_time") != "Missing":
                    time_parts.append(f"⏱️ **Total:** {row['total_time']}")
                st.markdown(" &nbsp; | &nbsp; ".join(time_parts))

                # Dietary label and rating
                if row.get("Dietary Label"):
                    st.markdown(f"🥗 **Diet:** {row['Dietary Label'].capitalize()}")
                if row.get("rating"):
                    st.markdown(f"⭐ **Rating:** {row['rating']}/5")

                # Expandable ingredients
                st.markdown(f"""
                <details>
                    <summary style='font-size:15px;'>🧾 View Ingredients</summary>
                    <p>{', '.join(row['ingredient_list'])}</p>
                </details>
                """, unsafe_allow_html=True)


