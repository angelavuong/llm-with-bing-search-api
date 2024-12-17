# This is an example of how to use the Bing Search API and the Azure OpenAI API to extract specific information
# from a website and generate a summary using a Large Language Model (LLM).

# Prerequisites:
# CTRL+SHIFT+P -> Python: Select Interpreter -> Create Virtual Environment -> venv
# .\.venv\Scripts\Activate
# pip install -r requirements.txt
# copy .env.template to .env and fill in the values

# Azure RBAC required for Azure OpenAI resource
# Cognitive Services OpenAI User
# Cognitive Services OpenAI Contributor
# Cognitive Services Contributor
# Cognitive Services Usages Reader


import requests
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Bing Search API configuration
BING_SEARCH_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_SUBSCRIPTION_KEY = os.getenv("BING_SUBSCRIPTION_KEY")

# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


# Mapping of persons to their specific websites
person_website_map = {
    "TED CRUZ": "https://www.tedcruz.org/",
    "RON DESANTIS": "https://www.rondesantis.com/",
    "MARCO RUBIO": "https://www.marcorubio.com/",
    "KAMALA HARRIS": "https://www.kamalaharris.com/",
    "JOE BIDEN": "https://www.joebiden.com/",
    "DONALD TRUMP": "https://www.donaldjtrump.com/",
    "BETO O'ROURKE": "https://www.betoorourke.com/",
    "JOHN KASICH": "https://www.johnkasich.com/",
    "JOHN JAMES": "https://www.johnjames.com/",
    # Add all 20 persons and their corresponding websites
}


# THIS FUNCTION CALLS THE BING SEARCH API TO SEARCH FOR A QUERY ON A SPECIFIC SITE
def search_bing(query, site, count=10):
    headers = {"Ocp-Apim-Subscription-Key": BING_SUBSCRIPTION_KEY}
    params = {
        "q": f"site:{site} {query}",  # Limits the search to a specific site
        "count": count,  # Limits the number of search results
        "textDecorations": True,  # Specifies whether the search results should include decorative elements such as bold or italic text
        "textFormat": "HTML",  # Specifies the text format to use for the search results
    }

    response = requests.get(BING_SEARCH_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    return search_results


# THIS FUNCTION EXTRACTS SPECFIC INFORMATION FROM THE SEARCH RESULTS
def extract_info(search_results):
    extracted_text = ""
    for item in search_results.get("webPages", {}).get("value", []):
        extracted_text += f"Title: {item['name']}\n"
        extracted_text += f"Snippet: {item['snippet']}\n\n"
    return extracted_text


# THIS FUNCTION CALLS THE LLM TO GENERATE A RESPONSE
def generate_openai_response(prompt):
    client = AzureOpenAI(
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()


# MAIN FUNCTION
def main():
    for person, website in person_website_map.items():
        search_query = f"{person} name address "

        # Get the full search results from Bing
        search_results = search_bing(search_query, website)

        # Extract specific information from the search results
        extracted_info = extract_info(search_results)

        print(f"Extracted Information from Bing for {person}:")
        print(extracted_info)

        prompt = f"Extract the name, state, address, and a three-sentence biography for {person} from the following information:\n\n{extracted_info}"
        print(prompt)

        # Calls the LLM, including the extracted web search information as a prompt
        summary = generate_openai_response(prompt)

        print(f"Extracted Information for {person}:")
        print(extracted_info)
        print(f"\nGenerated Summary for {person}:")
        print(summary)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
