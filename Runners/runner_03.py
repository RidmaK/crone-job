import re

def add_deals_cta_tags(content):
    filter_word_2 = "Inline"
    filter_word_3 = "inline"

    # Define the regex pattern to find img tags with specified filter words
    regex_pattern = re.compile(f"<img[^>]*{filter_word_2}[^>]*>|<img[^>]*{filter_word_3}[^>]*>")

    # Find all matches in the content
    matches = regex_pattern.finditer(content)

    # Initialize a counter for deals-cta tags
    deals_cta_counter = 1

    # Loop through matches and replace img tags with deals-cta tags
    for match in matches:
        img_tag = match.group(0)
        deals_cta_tag = f"<div class='raw-html-embed'><deals-cta-{deals_cta_counter}>{img_tag}</deals-cta-{deals_cta_counter}></div>"
        
        # Replace the img tag with the new deals-cta tag in the content
        content = content.replace(img_tag, deals_cta_tag, 1)

        # Increment the counter for the next deals-cta tag
        deals_cta_counter += 1

    return content

