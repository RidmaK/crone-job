# runner_05.py

import os
import json
import requests
from langchain.document_loaders import JSONLoader
from Runners.runner_02 import get_deals_cta_data_from_strapi_and_create_json
import time

STRAPI_BASE_URL = os.environ.get("STRAPI_BASE_URL")
STRAPI_TOKEN = os.environ.get("STRAPI_TOKEN")
OUTPUT_FILE_PATH = os.environ.get("OUTPUT_FILE_PATH")
STRAPI_FIELD_NAME = os.environ.get("STRAPI_FIELD_NAME")

# ...

def create_new_deals_cta_banners():
    loader = JSONLoader(
        file_path="./" + OUTPUT_FILE_PATH,
        jq_schema=".[] | {id: .id, title: .title, slug: .slug, seo_description: .seo_description, cta_src_urls: .cta_src_urls, cta_href_values: .cta_href_values}",
        text_content=False,
    )
    documents = loader.load()

    api_url = os.environ.get("STRAPI_API_URL")
    api_token = os.environ.get("STRAPI_CEATE_DEALS_BANNERS_TOKEN")

    with open("strapi-all-deals-cta-list.json", "r") as deals_file:
        deals_cta_list = json.load(deals_file)

    output_data_from_strapi = []
    x=1
    for document in documents:
        y=0
        try:
            json_data = json.loads(document.page_content)
            current_blog_id = json_data.get('id')
            current_title = json_data.get('title')
            current_cta_src_urls = json_data.get('cta_src_urls', [])
            current_cta_href_urls = json_data.get('cta_href_values', [])

            print(f"title: {current_title}")
            if current_blog_id:
                y=y+x
                for cta_src_url, cta_href_url in zip(current_cta_src_urls, current_cta_href_urls):
                    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}

                    # Check if the record with the same cta_src_url exists in deals_cta_list
                    existing_record = next(
                            (deal for deal in deals_cta_list if deal["cta_banner"]["url"] == cta_src_url),
                            None
                        )

                    if existing_record:
                        print(f"Record with cta_src_url '{cta_src_url}' already exists. Skipping creation.")
                    else:

                        # Make the POST request to create a new record
                        try:
                            output_data_from_strapi.append({
                            "id": y,
                            "_softDeletedAt": None,
                            "_softDeletedById": None,
                            "_softDeletedByType": None,
                            "name": cta_src_url.split("/")[-1].split(".")[0],
                            "slug": cta_src_url.split("/")[-1].split(".")[0],
                            "url": cta_href_url,
                            "createdAt": "2024-02-21T05:17:24.230Z",
                            "updatedAt": "2024-02-21T05:17:25.849Z",
                            "publishedAt": "2024-02-21T05:17:25.840Z",
                            "locale": "en",
                            "cta_banner": {
                                "id": y,
                                "url": cta_src_url,
                                "name": cta_src_url,
                                "alternativeText": cta_src_url
                            },
                                "blogs": [],
                                "localizations": []
                        })

                        except requests.RequestException as e:
                            print(f"Request error: {e}")
                    y=y+1

            x=x+2       

            

        except Exception as e:
            print(f"Error during search: {e}")
    output_file_path = "strapi-all-deals-cta-list.json"
    # Create a set to store unique URLs
    unique_urls = set()

    # Filter the list based on unique URLs in cta_banner["url"]
    filtered_data = [item for item in output_data_from_strapi if (url := item["cta_banner"]["url"]) not in unique_urls and not unique_urls.add(url)]

    with open(output_file_path, "w") as output_file:
        json.dump(filtered_data, output_file, indent=2)

    print("Fourth step is done\n")
