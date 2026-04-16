import json
import os
import time
import requests
import schedule   # pip install schedule  (lightweight, no extra dependencies)

# =============================================
# DESIGN (as required)
# =============================================
# Data Structure: List of dictionaries
#   [{"text": "fact here"}, {"text": "another fact"}, ...]
#
# Storage Format: JSON file ("useless_facts_archive.json")

ARCHIVE_FILE = "useless_facts_archive.json"


def load_facts():
    """Load facts from local JSON archive."""
    if not os.path.exists(ARCHIVE_FILE):
        print(f"📂 No archive found. Will create {ARCHIVE_FILE} on first save.")
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
    """Save facts to local JSON archive."""
    try:
        with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2, ensure_ascii=False)
        print(f"💾 Archive saved successfully — now contains {len(facts)} facts.")
    except Exception as e:
        print(f"❌ Failed to save archive: {e}")


def fetch_fact():
    """Fetch one random useless fact from the API."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "No fact available")
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def add_unique_fact():
    """Fetch a fact, check for duplicate, and add it if new."""
    facts = load_facts()
    new_fact_text = fetch_fact()

    if new_fact_text is None:
        print("⛔ Failed to fetch fact this cycle.")
        return

    # Fast duplicate check using set
    existing_texts = {fact["text"] for fact in facts}

    if new_fact_text in existing_texts:
        print("🔄 Duplicate fact detected — skipping.")
        print(f"   → {new_fact_text[:100]}{'...' if len(new_fact_text) > 100 else ''}")
        return

    # Add new unique fact
    facts.append({"text": new_fact_text})
    save_facts(facts)
    print("🎉 New unique fact added!")
    print(f"   → {new_fact_text}")


def view_archive():
    """Optional: Print all facts in the archive."""
    facts = load_facts()
    if not facts:
        print("🪹 Archive is empty.")
        return
    print(f"\n📖 Archive contains {len(facts)} unique facts:")
    for i, fact in enumerate(facts, 1):
        print(f"{i:3d}. {fact['text']}")


# =============================================
# AUTOMATION MECHANISM
# =============================================
def run_continuous_collection():
    """Run the collector in a loop using the 'schedule' library."""
    print("🚀 Starting Useless Facts Continuous Collector")
    print("   Facts will be fetched and added (if unique) every 5 minutes.")
    print("   Press Ctrl+C to stop.\n")

    # Schedule the job — you can change the interval easily
    schedule.every(5).minutes.do(add_unique_fact)
    # Alternative examples:
    # schedule.every().hour.do(add_unique_fact)
    # schedule.every(30).seconds.do(add_unique_fact)   # for testing

    # Initial run immediately
    print("📥 Performing initial fetch...")
    add_unique_fact()

    # Main scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(1)   # Small sleep to keep CPU usage low


# =============================================
# Main Entry Point
# =============================================
if __name__ == "__main__":
    # For quick testing: run once only (uncomment if needed)
    # add_unique_fact()
    # view_archive()

    # For continuous automatic collection (as required)
    try:
        run_continuous_collection()
    except KeyboardInterrupt:
        print("\n\n👋 Collector stopped by user. Archive is safely saved.")
    except Exception as e:
        print(f"\n❌ Unexpected error in collector: {e}")
