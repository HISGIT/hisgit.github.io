from typing import List
from urllib.parse import urlparse
import feedparser
import datetime
from dateutil.parser import parse

from tqdm import tqdm
from bs4 import BeautifulSoup

target_file = "_layouts/blogroll.html"

def remove_html_tags(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text()
    return cleaned_text


def get_base_url(feed_url: str) -> str:
    parsed_url = urlparse(feed_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def strip_protocol(url: str) -> str:
    if url.startswith("https://"):
        return url.lstrip("https://")
    elif url.startswith("http://"):
        return url.lstrip("http://")
    return url


def read_websites(filename: str) -> List[str]:
    with open(filename, "r") as file:
        return file.read().splitlines()


def write_html_with_updates(entries: List[feedparser.FeedParserDict]) -> None:
    today = datetime.datetime.today()
    three_months_ago = today - datetime.timedelta(days=90)

    links = []
    for entry in tqdm(entries):
        if not hasattr(entry, "links"):
            continue
        url = entry.links[0]['href']
        title = entry.title
        try:
            d = entry.get("published") or entry.get("updated")
            published_date = parse(d, ignoretz=True, fuzzy=True)
        except Exception:
            print("Skipping: ", url)
            continue
        if published_date >= three_months_ago:
            links.append((url, title, published_date))

    sorted_links = sorted(links, key=lambda x: x[2], reverse=True)

    html = """---
layout: default
# All the Tags of posts.
---
    <h1>Blogroll</h1>
    </br>
    This is a list of all the posts published by my favourite <a href="https://github.com/HISGIT/hisgit.github.io/blob/master/_data/websites.txt">blogs</a> during the last
    30 days.
    </br>
    </br>
    <div class="special-list">
    <ul>
    """

    for link, title, date in sorted_links:
        title = remove_html_tags(title)
        html += f"""
            <li>
            <span class="post-date">{date.date()}</span> -
            <a href='{link}'>{title}</a></li>\n
        """

    html += """
    </ul>
    </div>
    """

    with open(target_file, "w") as file:
        file.write(html)

    print("HTML file with updated links generated.")
def write_html_blog_metadata(
    feed_list: List[feedparser.FeedParserDict],
    target_file: str) -> None:
    items = []
    entries_per_feed = 3

    for feed in feed_list:
        entries = []
        print("Processing feed:", feed.get("feed", {}).get("title", "Unknown Feed"))
        # link
        if not hasattr(feed, "feed"):
            continue
        entries = feed.entries
        headers = feed.get("headers", {})
        feed = feed.get("feed", "")
        link = feed.get("link", "")

        # title
        title = remove_html_tags(feed.get("title", "Untitled"))

        # updated time
        try:
            d = feed.get("updated") or feed.get("published") or headers.get("date")
            updated_date = parse(d, ignoretz=True, fuzzy=True)
        except Exception:
            continue

        # description / summary
        description = feed.get("summary") or feed.get("description") or ""
        description = remove_html_tags(description).strip()

        # fetch only the latest 3 entry for each feed
        today = datetime.datetime.today()
        three_months_ago = today - datetime.timedelta(days=90)

        links = []
        for entry in tqdm(entries):
            if not hasattr(entry, "links"):
                continue
            url = entry.links[0]['href']
            entry_title = entry.title
            try:
                d = entry.get("published") or entry.get("updated")
                published_date = parse(d, ignoretz=True, fuzzy=True)
            except Exception:
                print("Skipping: ", url)
                continue
            if published_date >= three_months_ago:
                links.append((url, entry_title, published_date))
        sorted_links = sorted(links, key=lambda x: x[2], reverse=True)
        sorted_links = sorted_links[:entries_per_feed]

        items.append((title, link, updated_date, description, sorted_links))
    # sort by updated time (newest blog-post first)
    items.sort(key=lambda x: x[4][2], reverse=True)

    html = """---
layout: page
---
<h1 style="display:inline;">Friends Blog </h1><a style="color: #00000089;">During the last 90 days</a>

<div class="blogroll-meta">
<ul>
"""

    for title, link, date, description, sorted_links in items:
        html += f"""
            <li>
            <strong><a href='{link}'>{title}</a></strong> - Last updated: <span class="post-date">{date.date()}</span> .</br>
            Description: {description}
            <ul>
        """
        for entry_link, entry_title, published_date in sorted_links:    
            html += f"""<li>
            <span class="post-date">{published_date.date()}</span> - 
            <a href='{entry_link}'>{entry_title}</a></li>\n
            """
        html += """</ul>
            </li>
        """

    html += """
</ul>
</div>
"""

    with open(target_file, "w") as file:
        file.write(html)

    print(f"Blog metadata HTML generated: {target_file}")


def main():

    # Read websites from websites.txt
    websites = read_websites("_data/websites.txt")

    # Check for updates, aggregate entries
    entries = []
    feeds = []
    for website in tqdm(websites):
        feed = feedparser.parse(website)
        feeds.append(feed)
        entries += feed.entries
    # write_html_with_updates(entries)
    write_html_blog_metadata(feeds, target_file)
if __name__ == "__main__":
    main()