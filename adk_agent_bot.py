import os
from google.adk.agents import Agent
from google.adk.tools import google_search

# Create the intelligent agent with built-in Google Search tool
agent = Agent(
    name="knowledge_agent",
    model="gemini-3-flash-preview",   # Matches your previous Gemini script
    instruction="""You are a concise, accurate, and helpful AI assistant.

Rules:
- Decide intelligently: Use the google_search tool ONLY when the question requires up-to-date information, current events, recent facts, or external knowledge.
- For general knowledge, math, definitions, logic, or timeless facts — answer directly without searching.
- After any search, process the results and give a clear, concise, direct summary that fully answers the user's question.
- Never mention tools or your thinking process unless asked.
- Keep responses short and to the point.""",
    tools=[google_search],   # Built-in ADK tool — real Google search results
)

print("🚀 ADK AI Agent Bot Ready!")
print("Gemini + Intelligent Web Search")
print("The agent will decide when to search and always give a clean summary.\n")
print("Type 'exit', 'quit', or 'bye' to stop.\n")

while True:
    question = input("You: ").strip()
    
    if question.lower() in ['exit', 'quit', 'bye']:
        print("👋 Goodbye!")
        break
    
    if not question:
        print("Please ask a question!\n")
        continue
    
    try:
        # The agent reasons, decides on tool use, calls search if needed,
        # processes results, and returns the final concise answer
        response = agent.invoke(question)
        
        # ADK response object typically has .text (or .content in some versions)
        answer = response.text if hasattr(response, "text") else str(response)
        
        print("\nAgent:", answer.strip())
        print("-" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure GEMINI_API_KEY is set and ADK is installed correctly.\n")
