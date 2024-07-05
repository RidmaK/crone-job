# main.py

import os
from Runners.runner_01 import get_data_from_strapi_and_create_json
from Runners.runner_02 import get_deals_cta_data_from_strapi_and_create_json
from Runners.runner_03 import add_deals_cta_tags
from Runners.runner_04 import create_new_deals_cta_banners
from Runners.runner_05 import search_and_update_related_articles

MEILI_INDEX_NAME = os.environ.get("MEILI_INDEX_NAME")

def main():
    # Step_02
    # get_data_from_strapi_and_create_json()

    # Step_02
    # get_deals_cta_data_from_strapi_and_create_json()
    
    # Step_03
    # add_deals_cta_tags()

    # Step_04
    # create_new_deals_cta_banners()

    # Step_05
    search_and_update_related_articles()

if __name__ == "__main__":
    main()


# _Index__settings_url_for
# __class__
# __delattr__
# __dict__
# __dir__
# __doc__
# __eq__
# __format__
# __ge__
# __getattribute__
# __gt__
# __hash__
# __init__
# __init_subclass__
# __le__
# __lt__
# __module__
# __ne__
# __new__
# __reduce__
# __reduce_ex__
# __repr__
# __setattr__
# __sizeof__
# __str__
# __subclasshook__
# __weakref__
# _batch
# _build_url
# add_documents
# add_documents_csv
# add_documents_in_batches
# add_documents_json
# add_documents_ndjson
# add_documents_raw
# config
# create
# created_at
# delete
# delete_all_documents
# delete_document
# delete_documents
# facet_search
# fetch_info
# get_dictionary
# get_displayed_attributes
# get_distinct_attribute
# get_document
# get_documents
# get_faceting_settings
# get_filterable_attributes
# get_non_separator_tokens
# get_pagination_settings
# get_primary_key
# get_ranking_rules
# get_searchable_attributes
# get_separator_tokens
# get_settings
# get_sortable_attributes
# get_stats
# get_stop_words
# get_synonyms
# get_task
# get_tasks
# get_typo_tolerance
# http
# primary_key
# reset_dictionary
# reset_displayed_attributes
# reset_distinct_attribute
# reset_faceting_settings
# reset_filterable_attributes
# reset_non_separator_tokens
# reset_pagination_settings
# reset_ranking_rules
# reset_searchable_attributes
# reset_separator_tokens
# reset_settings
# reset_sortable_attributes
# reset_stop_words
# reset_synonyms
# reset_typo_tolerance
# search
# task_handler
# uid
# update
# update_dictionary
# update_displayed_attributes
# update_distinct_attribute
# update_documents
# update_documents_csv
# update_documents_in_batches
# update_documents_json
# update_documents_ndjson
# update_documents_raw
# update_faceting_settings
# update_filterable_attributes
# update_non_separator_tokens
# update_pagination_settings
# update_ranking_rules
# update_searchable_attributes
# update_separator_tokens
# update_settings
# update_sortable_attributes
# update_stop_words
# update_synonyms
# update_typo_tolerance
# updated_at
# wait_for_task