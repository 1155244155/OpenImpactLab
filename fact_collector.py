import json
import os
import time
import requests

# =============================================
# DESIGN (as required)
# =============================================
# Data Structure: List of dictionaries
#   Example: [{"text": "Banging your head against a wall burns 150 calories an hour."}, ...]
#
# Storage Format: JSON ("useless_facts_archive.json")

ARCHIVE_FILE = "useless_facts_archive.json"


def load_facts():
    """Load existing facts from the local JSON archive."""
    if not os.path.exists(ARCHIVE_FILE):
        print(f"📂 No archive found yet. Will create '{ARCHIVE_FILE}' automatically.")
        return []
    
    try:
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            facts = json.load(f)
        print(f"✅ Loaded {len(facts)} facts from archive.")
        return facts
    except Exception as e:
        print(f"⚠️ Error loading archive ({e}). Starting fresh.")
        return []


def save_facts(facts):
    """Save the updated list of facts back to the JSON archive."""
    try:
        with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2, ensure_ascii=False)
        print(f"💾 Archive saved — now contains {len(facts)} unique facts.")
    except Exception as e:
        print(f"❌ Failed to save archive: {e}")


def fetch_fact():
    """Fetch one random useless fact from the API (updated to v2 endpoint for reliability)."""
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "No fact available")
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def add_unique_fact():
    """Fetch a fact, check for duplicate, and add only if it's new."""
    facts = load_facts()
    new_fact_text = fetch_fact()

    if new_fact_text is None:
        print("⛔ Could not fetch a fact this time.")
        return

    # Fast duplicate detection
    existing_texts = {fact["text"] for fact in facts}

    if new_fact_text in existing_texts:
        print("🔄 Duplicate fact detected — skipping this cycle.")
        print(f"   → {new_fact_text[:120]}{'...' if len(new_fact_text) > 120 else ''}")
        return

    # Add the new unique fact
    facts.append({"text": new_fact_text})
    save_facts(facts)

    print("🎉 New unique fact successfully added to the archive!")
    print(f"   → {new_fact_text}")


# =============================================
# AUTOMATION (as required by the feedback)
# =============================================
if __name__ == "__main__":
    print("🚀 Useless Facts Continuous Collector Started")
    print("   Fetching a new fact every 60 seconds (only unique ones are saved)")
    print("   Press Ctrl + C to stop the collector.\n")

    try:
        while True:
            add_unique_fact()
            print(f"⏳ Waiting 60 seconds before next fetch...\n")
            time.sleep(60)   # Change to 300 for 5 minutes, 3600 for 1 hour, etc.

    except KeyboardInterrupt:
        print("\n\n👋 Collector stopped by user. Your archive is safely saved on disk.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
