import streamlit as st
import requests
from lxml import html
import re

# Function to scrape and extract English text without punctuation and special symbols
def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.text)
        paragraphs = tree.xpath("//p")
        
        article_text = ""
        for p in paragraphs:
            article_text += p.text_content() + " "

        # Remove punctuation, special symbols, and retain only English text
        article_text = re.sub(r'[^a-zA-Z\s]', '', article_text)
        
        # Split the text into words and remove duplicates
        words = article_text.split()
        unique_words = list(set(words))
        
        return unique_words
    except Exception as e:
        return []

# Streamlit app
st.title("News Article Scraper")

st.write("Enter URLs of news articles to scrape their content (one URL per line):")
input_urls = st.text_area("URLs (One URL per line):", "")

if st.button("Scrape Articles"):
    urls = input_urls.strip().split("\n")
    if urls:
        unique_words_set = set()  # To store unique words across all articles
        for url in urls:
            article_words = scrape_article(url.strip())
            unique_words_set.update(article_words)
        
        combined_content = ' '.join(unique_words_set)  # Combine unique words from all articles
        st.text_area("Combined Unique English Text", combined_content)
    else:
        st.warning("Please enter one or more valid URLs.") 
