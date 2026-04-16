import json
import os
import requests

# =============================================
# DESIGN DECISIONS (as required)
# =============================================
# Data Structure : List of dictionaries
#   Format: [{"text": "The fact here"}, {"text": "Another fact"}, ...]
#
# Storage Format : JSON file
#   Filename: useless_facts_archive.json
#   Why JSON? Human-readable, easy to extend, handles text perfectly.

ARCHIVE_FILE = "useless_facts_archive.json"


def load_facts():
    """Load existing facts from the local JSON file."""
    if not os.path.exists(ARCHIVE_FILE):
        print(f"📂 No archive found. Starting fresh archive: {ARCHIVE_FILE}")
        return []
    
    try:
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            facts = json.load(f)
        print(f"✅ Loaded {len(facts)} facts from archive.")
        return facts
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Error reading archive. Starting fresh. ({e})")
        return []


def save_facts(facts):
    """Save the list of facts to the local JSON file."""
    try:
        with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2, ensure_ascii=False)
        print(f"💾 Successfully saved {len(facts)} facts to {ARCHIVE_FILE}")
    except IOError as e:
        print(f"❌ Failed to save archive: {e}")


def fetch_fact():
    """Fetch one random useless fact from the API."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        fact_text = data.get("text", "No fact available")
        return fact_text
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def add_new_fact():
    """Main function: Fetch fact → Check duplicate → Save if unique."""
    # Step 1: Load existing facts
    facts = load_facts()

    # Step 2: Fetch a new fact
    new_fact_text = fetch_fact()
    if new_fact_text is None:
        print("⛔ Could not fetch a fact this time.")
        return

    # Step 3: Check for duplicate (crucial requirement)
    # Using set for fast lookup
    existing_facts = {fact["text"] for fact in facts}
    
    if new_fact_text in existing_facts:
        print("🔄 This fact already exists in the archive. Not added.")
        print(f"   → {new_fact_text}")
        return

    # Step 4: Add the new unique fact and save
    facts.append({"text": new_fact_text})
    save_facts(facts)

    print("🎉 New unique fact successfully added to archive!")
    print(f"   → {new_fact_text}")


# Optional: View all stored facts
def view_archive():
    """Display all facts currently in the archive."""
    facts = load_facts()
    if not facts:
        print("🪹 The archive is currently empty.")
        return
    
    print(f"\n📖 Useless Facts Archive — {len(facts)} facts total:")
    for i, fact in enumerate(facts, 1):
        print(f"{i:3d}. {fact['text']}")


# =============================================
# Main Execution
# =============================================
if __name__ == "__main__":
    print("🧠 Useless Facts Knowledge Base Builder")
    print("=" * 55)
    
    add_new_fact()
    
    # Uncomment the line below if you want to see the full archive after adding:
    # view_archive()
