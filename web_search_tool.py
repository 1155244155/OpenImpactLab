from ddgs import DDGS
import json
from typing import List, Dict

def perform_web_search(query: str, max_results: int = 10) -> List[Dict]:
    """
    Perform a web search and return raw results with title, URL, and snippet.
    """
    print(f"🔍 Searching the web for: '{query}' ...\n")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            print("❌ No results found for the query.")
            return []
        
        print(f"✅ Found {len(results)} relevant results:\n")
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            url = result.get('href', 'No URL')
            snippet = result.get('body', 'No snippet available')
            
            print(f"{i}. **{title}**")
            print(f"   📎 URL: {url}")
            print(f"   📝 Snippet: {snippet[:280]}{'...' if len(snippet) > 280 else ''}")
            print("-" * 85)
        
        return results  # List of dicts for further processing (e.g., feed to Gemini)
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        print("   Tip: Try again in a moment — occasional rate limits can occur.")
        return []


# Interactive demo / test
if __name__ == "__main__":
    print("🌐 Web Search Tool (using DDGS / DuckDuckGo)\n")
    print("Type your search query below. Type 'exit' or 'quit' to stop.\n")
    
    while True:
        query = input("🔎 Search query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("👋 Web search tool closed.")
            break
        
        if not query:
            print("Please enter a valid search query.\n")
            continue
        
        results = perform_web_search(query, max_results=8)
        
        # Optional: Save results to JSON file
        # with open(f"search_results_{query[:30]}.json", "w", encoding="utf-8") as f:
        #     json.dump(results, f, indent=2, ensure_ascii=False)
