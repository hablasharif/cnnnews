import streamlit as st
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import string

# Function to scrape and extract English text without punctuation and special symbols
def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the relevant HTML element containing the article content
        article_element = soup.find('div', {'class': 'article-content'})  # Adjust as needed

        if article_element:
            article_text = article_element.get_text()

            # Remove punctuation, special symbols, and retain only English text
            translator = str.maketrans('', '', string.punctuation)
            article_text = article_text.translate(translator)

            # Split the text into words and remove duplicates
            words = article_text.split()
            unique_words = list(set(words))

            return unique_words
        else:
            return []
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

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(scrape_article, urls)

        for article_words in results:
            unique_words_set.update(article_words)

        combined_content = ' '.join(unique_words_set)  # Combine unique words from all articles
        st.text_area("Combined Unique English Text", combined_content)
    else:
        st.warning("Please enter one or more valid URLs.")
