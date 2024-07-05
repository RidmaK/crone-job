# runner_05.py

import os
import json
import requests
from langchain.document_loaders import JSONLoader
import time
from Runners.runner_03 import add_deals_cta_tags

STRAPI_BASE_URL = os.environ.get("STRAPI_BASE_URL")
STRAPI_TOKEN = os.environ.get("STRAPI_TOKEN")
OUTPUT_FILE_PATH = os.environ.get("OUTPUT_FILE_PATH")
STRAPI_FIELD_NAME = os.environ.get("STRAPI_FIELD_NAME")

def search_and_update_related_articles():
    loader = JSONLoader(
        file_path="./"+OUTPUT_FILE_PATH,
        jq_schema=".[] | {id: .id, title: .title, slug: .slug, seo_description: .seo_description, cta_src_urls: .cta_src_urls, content: .content}",
        text_content=False,
    )
    documents = loader.load()

    api_url = STRAPI_BASE_URL
    api_token = STRAPI_TOKEN

    with open("strapi-all-deals-cta-list.json", "r") as deals_file:
        deals_cta_list = json.load(deals_file)
    for document in documents:
        try:
            json_data = json.loads(document.page_content)
            current_blog_id = json_data.get('id')
            current_title = json_data.get('title')
            current_slug = json_data.get('slug')
            content = json_data.get('content')
            current_seo_description = json_data.get('seo_description')
            current_cta_src_urls = json_data.get('cta_src_urls', [])    

            print(f"title: {current_title}")

            query = f"{current_title} {current_seo_description}"

            if query:
                if current_blog_id:
                    api_endpoint = f"{api_url}{current_blog_id}"
                    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
                    payload = {
                        "data": {
                            "deals_cta_lists": [],
                            "content": '',
                        }
                    }

                    for cta_src_url in current_cta_src_urls:
                        # Find matching cta_banner in the deals_cta_list JSON
                        matching_deal = next(
                            (deal for deal in deals_cta_list if deal["cta_banner"]["url"] == cta_src_url),
                            None
                        )

                        if matching_deal:
                            payload["data"]["deals_cta_lists"].append(matching_deal["id"])
                    # Use string concatenation to append the deals-cta tags to the content
                    payload["data"]["content"] += add_deals_cta_tags(content)
                    # print(f"payload {payload}")
                    response = requests.put(api_endpoint, headers=headers, json=payload)
                    # print(f"response {response.json()}")
                    if response.status_code == 200:
                        print(f"Successfully updated for ID {current_blog_id}")
                        time.sleep(5)
                    else:
                        print(f"Failed to update. Status code: {response.status_code}, Response: {response.text}")
                        # Add more detailed error handling
                        try:
                            response_json = response.json()
                            print(f"Error details: {response_json}")
                        except json.JSONDecodeError:
                            print("Failed to decode response JSON")

        except Exception as e:
            print(f"Error during search: {e}")

    print("Fifth step is done\n")

    print("**************************************")
    print("All Documents Updated")
    print("**************************************")

