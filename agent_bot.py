import os
from google.adk.agents import Agent
from google.adk.tools import google_search

# Enhanced system prompt for better behavior
SYSTEM_INSTRUCTION = """You are a helpful, concise, and accurate AI assistant.

Core rules:
- For general knowledge, definitions, math, logic, or timeless facts → answer directly without tools.
- For current events, recent news, specific facts after 2023, prices, sports scores, or anything that might need up-to-date info → use the google_search tool first.
- After searching, synthesize the results into a clear, concise, and direct answer.
- Never mention tools, search results, or your internal reasoning in the final response.
- Keep answers focused and easy to read. Use bullet points or short paragraphs when helpful."""

# Initialize the ADK Agent with web search capability
agent = Agent(
    name="knowledge_agent",
    model="gemini-3-flash-preview",
    instruction=SYSTEM_INSTRUCTION,
    tools=[google_search],
)

def print_header():
    print("\n" + "="*70)
    print("🚀 ADK AI Agent Bot".center(70))
    print("Gemini + Intelligent Web Search".center(70))
    print("="*70)

def main():
    print_header()
    print("Ask anything! The agent will intelligently decide whether to search the web.")
    print("Type 'exit', 'quit', or 'bye' to stop.\n")

    while True:
        try:
            question = input("\n\033[1;36mYou: \033[0m").strip()  # Cyan prompt
            
            if question.lower() in ['exit', 'quit', 'bye']:
                print("\n\033[1;33m👋 Thank you for using the ADK AI Agent. Goodbye!\033[0m\n")
                break
            
            if not question:
                print("Please ask a question.")
                continue
            
            print("\n\033[1;32mAgent is thinking...\033[0m")  # Green thinking indicator
            
            # Agent handles reasoning, tool use (if needed), and final summary
            response = agent.invoke(question)
            answer = response.text if hasattr(response, "text") else str(response)
            
            print("\n\033[1;34mAgent:\033[0m")  # Blue label
            print(answer.strip())
            print("-" * 70)
            
        except KeyboardInterrupt:
            print("\n\n\033[1;33m👋 Session interrupted. Goodbye!\033[0m")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("   Make sure your GEMINI_API_KEY is set correctly.\n")

if __name__ == "__main__":
    # Ensure API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Warning: GEMINI_API_KEY environment variable not found.")
        print("   Set it with: export GEMINI_API_KEY='your_key_here'\n")
    
    main()
