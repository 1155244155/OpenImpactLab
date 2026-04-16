from duckduckgo_search import DDGS
import json

def perform_web_search(query: str, max_results: int = 10):
    """
    Perform a web search using DuckDuckGo and return raw results.
    """
    print(f"🔍 Searching the web for: '{query}' ...\n")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            print("No results found.")
            return []
        
        # Print raw results in a clean, readable format
        print(f"✅ Found {len(results)} results:\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. **{result['title']}**")
            print(f"   URL: {result['href']}")
            print(f"   Snippet: {result['body'][:300]}..." if len(result['body']) > 300 else f"   Snippet: {result['body']}")
            print("-" * 80)
        
        return results  # Return list of dicts for further use (e.g., feed to LLM)
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

# Interactive demo
if __name__ == "__main__":
    print("🌐 Web Search Tool Ready!")
    print("Type your search query (or 'exit' to quit)\n")
    
    while True:
        query = input("Search query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not query:
            print("Please enter a search query.\n")
            continue
        
        results = perform_web_search(query, max_results=8)
        
        # Optional: Save to JSON for later use
        # with open("search_results.json", "w", encoding="utf-8") as f:
        #     json.dump(results, f, indent=2, ensure_ascii=False)
