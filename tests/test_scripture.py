from src.core.scripture_service import ScriptureService
import time

print("--- Testing Scripture Service ---")

# Test 1: General Tag (Fallback check + API check)
print("\n1. Fetching 'general' tag...")
start = time.time()
verse = ScriptureService.get_verse("general")
duration = time.time() - start
print(f"Result: {verse.reference} - {verse.text[:30]}...")
print(f"Time taken: {duration:.2f}s")

# Test 2: Specific Tag
print("\n2. Fetching 'peace' tag...")
verse_peace = ScriptureService.get_verse("peace")
print(f"Result: {verse_peace.reference} - {verse_peace.text[:30]}...")

# Test 3: Unknown Tag (Should fallback to general)
print("\n3. Fetching 'unknown_tag'...")
verse_unknown = ScriptureService.get_verse("unknown_xyz")
print(f"Result: {verse_unknown.reference} - {verse_unknown.text[:30]}...")

print("\n--- Test Complete ---")
