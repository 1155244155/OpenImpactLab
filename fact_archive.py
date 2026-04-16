import json
import os
import requests

# === DESIGN CHOICES ===
# Data structure: List of dictionaries
#   Example: [{"text": "Banging your head against a wall burns 150 calories an hour."}, ...]
#   Why? Simple, extensible (easy to add fields like "date_added" later), and matches the
#        suggestion in the query. Each fact is stored exactly as returned by the API.
#
# Storage format: JSON file ("useless_facts_archive.json")
#   Why? Human-readable, preserves order, handles Unicode facts perfectly, no extra
#        dependencies beyond the Python standard library (json + os). JSON is also
#        easy to version-control or share if you ever want to move the archive.
#
# Core logic:
#   - load_facts() returns the list (or empty list if file missing/corrupt)
#   - save_facts() writes the list back to disk
#   - Duplicate check uses a set comprehension for O(1) lookup speed (critical even
#     when the archive grows to thousands of facts)
#   - The original fetch logic from fetch_fact.py is reused exactly, wrapped in a
#     reusable function.

def load_facts(filename="useless_facts_archive.json"):
    """Load existing facts from the local JSON archive."""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                facts = json.load(f)
            print(f"✅ Loaded {len(facts)} facts from archive '{filename}'.")
            return facts
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Corrupt or unreadable archive. Starting fresh. Error: {e}")
            return []
    else:
        print(f"📂 No archive found yet. Will create '{filename}' on first save.")
        return []


def save_facts(facts, filename="useless_facts_archive.json"):
    """Save the list of facts to the local JSON archive."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2, ensure_ascii=False)
        print(f"💾 Archive successfully saved ({len(facts)} facts total).")
    except IOError as e:
        print(f"❌ Failed to save archive: {e}")


def fetch_fact():
    """Fetch one random useless fact (exact logic from the provided fetch_fact.py)."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        fact = data.get("text", "No fact available")
        return fact
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to the API: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def add_fact_if_unique():
    """Main function: fetch → check duplicate → save if new. Builds the persistent knowledge base."""
    # 1. Load current archive
    facts = load_facts()

    # 2. Fetch a new fact
    new_fact_text = fetch_fact()
    if new_fact_text is None:
        print("⛔ Could not fetch a fact. Archive unchanged.")
        return

    # 3. Crucial duplicate check (set for instant lookup)
    existing_texts = {fact_dict["text"] for fact_dict in facts}
    if new_fact_text in existing_texts:
        print("🔄 Duplicate fact detected – not added to archive.")
        print(f"   Fact: {new_fact_text}")
        return

    # 4. Add the new unique fact
    facts.append({"text": new_fact_text})
    save_facts(facts)

    print("🎉 New unique fact added to your persistent knowledge base!")
    print(f"   {new_fact_text}")


# Optional helper to inspect the archive (demonstrates loading)
def view_all_facts():
    """Load and display every fact currently in the archive."""
    facts = load_facts()
    if not facts:
        print("🪹 Archive is empty.")
        return
    print(f"\n📖 Your Useless Facts Archive ({len(facts)} facts):")
    for i, fact_dict in enumerate(facts, 1):
        print(f"{i:3d}. {fact_dict['text']}")


# === RUN THE PROGRAM ===
if __name__ == "__main__":
    print("🧠 Useless Facts Persistent Knowledge Base Builder")
    print("=" * 60)
    add_fact_if_unique()
    # Uncomment the line below anytime to see the full archive:
    # view_all_facts()
