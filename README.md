Traitify  Python 2.x
==================

```
# Import traitify
from traitify import Traitify

# Initialize and Authenticate
secret_key = "Your Secret Key"
traitify = Traitify(secret_key)

# Get the decks
decks = traitify.get_decks()

# Set deck key
traitify.deck_key = decks[0].key

# Create an assessment
assessment = traitify.create_assessment()

# Get an assessment
assessment = traitify.get_assessment(assessment.id)

# Get an assessment's slides
slides = traitify.get_slides(assessment.id)

# Upate a slide
slide = slides[0]
slide.response = True
slide.time_taken = 200
slide = traitify.update_slide(assessment.id, slide)

# Bulk update slides
for slide in slides:
  slide.response = True
  slide.time_taken = 200
slides = traitify.update_slides(assessment.id, slides)

# Get an assessment's results (personality types)
personality_types = traitify.get_personality_types(assessment.id)

# Get an assessment's results (personality type traits)
personality_type = personality_types["personality_types"][0]["personality_type"]
personality_traits = traitify.get_personality_type_traits(assessment.id, personality_type.id)

# Get an assessment's results (personality traits)
personality_traits = traitify.get_personality_traits(assessment.id)
```
