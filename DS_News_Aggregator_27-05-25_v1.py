# DO_NOT_MAKE_ANY_CHANGES_TO_THE_CODE: Critical for code integrity.
# Python code to retieve news from different APIs.
# Author - Deepak Kumar Sahoo
# Last Update on 27-May-25 - Multi-select check boxes for both the prompts (Topic and Country)

import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import webbrowser

# News fetching functions
def fetch_news_from_newsapi(topic, country='in'):
    api_key = '8000b3b3a42e4da49d018b2f53d39169'
    url = f'https://newsapi.org/v2/top-headlines?q={topic}&country={country}&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error from NewsAPI: {response.status_code} - {response.reason}"
    try:
        return response.json().get('articles', [])
    except ValueError:
        return "Error: Unable to parse JSON response from NewsAPI"

def fetch_news_from_mediastack(topic, country='in'):
    api_key = 'f95c057b7f7ea6fc6bee36c209e62912'
    url = f'http://api.mediastack.com/v1/news?access_key={api_key}&keywords={topic}&countries={country}&sort=published_desc'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error from Mediastack: {response.status_code} - {response.reason}"
    try:
        return response.json().get('data', [])
    except ValueError:
        return "Error: Unable to parse JSON response from Mediastack"

def fetch_news_from_newsdata(topic, country='in'):
    api_key = 'pub_88128f768af05fbd085d0d2937ae485b47e61'
    url = f'https://newsdata.io/api/1/news?apikey={api_key}&q={topic}&country={country}'
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error from Newsdata.io: {response.status_code} - {response.reason}"
    try:
        return response.json().get('results', [])
    except ValueError:
        return "Error: Unable to parse JSON response from Newsdata.io"

def get_news_summary(topics, countries):
    all_summaries = []
    for topic in topics:
        for country in countries:
            newsapi_articles = fetch_news_from_newsapi(topic, country)
            mediastack_articles = fetch_news_from_mediastack(topic, country)
            newsdata_articles = fetch_news_from_newsdata(topic, country)

            # If any API returned an error string, show it and stop
            if isinstance(newsapi_articles, str):
                messagebox.showerror("NewsAPI Error", newsapi_articles)
                continue
            if isinstance(mediastack_articles, str):
                messagebox.showerror("Mediastack Error", mediastack_articles)
                continue
            if isinstance(newsdata_articles, str):
                messagebox.showerror("Newsdata.io Error", newsdata_articles)
                continue

            all_articles = newsapi_articles + mediastack_articles + newsdata_articles

            for article in all_articles[:10]:
                if isinstance(article, dict):
                    title = article.get('title', 'No Title')
                    description = article.get('description', 'No Description')
                    url = article.get('link') or article.get('url', '#')
                    all_summaries.append((topic, title, description, url))
    return all_summaries

# Display news in GUI

def display_news():
    selected_topics = [topic for topic, var in topic_vars.items() if var.get()]
    if not selected_topics or not selected_countries:
        messagebox.showwarning("Input Error", "Please select at least one topic and one country.")
        return
    news_summaries = get_news_summary(selected_topics, selected_countries)
    result_text.delete(1.0, tk.END)
    current_topic = None
    article_count = 1
    for topic, title, description, url in news_summaries:
        if topic != current_topic:
            result_text.insert(tk.END, f"\n{topic.capitalize()} News:\n", 'topic_heading')
            current_topic = topic
            article_count = 1
        result_text.insert(tk.END, f"{article_count}. ", 'normal')
        link = tk.Label(result_text, text=title, fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
        result_text.window_create(tk.END, window=link)
        result_text.insert(tk.END, f"\nSummary: {description}\n\n", 'summary')
        article_count += 1

# Country selector
def open_country_selector():
    def apply_selection():
        selected_countries.clear()
        for country, var in country_vars.items():
            if var.get():
                selected_countries.append(country_codes[country])
        country_label.config(text=", ".join([code.upper() for code in selected_countries]))
        selector.destroy()
    selector = tk.Toplevel(root)
    selector.title("Select Countries")
    for i, country in enumerate(country_codes):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(selector, text=country, variable=var)
        chk.grid(row=i//3, column=i%3, sticky='w', padx=5, pady=2)
        country_vars[country] = var
    ttk.Button(selector, text="Apply", command=apply_selection).grid(
        row=(len(country_codes)//3)+1, column=0, columnspan=3, pady=10)

# Topic selector -- Original
def open_topic_selector():
    def apply_selection():
        topic_label.config(text=", ".join([t for t, v in topic_vars.items() if v.get()]))
        selector.destroy()
    selector = tk.Toplevel(root)
    selector.title("Select Topics")
    for i, topic in enumerate(predefined_topics):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(selector, text=topic, variable=var)
        chk.grid(row=i//3, column=i%3, sticky='w', padx=5, pady=2)
        topic_vars[topic] = var
    ttk.Button(selector, text="Apply", command=apply_selection).grid(
        row=(len(predefined_topics)//3)+1, column=0, columnspan=3, pady=10)

# GUI setup
root = tk.Tk()
root.title("News Aggregator")

predefined_topics = [
    "Security","Politics", "Sports", "Weather", "Technology", "Health", "Entertainment",
    "Business", "Science", "Education", "Travel", "Food", "Fashion", "Finance",
    "Environment", "Culture", "Crime", "World", "Local", "Opinion"
]

country_codes = {
    "India": "in", "United States": "us", "United Kingdom": "gb", "Canada": "ca",
    "Australia": "au", "Germany": "de", "France": "fr", "Japan": "jp", "China": "cn",
    "Brazil": "br", "Italy": "it", "Spain": "es", "Russia": "ru", "South Korea": "kr",
    "Mexico": "mx", "South Africa": "za", "Netherlands": "nl", "Sweden": "se", "New Zealand": "nz"
}
selected_countries = []
country_vars = {}
topic_vars = {}


ttk.Label(root, text="Predefined Topics:").grid(column=0, row=1, padx=10, pady=10, sticky='ew')
ttk.Button(root, text="Select Topics", command=open_topic_selector).grid(column=1, row=1, padx=10, pady=10, sticky='ew')
topic_label = ttk.Label(root, text="None Selected")
topic_label.grid(column=1, row=2, padx=10, pady=5, sticky='w')

ttk.Label(root, text="Countries:").grid(column=0, row=3, padx=10, pady=10, sticky='ew')
ttk.Button(root, text="Select Countries", command=open_country_selector).grid(column=1, row=3, padx=10, pady=10, sticky='ew')
country_label = ttk.Label(root, text="None Selected")
country_label.grid(column=1, row=4, padx=10, pady=5, sticky='w')

ttk.Button(root, text="Fetch News", command=display_news).grid(column=0, row=5, columnspan=2, padx=10, pady=10)

result_text = ScrolledText(root, wrap=tk.WORD)
result_text.grid(column=0, row=6, columnspan=2, padx=10, pady=10, sticky='nsew')
result_text.tag_configure('title', font=('Helvetica', 10, 'bold'))
result_text.tag_configure('summary', font=('Helvetica', 10))
result_text.tag_configure('topic_heading', font=('Helvetica', 10, 'bold'), foreground='purple')
result_text.tag_configure('normal', font=('Helvetica', 10))

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)
root.mainloop()
