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

