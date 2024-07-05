# Import necessary libraries
import json
import re
from dotenv import load_dotenv
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
        response_json = response.json()
        data = response_json.get("data", {}).get("dealsCtaLists", {}).get("data", [])
        documents = [
          {
              "id": entry["id"],
              "name": entry["attributes"]["name"],
              "slug": entry["attributes"]["slug"],
              "url": entry["attributes"]["url"],
              "cta_banner": entry["attributes"]["cta_banner"]["data"]["attributes"]["url"]
              if entry["attributes"]["cta_banner"] and entry["attributes"]["cta_banner"]["data"]
              else None,
          }
          for entry in data
      ]

        return documents

def get_deals_cta_data_from_strapi_and_create_json():
    # Read the limit from the environment variables or use a default value (5 in this case)
    limit = int(os.environ.get("STRAPI_GRAPHQL_LIMIT"))

    graphql_query = """
    query GetRelatedArticles {
      dealsCtaLists(pagination: { limit: """ + str(-1) + """ }) {
        data {
          id
          attributes {
            name
            slug
            url
            cta_banner {
              data {
                attributes {
                  url
                  alternativeText
                  caption
                  height
                  width
                  name
                }
              }
            }
          }
        }
      }
    }
    """

    graphql_loader = GraphQLLoader(
        endpoint=os.environ.get("STRAPI_GRAPHQL_BASE_URL"),
        query=graphql_query,
    )
    graphql_documents = graphql_loader.load()

    output_data_from_strapi = []

    for document in graphql_documents:
        output_data_from_strapi.append({
            "id": document["id"],
            "_softDeletedAt": None,
            "_softDeletedById": None,
            "_softDeletedByType": None,
            "name": document["name"],
            "slug": document["slug"],
            "url": document["url"],
            "createdAt": "2024-02-21T05:17:24.230Z",
		        "updatedAt": "2024-02-21T05:17:25.849Z",
		        "publishedAt": "2024-02-21T05:17:25.840Z",
		        "locale": "en",
            "cta_banner": {
                "id": document["id"],
                "url": document["cta_banner"],
                "name": document["cta_banner"],
                "alternativeText": document["cta_banner"]
            },
		        "blogs": [],
		        "localizations": []
        })

    output_file_path = "strapi-all-deals-cta-list.json"

    with open(output_file_path, "w") as output_file:
        json.dump(output_data_from_strapi, output_file, indent=2)

    print(f"Data has been saved to {output_file_path}")
    print("Third step is done\n")

    return output_file_path
