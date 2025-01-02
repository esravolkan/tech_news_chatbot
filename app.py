import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch posts from TechCrunch
def fetch_techcrunch_news():
    base_url = "https://techcrunch.com/wp-json/wp/v2/posts"
    params = {"per_page": 5}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        posts = response.json()
        return [
            {
                "Title": post["title"]["rendered"],
                "Link": post["link"],
                "Image": post.get("jetpack_featured_media_url", "No Image Available"),
                "Date": post.get("date", "No Date Available")
            }
            for post in posts
        ]
    except Exception as e:
        return [{"Title": f"Error fetching TechCrunch news: {e}", "Link": None, "Image": None, "Date": None}]

# Function to fetch posts from Wired
def fetch_wired_news():
    rss_url = "https://www.wired.com/feed/rss"
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:5]
        return [
            {
                "Title": item.title.text,
                "Link": item.link.text,
                "Image": item.enclosure["url"] if item.find("enclosure") else "https://www.wired.com/favicon.ico",
                "Date": item.pubDate.text if item.pubDate else "No Date Available"
            }
            for item in items
        ]
    except Exception as e:
        return [{"Title": f"Error fetching Wired news: {e}", "Link": None, "Image": None, "Date": None}]

# Function to fetch posts from BBC Technology
def fetch_bbc_technology_news():
    rss_url = "http://feeds.bbci.co.uk/news/technology/rss.xml"
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")[:5]
        return [
            {
                "Title": item.title.text,
                "Link": item.link.text,
                "Image": fetch_bbc_image(item.link.text),  # Fetch image from article page
                "Date": item.pubDate.text if item.pubDate else "No Date Available"
            }
            for item in items
        ]
    except Exception as e:
        return [{"Title": f"Error fetching BBC Technology news: {e}", "Link": None, "Image": None, "Date": None}]

# Helper function to fetch image from BBC article page
def fetch_bbc_image(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        image = soup.find("meta", property="og:image")
        return image["content"] if image else "No Image Available"
    except Exception:
        return "No Image Available"

# Function to fetch posts from multiple sources based on user selection
def fetch_news(sources):
    news = []
    if "TechCrunch" in sources:
        news.extend(fetch_techcrunch_news())
    if "Wired" in sources:
        news.extend(fetch_wired_news())
    if "BBC Technology" in sources:
        news.extend(fetch_bbc_technology_news())
    return news

import streamlit as st

# CSS for header customization
st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(to right, #32CD32, #333333); /* Green to Black */
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px; /* Space between header and content */
    }
    .header-title {
        color: #FFFFFF; /* White */
        font-size: 36px;
        font-weight: bold;
        margin: 0;
    }
    .header-subtitle {
        color: #CCCCCC; /* Light Grey */
        font-size: 20px;
        margin-top: 5px;
    }
    </style>
    <div class="header-container">
        <h1 class="header-title">Code & Circuit News 📩 </h1>
        <p class="header-subtitle">Stay updated with the latest in innovation and technology 🚀</p>
    </div>
""", unsafe_allow_html=True)

# Main content

st.write("**Select your sources from the sidebar to get started. 👈**")



# Sidebar: Welcome and Multiselect for News Sources
st.sidebar.markdown("# 🤖 Welcome to the Tech News Chatbot!")
st.sidebar.image("tech.png", caption="TechCrunch News Bot", use_column_width=True)

st.sidebar.info("""
This is where you can stay updated with the latest news from **TechCrunch**, **Wired**, and **BBC Technology**. 

This application was designed to provide users with instant access to the latest and most important technology news from technology websites.

I hope this app helps you stay ahead in the fast-moving world of technology. 😊
""")

# Multiselect: Allow users to choose news sources
st.sidebar.markdown("### Select News Sources")
sources = st.sidebar.multiselect(
    "Choose your sources:",
    ["TechCrunch", "Wired", "BBC Technology"],
    default=["TechCrunch", "Wired", "BBC Technology"]
)

# Notifications section
st.sidebar.markdown("### Notifications")
email_notifications = st.sidebar.checkbox("Enable Email Notifications")
if email_notifications:
    st.sidebar.text_input("Notification Email", placeholder="Enter your email")

if st.button("📩 Fetch Top 5 News"):
    st.info("Fetching the latest news from selected sources...")
    news = fetch_news(sources)
    if news:
        st.success("Here are the top 5 news articles:")
        for i, article in enumerate(news, 1):
            st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                    <h3 style="color: #0078D7;">{i}. {article['Title']}</h3>
                    <img src="{article['Image']}" style="width: 100%; max-width: 300px; border-radius: 10px;"/>
                    <p><strong>Date Published:</strong> {article['Date']}</p>
                    <a href="{article['Link']}" target="_blank" style="color: #FF5733; text-decoration: none;">Read More</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No news found.")
