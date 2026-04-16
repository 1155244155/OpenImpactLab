from ddgs import DDGS
from typing import List, Dict, Any

def perform_web_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Perform a web search using DDGS (DuckDuckGo metasearch) and return raw results.
    Prints titles, URLs, and snippets clearly.
    """
    print(f"🔍 Searching the web for: '{query}' ...\n")
    
    try:
        with DDGS() as ddgs:
            # Use text search with multiple backends for better coverage
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            print("❌ No results found for this query.")
            return []
        
        print(f"✅ Found {len(results)} relevant results:\n")
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title available")
            url = result.get("href", result.get("url", "No URL available"))
            snippet = result.get("body", result.get("snippet", "No snippet available"))
            
            print(f"{i}. **{title}**")
            print(f"   📎 URL: {url}")
            print(f"   📝 Snippet: {snippet[:280]}{'...' if len(snippet) > 280 else ''}")
            print("-" * 90)
        
        return results  # Structured list of dicts for future integration
        
    except Exception as e:
        print(f"❌ Error during web search: {e}")
        print("   Tip: This can happen occasionally due to rate limits. Try again shortly.")
        return []


# Interactive test / standalone mode
if __name__ == "__main__":
    print("🌐 Web Search Tool Ready (powered by DDGS)\n")
    print("Enter a search query. Type 'exit', 'quit', or 'bye' to stop.\n")
    
    while True:
        query = input("🔎 Enter search query: ").strip()
        
        if query.lower() in ["exit", "quit", "bye"]:
            print("👋 Web search tool closed.")
            break
        
        if not query:
            print("Please enter a search query.\n")
            continue
        
        perform_web_search(query, max_results=8)
