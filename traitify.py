import httplib, urllib, base64, json
class TraitifyException(Exception):
  pass

def check_errors(response):
  if type(response) is dict and response.get("errors") is not None:
    raise TraitifyException(", ".join(response["errors"]))

def get_details(raw_details):
    details = []
    for detail in raw_details:
      details.append(Detail(detail))
    return details

class Deck:
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.attributes = attributes

class Assessment:
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.deck_id = attributes.get("deck_id")
    self.completed_at = attributes.get("completed_at")
    self.created_at = attributes.get("created_at")
    self.attributes = attributes

class Slide:
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.position = attributes.get("position")
    self.image_desktop = attributes.get("image_desktop")
    self.image_desktop_retina = attributes.get("image_desktop_retina")
    self.image_phone_landscape = attributes.get("image_phone_landscape")
    self.image_phone_portrait = attributes.get("image_phone_portrait")
    self.response = attributes.get("response")
    self.time_taken = attributes.get("time_taken")
    self.completed_at = attributes.get("completed_at")
    self.created_at = attributes.get("created_at")
    self.attributes = attributes

class Detail:
  def __init__(self, attributes):
    self.title = attributes.get("title")
    self.body = attributes.get("body")

class PersonalityBlend:
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.personality_type_1 = PersonalityType(attributes.get("personality_type_1"))
    self.personality_type_2 = PersonalityType(attributes.get("personality_type_2"))
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.details = get_details(attributes.get("details"))
    self.attributes = attributes

class PersonalityType:
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.badge = Badge(attributes.get("badge"))
    self.details = get_details(attributes.get("details"))
    self.attributes = attributes

class Badge:
  def __init__(self, attributes):
    self.image_small = attributes.get("image_small")
    self.image_medium = attributes.get("image_medium")
    self.image_large = attributes.get("image_large")
    self.font_color = attributes.get("font_color")
    self.color_1 = attributes.get("color_1")
    self.color_2 = attributes.get("color_2")
    self.color_3 = attributes.get("color_3")
    self.attributes = attributes

class FamousPerson:
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.picture = attributes.get("picture")
    self.attributes = attributes

class PersonalityTraitDichotomoy:
  def __init__(self, attributes):
    self.left_personality_trait = PersonalityTrait(attributes.get("left_personality_trait"))
    self.right_personality_trait = PersonalityTrait(attributes.get("right_personality_trait"))
    self.score = attributes.get("score")
    self.attributes = attributes

class PersonalityTrait:
  def __init__(self, attributes):
    self.name = attributes.get("name")
    self.definition = attributes.get("definition")
    self.description = attributes.get("description")
    self.attributes = attributes

class Traitify:
  def __init__(self, secret_key=None, deck_id=None, host="api-sandbox.traitify.com", version="v1"):
    self.host = host
    self.secret_key = secret_key
    self.deck_id = deck_id
    self.version = version

  def headers(self):
    return { "Accept":"application/json", "Content-Type":"application/json", "Authorization":"Basic " + self.secret_key + ":x" }

  def get(self, path):
    conn = httplib.HTTPSConnection(self.host)
    conn.request("GET", "/" + self.version + path, None, self.headers())
    response = conn.getresponse()
    data = response.read()
    conn.close()
    response = json.loads(data)
    check_errors(response)
    return response

  def post(self, path, arguments):
    conn = httplib.HTTPSConnection(self.host)
    conn.request("POST", "/" + self.version + path, arguments, self.headers())
    response = conn.getresponse()
    data = response.read()
    conn.close()
    response = json.loads(data)
    check_errors(response)
    return response

  def put(self, path, arguments):
    conn = httplib.HTTPSConnection(self.host)
    conn.request("PUT", "/" + self.version + path, arguments, self.headers())
    response = conn.getresponse()
    data = response.read()
    conn.close()
    response = json.loads(data)
    check_errors(response)
    return response

  def get_decks(self):
    data = self.get("/decks")
    decks = []
    for deck in data:
      decks.append(Deck(deck))
    return decks

  def create_assessment(self, deck_id=None):
    if deck_id is None: deck_id = self.deck_id
    data = self.post("/assessments", json.dumps({"deck_id": deck_id}))
    return Assessment(data)

  def get_assessment(self, assessment_id):
    data = self.get("/assessments/" + assessment_id)
    return Assessment(data)

  def get_slides(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/slides")
    slides = []
    for slide in data:
      slides.append(Slide(slide))
    return slides

  def update_slide(self, assessment_id, slide):
    slim_slide = {"response": slide.response, "time_taken": slide.time_taken}
    data = self.put("/assessments/" + assessment_id + "/slides/" + slide.id, json.dumps(slim_slide))
    return Slide(data)

  def update_slides(self, assessment_id, slides):
    slim_slides = []
    for slide in slides:
      slim_slides.append({"id": slide.id, "response": slide.response, "time_taken": slide.time_taken})
    data = self.put("/assessments/" + assessment_id + "/slides", json.dumps(slim_slides))
    slides = []
    for slide in data:
      slides.append(Slide(slide))
    return slides

  def get_personality_types(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/personality_types")
    personality_types = []
    for personality_type in data.get("personality_types"):
      personality_types.append({
        "personality_type": PersonalityType(personality_type.get("personality_type")),
        "score": personality_type.get("score") })
    return { "personality_blend": PersonalityBlend(data.get("personality_blend")), "personality_types": personality_types }

  def get_personality_type_traits(self, assessment_id, personality_type_id):
    data = self.get("/assessments/" + assessment_id + "/personality_types/" + personality_type_id + "/personality_traits")
    personality_traits = []
    for personality_trait in data:
      personality_traits.append({
        "personality_trait": PersonalityTrait(personality_trait.get("personality_trait")),
        "score": personality_trait.get("score") })
    return personality_traits

  def get_personality_traits(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/personality_traits")
    personality_traits = []
    for personality_trait in data:
      personality_traits.append(PersonalityTraitDichotomoy(personality_trait))
    return personality_traits

  def get_personality_traits_raw(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/personality_traits/raw")
    personality_traits = []
    for personality_trait in data:
      personality_traits.append(PersonalityTrait(personality_trait))
    return personality_traits
