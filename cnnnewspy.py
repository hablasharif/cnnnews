import streamlit as st
import requests
from lxml import html

# Function to scrape and extract English text without punctuation and special symbols
def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.text)
        paragraphs = tree.xpath("//p")
        
        combined_content = ""
        for p in paragraphs:
            combined_content += html.tostring(p, method='html').decode()
        
        return combined_content
    except Exception as e:
        return ""

# Streamlit app
st.title("News Article Scraper")

st.write("Enter URLs of news articles to scrape their content (one URL per line):")
input_urls = st.text_area("URLs (One URL per line):", "")

if st.button("Scrape Articles"):
    urls = input_urls.strip().split("\n")
    if urls:
        combined_content = ""  # To store combined content from all articles
        for url in urls:
            article_content = scrape_article(url.strip())
            combined_content += article_content
        
        st.markdown(combined_content, unsafe_allow_html=True)
    else:
        st.warning("Please enter one or more valid URLs.")

st.text("Note: This is a basic web scraping example for educational purposes.")
