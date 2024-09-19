## Issue Description

The `generate_story_part` function is not returning the expected values. Specifically:

- **`SUMMARY`** is correctly displayed as `None`.
- **`GENRE`** is unexpectedly empty or malformed.
- **`TOPIC`** displays as `sci-fi`, which is correct.
- **`KEY WORDS`** is displayed as `None` instead of the expected list of keywords.

### Code
```python
def generate_story_part(
        genre="sci-fi",
        topic="colors in spanish",
        keywords="[\"aliens\", \"moon\"]",  # Note: This should be a list, not a string
        choice=None,
        story_part=0,
        length_of_story=10,
        story_summary=None,
):
    print(f"SUMMARY: {story_summary}")
    print(f"GENRE: {genre}")
    print(f"TOPIC: {topic}")
    print(f"KEY WORDS: {keywords}")
    print("\n\n")
```

### CURL

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"genre\": \"sci-fi\", \"topic\
": \"colors in spanish\", \"keywords\": [\"aliens\", \"moon\"], \"choice\": null, \"story_part\": 0, \"length_of_story\": 10, \"story_summary\": null}" "http://localhost:5000/generate-story"
```

### Correct output
```bash
SUMMARY: None
GENRE: sci-fi
TOPIC: colors in spanish
KEY WORDS: ["aliens", "moon"]
```

### Actual output
```bash
SUMMARY: None
GENRE: 
        Be
    
TOPIC: sci-fi
KEY WORDS: None

```
