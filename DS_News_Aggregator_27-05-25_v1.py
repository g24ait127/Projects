# DO_NOT_MAKE_ANY_CHANGES_TO_THE_CODE: Critical for code integrity.
# Python code to retieve news from different APIs.
# Author - Deepak Kumar Sahoo
# Updated on 27-May-25 - Multi-select check boxes for both the prompts (Topic and Country)
# Updated on 05-Jun-25 - Streamlit-based deployment of multi-source news

import streamlit as st
import requests

# APIs
def fetch_news_from_newsapi(topic, country='in'):
    api_key = '8000b3b3a42e4da49d018b2f53d39169'
    url = f'https://newsapi.org/v2/top-headlines?q={topic}&country={country}&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error from NewsAPI: {response.status_code} - {response.reason}"
    return response.json().get('articles', [])

def fetch_news_from_mediastack(topic, country='in'):
    api_key = 'f95c057b7f7ea6fc6bee36c209e62912'
    url = f'http://api.mediastack.com/v1/news?access_key={api_key}&keywords={topic}&countries={country}&sort=published_desc'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error from Mediastack: {response.status_code} - {response.reason}"
    return response.json().get('data', [])

def fetch_news_from_newsdata(topic, country='in'):
    api_key = 'pub_88128f768af05fbd085d0d2937ae485b47e61'
    url = f'https://newsdata.io/api/1/news?apikey={api_key}&q={topic}&country={country}'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error from Newsdata.io: {response.status_code} - {response.reason}"
    return response.json().get('results', [])

def get_news_summary(topics, countries):
    all_summaries = []
    for topic in topics:
        for country in countries:
            sources = [
                fetch_news_from_newsapi(topic, country),
                fetch_news_from_mediastack(topic, country),
                fetch_news_from_newsdata(topic, country)
            ]
            for source_articles in sources:
                if isinstance(source_articles, str):
                    st.error(source_articles)
                    continue
                for article in source_articles[:5]:
                    title = article.get('title', 'No Title')
                    description = article.get('description', 'No Description')
                    url = article.get('url') or article.get('link', '#')
                    all_summaries.append((topic, title, description, url))
    return all_summaries

# UI
st.title("🌐 Multi-Source News Aggregator")

predefined_topics = [
    "Security", "Politics", "Sports", "Weather", "Technology", "Health", "Entertainment",
    "Business", "Science", "Education", "Travel", "Food", "Fashion", "Finance",
    "Environment", "Culture", "Crime", "World", "Local", "Opinion"
]

country_codes = {
    "India": "in", "United States": "us", "United Kingdom": "gb", "Canada": "ca",
    "Australia": "au", "Germany": "de", "France": "fr", "Japan": "jp", "China": "cn",
    "Brazil": "br", "Italy": "it", "Spain": "es", "Russia": "ru", "South Korea": "kr",
    "Mexico": "mx", "South Africa": "za", "Netherlands": "nl", "Sweden": "se", "New Zealand": "nz"
}

topics_selected = st.multiselect("Select News Topics", predefined_topics)
countries_selected = st.multiselect("Select Countries", list(country_codes.keys()))

if st.button("Fetch News"):
    if not topics_selected or not countries_selected:
        st.warning("Please select at least one topic and one country.")
    else:
        country_code_list = [country_codes[c] for c in countries_selected]
        summaries = get_news_summary(topics_selected, country_code_list)

        if summaries:
            for topic in topics_selected:
                st.subheader(f"{topic} News")
                for (t, title, desc, url) in [s for s in summaries if s[0] == topic]:
                    st.markdown(f"**[{title}]({url})**")
                    st.markdown(f"_{desc}_\n")
        else:
            st.info("No news articles found for the selected filters.")
