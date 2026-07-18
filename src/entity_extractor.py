import spacy
import re

nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Normalization dictionaries
# -----------------------------
COUNTRY_MAP = {
    "USA": "United States",
    "U.S.": "United States",
    "US": "United States",
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates"
}

CITY_COUNTRY_MAP = {
    "Shanghai": "China",
    "Shenzhen": "China",
    "Beijing": "China",
    "Mumbai": "India",
    "Delhi": "India",
    "Ho Chi Minh City": "Vietnam",
    "Hanoi": "Vietnam",
    "Tokyo": "Japan",
    "Seoul": "South Korea",
    "Singapore": "Singapore"
}


def normalize_country(country):
    return COUNTRY_MAP.get(country, country)


def remove_duplicates(values):
    seen = set()
    result = []

    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)

    return result


def extract_entities(news):
    """
    Parameters:
        news (dict)

    Example:
    {
        "title": "...",
        "content": "...",
        "category": "...",
        "severity": "High"
    }
    """

    text = news.get("title", "") + "\n" + news.get("content", "")

    doc = nlp(text)

    entities = {
        "countries": [],
        "cities": [],
        "ports": [],
        "airports": [],
        "suppliers": [],
        "plants": [],
        "shipping_routes": []
    }

    # -----------------------------
    # Named Entity Recognition
    # -----------------------------
    for ent in doc.ents:

        value = ent.text.strip()

        if ent.label_ == "GPE":

            if value in CITY_COUNTRY_MAP:
                entities["cities"].append(value)

            else:
                entities["countries"].append(normalize_country(value))

        elif ent.label_ == "ORG":
            if value.endswith("Plant"):
                entities["plants"].append(value)
                entities["suppliers"].append(
                   re.sub(r"\s+Plant$", "", value).strip()
                )
            elif not value.endswith(("Port", "Airport")):
                entities["suppliers"].append(value)

    # -----------------------------
    # Rule-based extraction
    # -----------------------------

    port_pattern = r'\b([A-Z][A-Za-z]*(?:\s[A-Z][A-Za-z]*)*\sPort)\b'

    airport_pattern = r'\b([A-Z][A-Za-z]*(?:\s[A-Z][A-Za-z]*)*\sAirport)\b'

    plant_pattern = r'\b([A-Z][A-Za-z0-9&-]*(?:\s[A-Z][A-Za-z0-9&-]*)*\sPlant)\b'

    route_pattern = r'\b(Route\s\d+|[A-Z][A-Za-z]*(?:\s[A-Z][A-Za-z]*)*\sRoute)\b'

    entities["ports"].extend(re.findall(port_pattern, text))
    entities["airports"].extend(re.findall(airport_pattern, text))
    entities["plants"].extend(re.findall(plant_pattern, text))
    entities["shipping_routes"].extend(re.findall(route_pattern, text))

    # Infer supplier names from plant names
    for plant in entities["plants"]:
        supplier = re.sub(r"\s+Plant$", "", plant).strip()
        if supplier:
            entities["suppliers"].append(supplier)

    # -----------------------------
    # Infer country from city
    # -----------------------------
    for city in entities["cities"]:
        country = CITY_COUNTRY_MAP.get(city)

        if country:
            entities["countries"].append(country)

    # -----------------------------
    # Normalize countries
    # -----------------------------
    entities["countries"] = [
        normalize_country(c)
        for c in entities["countries"]
    ]

    # -----------------------------
    # Remove duplicates
    # -----------------------------
    for key in entities:
        entities[key] = remove_duplicates(entities[key])

    return entities


# --------------------------------------------------
# Example
# --------------------------------------------------

if __name__ == "__main__":

    sample_news = {
        "title": "Floods disrupt Samsung operations in Vietnam",
        "content": """
        Heavy flooding near Ho Chi Minh City disrupted
        Samsung Plant.

        Shipments through Cat Lai Port were delayed.

        Flights from Tan Son Nhat Airport were cancelled.

        Supply chain experts warned that Route 5 may also
        experience delays.
        """,
        "category": "Natural Disaster",
        "severity": "High"
    }

    result = extract_entities(sample_news)

    from pprint import pprint

    pprint(result)