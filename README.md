# llm-with-bing-search-api
Leverage Azure OpenAI with Bing Search API to query information from the web

**Required Azure resources:**
1. Azure OpenAI resource with gpt-4o deployment (named "gpt-4o")
2. Bing Search resource

**Required environment variables:**
```
BING_SUBSCRIPTION_KEY = "<Add Bing Subscription Key>"
AZURE_OPENAI_ENDPOINT = "<Add Azure OpenAI Endpoint>"
AZURE_OPENAI_KEY = "<Add Azure OpenAI API Key>"
AZURE_OPENAI_API_VERSION = "2024-09-01-preview"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"
```

**References:**
[Create Bing Search resource](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource)
[Create an Azure OpenAI resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
