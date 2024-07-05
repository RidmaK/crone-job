# runner_02.py

import json
import re
from dotenv import load_dotenv
from langchain.document_loaders import JSONLoader
import requests
import os

load_dotenv()

class GraphQLLoader:
    def __init__(self, endpoint, query, headers=None):
        self.endpoint = endpoint
        self.query = query
        self.headers = headers

    def load(self):
        response = requests.post(
            self.endpoint,
            json={"query": self.query},
            headers=self.headers,
        )
        response.raise_for_status()

        index = os.environ.get("STRAPI_GRAPHQL_INDEX")
        data = response.json().get("data", {}).get(index, {}).get("data", [])

        documents = [
            {
                "id": entry["id"],
                "title": entry["attributes"]["title"],
                "slug": entry["attributes"]["slug"],
                "content": entry["attributes"]["content"],
                "seo_description": entry["attributes"]["seo"]["seo_description"],
                "seo_title": entry["attributes"]["seo"]["seo_title"]
            }
            for entry in data
        ]

        return documents
    
def extract_href_from_html(html_content, filter_word_2="Inline", filter_word_3="inline"):
    # Create a regex pattern for matching <a> tags with href attributes
    regex_pattern = re.compile(f'<a\\s+[^>]*href=["\'](.*?)["\'][^>]*>.*?<img[^>]*{filter_word_2}[^>]*>|<img[^>]*{filter_word_3}[^>]*>.*?</a>')

    # Use findall to get all matched content
    matched_content = regex_pattern.findall(html_content)

    # Extract only href values from the matched content
    href_urls = [match for match in matched_content]

    return href_urls

def get_data_from_strapi_and_create_json():
    # Read the limit from the environment variables or use a default value (5 in this case)
    limit = int(os.environ.get("STRAPI_GRAPHQL_LIMIT"))
    index = os.environ.get("STRAPI_GRAPHQL_INDEX")

    graphql_query = f"""
    query getAllBlogs {{
      {index}(
        sort: ["updatedAt:desc", "id:desc"]
        pagination: {{ limit: {limit} }}
      ) {{
        data {{
          id
          attributes {{
            title
            seo {{
              seo_title
              seo_description
            }}
            slug
            content
          }}
        }}
      }}
    }}
    """

    graphql_loader = GraphQLLoader(
        endpoint=os.environ.get("STRAPI_GRAPHQL_BASE_URL"),
        query=graphql_query,
    )
    graphql_documents = graphql_loader.load()

    output_data_from_strapi = []

    for document in graphql_documents:
        output_data_from_strapi.append({
            "id": int(document["id"]),
            "title": document["title"],
            "slug": document["slug"],
            "seo_description": document["seo_description"],
            "content": document["content"],
        })
        

        # Applying regex filter to the content field
        filter_word_2 = "Inline"
        filter_word_3 = "inline"
        regex_pattern = re.compile(f"<img[^>]*{filter_word_2}[^>]*>|<img[^>]*{filter_word_3}[^>]*>")

        filtered_content = [
            match.group(0) for match in regex_pattern.finditer(document["content"])
        ]

        # Adding the filtered content to the output_data_from_strapi
        output_data_from_strapi[-1]["filtered_deals_cta_content"] = filtered_content

        filtered_content = document["content"]
        matches = regex_pattern.finditer(filtered_content)

        # Extracting src URLs from img tags
        src_urls = [re.search(r'src="([^"]*)"', match.group(0)).group(1) for match in matches]

        # Adding the extracted src URLs to the output_data_from_strapi
        output_data_from_strapi[-1]["cta_src_urls"] = src_urls

        # Extracting href values from the HTML content
        href_values = extract_href_from_html(document["content"])

        # Adding the extracted href values to the output_data_from_strapi
        output_data_from_strapi[-1]["cta_href_values"] = href_values


    output_file_path = os.environ.get("OUTPUT_FILE_PATH")

    with open(output_file_path, "w") as output_file:
        json.dump(output_data_from_strapi, output_file, indent=2)

    print(f"Data has been saved to {output_file_path}")
    print("Second step is done\n")

    return output_file_path
