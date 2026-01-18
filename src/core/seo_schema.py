import json
from typing import Dict, Any, List

def generate_software_schema(name: str, title: str, description: str, keywords: List[str], base_url: str) -> str:
    """
    Generate JSON-LD SoftwareApplication schema for a tool.

    This helps Google display the tool with a "Free" tag or star rating in search results.
    """
    # Determine category based on keywords or name
    category = "UtilityApplication"
    multimedia_keywords = ['pdf', 'video', 'image', 'audio', 'editor', 'convert']
    if any(k in name.lower() or k in " ".join(keywords).lower() for k in multimedia_keywords):
        category = "MultimediaApplication"

    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": title,
        "description": description,
        "applicationCategory": category,
        "operatingSystem": "Web",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "url": f"{base_url.rstrip('/')}/{name}/",
        "keywords": ", ".join(keywords[:10]),
        "author": {
            "@type": "Person",
            "name": "Chirag Singhal",
            "url": "https://github.com/chirag127"
        }
    }

    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'
