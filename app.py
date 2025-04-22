import streamlit as st

# Page config
st.set_page_config(page_title="Search Page", layout="centered")

# Centered layout using containers and some custom styling
st.markdown("""
    <style>
    .centered {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 70vh;
    }
    .search-bar input {
        width: 400px !important;
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    
    st.title("🔍 Search Something")

    # Search input
    search_query = st.text_input(" ", placeholder="Type your query here...", label_visibility="collapsed", key="search", help="Enter a search term")
    
    if search_query:
        st.write(f"Searching for: **{search_query}**")

    st.markdown('</div>', unsafe_allow_html=True)
