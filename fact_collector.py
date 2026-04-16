import json
import os
import time
import requests

# =============================================
# DESIGN DECISIONS
# =============================================
# Data Structure: List of dictionaries
#   [{"text": "The fact goes here"}, ...]
#
# Storage Format: JSON file (useless_facts_archive.json)

ARCHIVE_FILE = "useless_facts_archive.json"


def load_facts():
    """Load existing facts from the local JSON file."""
    if not os.path.exists(ARCHIVE_FILE):
        print(f"📂 No archive found. Will create '{ARCHIVE_FILE}' on first save.")
        return []
    
    try:
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            facts = json.load(f)
        print(f"✅ Loaded {len(facts)} facts from archive.")
        return facts
    except Exception as e:
        print(f"⚠️ Error loading archive: {e}. Starting fresh.")
        return []


def save_facts(facts):
    """Save the list of facts to the local JSON file."""
    try:
        with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2, ensure_ascii=False)
        print(f"💾 Archive saved successfully — now contains {len(facts)} unique facts.")
    except Exception as e:
        print(f"❌ Failed to save archive: {e}")


def fetch_fact():
    """Fetch one random useless fact from the API (using current v2 endpoint)."""
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # v2 returns "fact" key instead of "text"
        return data.get("fact", data.get("text", "No fact available"))
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def add_new_fact():
    """Fetch a fact, check if it already exists, and save only if unique."""
    facts = load_facts()
    new_fact_text = fetch_fact()

    if new_fact_text is None:
        print("⛔ Could not fetch a fact this time.")
        return

    # Duplicate check (fast set lookup)
    existing_texts = {fact["text"] for fact in facts}

    if new_fact_text in existing_texts:
        print("🔄 Duplicate fact detected — skipping.")
        print(f"   → {new_fact_text[:100]}{'...' if len(new_fact_text) > 100 else ''}")
        return

    # Add the new unique fact
    facts.append({"text": new_fact_text})
    save_facts(facts)

    print("🎉 New unique fact added to the archive!")
    print(f"   → {new_fact_text}")


# =============================================
# AUTOMATION (as explicitly suggested)
# =============================================
if __name__ == "__main__":
    print("🚀 Useless Facts Continuous Collector")
    print("   Fetching every 60 seconds (only unique facts are saved)")
    print("   Press Ctrl + C to stop.\n")

    try:
        while True:
            add_new_fact()
            print("⏳ Waiting 60 seconds before next fetch...\n")
            time.sleep(60)   # Change to 300 for 5 minutes, 3600 for 1 hour, etc.

    except KeyboardInterrupt:
        print("\n\n👋 Collector stopped. Your archive has been saved safely.")
    except Exception as e:
        print(f"\n❌ Unexpected error in collector: {e}")
