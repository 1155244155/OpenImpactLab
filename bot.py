import os
import genai

# The SDK automatically reads GEMINI_API_KEY from your environment
client = genai.Client()

print("🚀 Gemini Bot is ready!")
print("Ask anything. Type 'exit', 'quit', or 'bye' to stop.\n")

while True:
    question = input("You: ").strip()
    
    if question.lower() in ['exit', 'quit', 'bye']:
        print("👋 Goodbye!")
        break
    
    if not question:
        print("Please ask a question!\n")
        continue
    
    try:
        # Send the question to Gemini and get a direct response
        response = client.models.generate_content(
            model="gemini-3-flash-preview",   # Fast, capable model (official quickstart default)
            contents=question
        )
        
        print("\nGemini:", response.text.strip())
        print("-" * 50)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your GEMINI_API_KEY is set correctly.\n")
