import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def pharmacy_availability_search(medicine_name, location):
    """
    Search the web for pharmacies and medicine listings
    for a given medicine and location.
    """

    query = f"{medicine_name} available pharmacy {location}"

    response = tavily.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = []

    for result in response.get("results", []):
        results.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content")
        })

    return {
        "medicine": medicine_name,
        "location": location,
        "results": results
    }


if __name__ == "__main__":

    result = pharmacy_availability_search(
        "paracetamol",
        "Chennai"
    )

    print(result)