import os
import requests
from dotenv import load_dotenv

load_dotenv()

RXNORM_BASE_URL = os.getenv("RXNORM_BASE_URL")
MEDLINEPLUS_CONNECT_URL = os.getenv("MEDLINEPLUS_CONNECT_URL")


def find_rxcui(medicine_name):
    url = f"{RXNORM_BASE_URL}/rxcui.json"

    params = {
        "name": medicine_name,
        "search": 1
    }

    response = requests.get(url, params=params, timeout=10)

    response.raise_for_status()

    data = response.json()

    id_group = data.get("idGroup", {})
    rxcui_list = id_group.get("rxnormId")

    if not rxcui_list:
        return None

    return rxcui_list[0]


def get_medlineplus_information(rxcui):
    params = {
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.88",
        "mainSearchCriteria.v.c": rxcui,
        "knowledgeResponseType": "application/json"
    }

    response = requests.get(
        MEDLINEPLUS_CONNECT_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()

def medical_information_search(medicine_name):
    rxcui = find_rxcui(medicine_name)

    if not rxcui:
        return {
            "success": False,
            "medicine": medicine_name,
            "message": "Medicine not found in RxNorm."
        }

    data = get_medlineplus_information(rxcui)

    entries = data.get("feed", {}).get("entry", [])

    if not entries:
        return {
            "success": False,
            "medicine": medicine_name,
            "rxcui": rxcui,
            "message": "No MedlinePlus information found."
        }

    first_entry = entries[0]

    title = first_entry.get("title", {}).get("_value")
    summary = first_entry.get("summary", {}).get("_value")

    links = first_entry.get("link", [])

    source_url = None

    if links:
        source_url = links[0].get("href")

    return {
        "success": True,
        "medicine": medicine_name,
        "rxcui": rxcui,
        "title": title,
        "summary": summary,
        "source": "MedlinePlus",
        "source_url": source_url
    }