import streamlit as st
import httpx
import lxml.html as lh
import re

# Function to scrape and extract English text without punctuation and special symbols
async def scrape_article_async(url, session):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()

            tree = lh.fromstring(text)
            paragraphs = tree.xpath("//p")

            article_text = ""
            for p in paragraphs:
                article_text += p.text_content() + " "

            article_text = re.sub(r'[^a-zA-Z\s]', '', article_text)
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

        async with httpx.AsyncClient() as session:
            tasks = [scrape_article_async(url.strip(), session) for url in urls]
            article_words = await asyncio.gather(*tasks)

            for words in article_words:
                unique_words_set.update(words)

        combined_content = ' '.join(unique_words_set)  # Combine unique words from all articles
        st.text_area("Combined Unique English Text", combined_content)
    else:
        st.warning("Please enter one or more valid URLs.")

st.text("Note: This is an asynchronous web scraping example for educational purposes.")
