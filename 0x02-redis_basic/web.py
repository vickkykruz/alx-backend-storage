#!/usr/bin/env python3
""" This is a module that implement a get_page function (prototype:
def get_page(url: str) -> str:). The core of the function is very simple.
It uses the requests module to obtain the HTML content of a particular URL and
returns it
"""


import requests
import redis
import time


redis_conn = redis.Redis()


def get_page(url: str) -> str:
    """ This is a function that return the HTM content of a partcular URL """

    # Check if the URL access count is already stored in Redis
    count_key = f"count:{url}"
    access_count = redis_conn.get(count_key)

    # If URL access count is not in Redis or if it has expired, fetch the page
    if access_count is None:
        response = requests.get(url)
        html_content = response.text

        # Cache the page content with an expiration time of 10 seconds
        redis_conn.setex(url, 10, html_content)

        # Set the URL access count to 1
        redis_conn.setex(count_key, 10, 1)
    else:
        # If URL access count is already in Redis, increment it
        redis_conn.incr(count_key)

        # Retrieve the cached page content
        html_content = redis_conn.get(url)

    return html_content


if __name__ == "__main__":
    # Example usage
    url = ("http://slowwly.robertomurray.co.uk/delay/1000/url/"
           "http://www.example.com")
    page_content = get_page(url)
    print(page_content)

    # Sleep for a while to ensure the cache expiration
    time.sleep(5)

    # Access the page again
    page_content = get_page(url)
    print(page_content)
