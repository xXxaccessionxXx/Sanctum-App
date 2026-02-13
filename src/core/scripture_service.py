import requests
import random
from src.core.covenant import Scripture

class ScriptureService:
    BASE_URL = "https://bible-api.com"

    # Fallback verses in case API fails or offline
    FALLBACK_VERSES = {
        "peace": [
            Scripture("Peace I leave with you; my peace I give to you.", "John 14:27"),
            Scripture("Blessed are the peacemakers, for they shall be called sons of God.", "Matthew 5:9"),
        ],
        "patience": [
            Scripture("Be still before the Lord and wait patiently for him.", "Psalm 37:7"),
            Scripture("Rejoice in hope, be patient in tribulation, be constant in prayer.", "Romans 12:12"),
        ],
        "love": [
            Scripture("Love is patient and kind; love does not envy or boast.", "1 Corinthians 13:4"),
            Scripture("Let all that you do be done in love.", "1 Corinthians 16:14"),
        ],
        "strength": [
            Scripture("I can do all things through him who strengthens me.", "Philippians 4:13"),
            Scripture("The Lord is my strength and my shield.", "Psalm 28:7"),
        ],
        "purity": [
            Scripture("Blessed are the pure in heart, for they shall see God.", "Matthew 5:8"),
            Scripture("Flee from sexual immorality. Every other sin a person commits is outside the body, but the sexually immoral person sins against his own body.", "1 Corinthians 6:18"),
        ],
         "humility": [
            Scripture("God opposes the proud but gives grace to the humble.", "James 4:6"),
            Scripture("Humble yourselves before the Lord, and he will exalt you.", "James 4:10"),
        ],
        "diligence": [
            Scripture("Whatever you do, work at it with all your heart, as working for the Lord, not for human masters.", "Colossians 3:23"),
            Scripture("The soul of the sluggard craves and gets nothing, while the soul of the diligent is richly supplied.", "Proverbs 13:4"),
        ],
        "contentment": [
            Scripture("But godliness with contentment is great gain.", "1 Timothy 6:6"),
            Scripture("Keep your life free from love of money, and be content with what you have, for he has said, 'I will never leave you nor forsake you.'", "Hebrews 13:5"),
        ],
        "temperance": [
            Scripture("Man shall not live by bread alone, but by every word that comes from the mouth of God.", "Matthew 4:4"),
            Scripture("Do not join those who drink too much wine or gorge themselves on meat, for drunkards and gluttons become poor.", "Proverbs 23:20-21"),
        ],
        "morning": [
            Scripture("This is the day that the Lord has made; let us rejoice and be glad in it.", "Psalm 118:24"),
            Scripture("Satisfy us in the morning with your steadfast love, that we may rejoice and be glad all our days.", "Psalm 90:14"),
             Scripture("Let me hear in the morning of your steadfast love, for in you I trust.", "Psalm 143:8"),
        ],
        "evening": [
            Scripture("In peace I will both lie down and sleep; for you alone, O Lord, make me dwell in safety.", "Psalm 4:8"),
            Scripture("The Lord is my light and my salvation; whom shall I fear?", "Psalm 27:1"),
             Scripture("I remember you upon my bed, and meditate on you in the watches of the night.", "Psalm 63:6"),
        ],
        "midday": [
             Scripture("The Lord is my shepherd; I shall not want.", "Psalm 23:1"),
             Scripture("Cast your burden on the Lord, and he will sustain you.", "Psalm 55:22"),
        ],
         "general": [
            Scripture("For God so loved the world, that he gave his only Son.", "John 3:16"),
            Scripture("Trust in the Lord with all your heart.", "Proverbs 3:5"),
        ]
    }

    @staticmethod
    def get_verse(tag: str = "general") -> Scripture:
        """
        Fetches a random verse based on a tag (keyword).
        Returns a Scripture object.
        """
        # 1. Fallback / Seed Data
        # We use this as the primary "Selector" of references for now
        # to ensure the verses are actually relevant to the topic.
        # Ideally, we would have a large database of tagged references.
        options = ScriptureService.FALLBACK_VERSES.get(tag, ScriptureService.FALLBACK_VERSES["general"])
        
        # Default if tag completely unknown
        if not options:
             options = ScriptureService.FALLBACK_VERSES["general"]
             
        selected_scripture = random.choice(options)

        # 2. Try to fetch fresh text from API (Optional but nice for formatting)
        # API: bible-api.com/REFERENCE
        try:
            # Clean reference for URL (e.g., "John 3:16" -> "John+3:16")
            ref_url = selected_scripture.reference.replace(" ", "+")
            url = f"{ScriptureService.BASE_URL}/{ref_url}"
            
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                text = data.get("text", "").strip()
                if text:
                    # Update text with API version (usually WEB or KJV by default on this API)
                    # We can keep the reference as is.
                     return Scripture(text, selected_scripture.reference)
        except Exception as e:
            # Silently fail back to hardcoded text
            print(f"API Error for {selected_scripture.reference}: {e}")

        return selected_scripture

    @staticmethod
    def get_smart_verse(base_tag: str = "general") -> Scripture:
        """
        Intelligently selects a verse based on time of day and context.
        If base_tag is specific (not 'general'), it prioritizes that tag but may occasionaly inject a time-based verse.
        """
        import datetime
        
        current_hour = datetime.datetime.now().hour
        time_tag = "general"
        
        if 5 <= current_hour < 12:
            time_tag = "morning"
        elif 12 <= current_hour < 18:
            time_tag = "midday"
        elif 18 <= current_hour <= 23 or 0 <= current_hour < 5:
            time_tag = "evening"
            
        # Decision Logic:
        # 1. If base_tag is specific (e.g. "temperance"), use it 70% of the time, time-based 30%
        # 2. If base_tag is "general", use time-based 80% of the time.
        
        should_use_time = False
        if base_tag == "general":
            should_use_time = random.random() < 0.8
        else:
            should_use_time = random.random() < 0.3
            
        final_tag = time_tag if should_use_time else base_tag
        
        # If we selected a time tag that doesn't exist (safety), fall back to base
        if final_tag not in ScriptureService.FALLBACK_VERSES:
            final_tag = base_tag
            
        return ScriptureService.get_verse(final_tag)

