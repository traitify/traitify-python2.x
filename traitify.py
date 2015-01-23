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

class TraitifyModel:
  @classmethod
  def from_attr_list(cls, attr_list):
    models = []
    for model in attr_list:
      models.append(cls(model))
    return models

class Deck(TraitifyModel):
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.attributes = attributes

class Assessment(TraitifyModel):
  (personality_blend, personality_types, personality_traits, career_matches) = [None] * 4

  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.deck_id = attributes.get("deck_id")
    self.completed_at = attributes.get("completed_at")
    self.created_at = attributes.get("created_at")
    if attributes.get("personality_blend") != None:
      self.personality_blend = PersonalityBlend(attributes.get("personality_blend"))
    if attributes.get("personality_types") != None:
      self.personality_types = ScoredPersonalityType.from_attr_list(attributes.get("personality_types"))
    if attributes.get("personality_traits") != None:
      self.personality_traits = ScoredPersonalityTrait.from_attr_list(attributes.get("personality_traits"))
    if attributes.get("career_matches") != None:
      self.career_matches = ScoredCareer.from_attr_list(attributes.get("career_matches"))
    self.attributes = attributes

class Slide(TraitifyModel):
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

class Detail(TraitifyModel):
  def __init__(self, attributes):
    self.title = attributes.get("title")
    self.body = attributes.get("body")

class PersonalityBlend(TraitifyModel):
  def __init__(self, attributes):
    self.personality_type_1 = PersonalityType(attributes.get("personality_type_1"))
    self.personality_type_2 = PersonalityType(attributes.get("personality_type_2"))
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.details = get_details(attributes.get("details"))
    self.attributes = attributes

class PersonalityType(TraitifyModel):
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.badge = Badge(attributes.get("badge"))
    self.details = get_details(attributes.get("details"))
    self.attributes = attributes

class ScoredPersonalityType(TraitifyModel):
  def __init__(self, attributes):
    self.personality_type = PersonalityType(attributes.get("personality_type"))
    self.score = attributes.get("score")

class Badge(TraitifyModel):
  def __init__(self, attributes):
    self.image_small = attributes.get("image_small")
    self.image_medium = attributes.get("image_medium")
    self.image_large = attributes.get("image_large")
    self.font_color = attributes.get("font_color")
    self.color_1 = attributes.get("color_1")
    self.color_2 = attributes.get("color_2")
    self.color_3 = attributes.get("color_3")
    self.attributes = attributes

class FamousPerson(TraitifyModel):
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.description = attributes.get("description")
    self.picture = attributes.get("picture")
    self.attributes = attributes

class PersonalityTraitDichotomoy(TraitifyModel):
  def __init__(self, attributes):
    self.left_personality_trait = PersonalityTrait(attributes.get("left_personality_trait"))
    self.right_personality_trait = PersonalityTrait(attributes.get("right_personality_trait"))
    self.score = attributes.get("score")
    self.attributes = attributes

class PersonalityTrait(TraitifyModel):
  def __init__(self, attributes):
    self.name = attributes.get("name")
    self.definition = attributes.get("definition")
    self.description = attributes.get("description")
    self.attributes = attributes

class ScoredPersonalityTrait(TraitifyModel):
  def __init__(self, attributes):
    self.personality_trait = PersonalityTrait(attributes.get("personality_trait"))
    self.score = attributes.get("score")

class ExperienceLevel(TraitifyModel):
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.name = attributes.get("name")
    self.experience = attributes.get("experience")
    self.job_training = attributes.get("job_training")
    self.examples = attributes.get("examples")
    self.svp_range = attributes.get("svp_range")

class SalaryProjection(TraitifyModel):
  def __init__(self, attributes):
    self.source = attributes.get("source")
    self.total_employees = attributes.get("total_employees")
    self.hourly_rate_10_percentile = attributes.get("hourly_rate_10_percentile")
    self.hourly_rate_25_percentile = attributes.get("hourly_rate_25_percentile")
    self.hourly_rate_75_percentile = attributes.get("hourly_rate_75_percentile")
    self.hourly_rate_90_percentile = attributes.get("hourly_rate_90_percentile")
    self.hourly_rate_median = attributes.get("hourly_rate_median")
    self.hourly_rate_mean = attributes.get("hourly_rate_mean")
    self.annual_salary_10_percentile = attributes.get("annual_salary_10_percentile")
    self.annual_salary_25_percentile = attributes.get("annual_salary_25_percentile")
    self.annual_salary_75_percentile = attributes.get("annual_salary_75_percentile")
    self.annual_salary_90_percentile = attributes.get("annual_salary_90_percentile")
    self.annual_salary_median = attributes.get("annual_salary_median")
    self.annual_salary_mean = attributes.get("annual_salary_mean")

class EmploymentProjection(TraitifyModel):
  def __init__(self, attributes):
    self.source = attributes.get("source")
    self.annual_salary_median_2012 = attributes.get("annual_salary_median_2012")
    self.total_employees_2012 = attributes.get("total_employees_2012")
    self.total_employees_2022 = attributes.get("total_employees_2022")
    self.new_openings_2022 = attributes.get("new_openings_2022")
    self.new_openings_and_replacement_2022 = attributes.get("new_openings_and_replacement_2022")
    self.percent_growth_2022 = attributes.get("percent_growth_2022")

class Major(TraitifyModel):
  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.title = attributes.get("title")
    self.description = attributes.get("description")
    self.group_id = attributes.get("group_id")

class Career(TraitifyModel):
  (majors, experience_level, salary_projection, employment_projection) = [None] * 4

  def __init__(self, attributes):
    self.id = attributes.get("id")
    self.title = attributes.get("title")
    self.description = attributes.get("description")
    if attributes.get("majors"):
      self.majors = Major.from_attr_list(attributes.get("majors"))
    if attributes.get("experience_level"):
      self.experience_level = ExperienceLevel(attributes.get("experience_level"))
    if attributes.get("salary_projection"):
      self.salary_projection = SalaryProjection(attributes.get("salary_projection"))
    if attributes.get("employment_projection"):
      self.employment_projection = EmploymentProjection(attributes.get("employment_projection"))
    self.bright_outlooks = attributes.get("bright_outlooks")
    self.attributes = attributes

class ScoredCareer(TraitifyModel):
  def __init__(self, attributes):
    self.career = Career(attributes.get("career"))
    self.score = attributes.get("score")

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
    return Deck.from_attr_list(data)

  def create_assessment(self, deck_id=None):
    if deck_id is None: deck_id = self.deck_id
    data = self.post("/assessments", json.dumps({"deck_id": deck_id}))
    return Assessment(data)

  def get_assessment(self, assessment_id):
    data = self.get("/assessments/" + assessment_id)
    return Assessment(data)

  def get_slides(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/slides")
    return Slide.from_attr_list(data)

  def update_slide(self, assessment_id, slide):
    slim_slide = {"response": slide.response, "time_taken": slide.time_taken}
    data = self.put("/assessments/" + assessment_id + "/slides/" + slide.id, json.dumps(slim_slide))
    return Slide(data)

  def update_slides(self, assessment_id, slides):
    slim_slides = []
    for slide in slides:
      slim_slides.append({"id": slide.id, "response": slide.response, "time_taken": slide.time_taken})
    data = self.put("/assessments/" + assessment_id + "/slides", json.dumps(slim_slides))
    return Slide.from_attr_list(data)

  def get_personality_types(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/personality_types")
    return { "personality_blend": PersonalityBlend(data.get("personality_blend")), "personality_types": ScoredPersonalityType.from_attr_list(data.get("personality_types")) }

  def get_personality_type_traits(self, assessment_id, personality_type_id):
    data = self.get("/assessments/" + assessment_id + "/personality_types/" + personality_type_id + "/personality_traits")
    return ScoredPersonalityTrait.from_attr_list(data)

  def get_personality_traits(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/personality_traits")
    return PersonalityTraitDichotomoy.from_attr_list(data)

  def get_personality_traits_raw(self, assessment_id):
    data = self.get("/assessments/" + assessment_id + "/personality_traits/raw")
    return ScoredPersonalityTrait.from_attr_list(data)

  def career_matches(self, assessment_id, number_of_matches = None, experience_levels = None):
    query_params = "?x=1"
    if number_of_matches != None:
      query_params += "&number_of_matches=" + str(number_of_matches)
    if experience_levels != None:
      query_params += "&experience_levels=" + ",".join(str(x) for x in experience_levels)
    data = self.get("/assessments/" + assessment_id + "/matches/careers" + query_params)
    return ScoredCareer.from_attr_list(data)

  # data is an array of data you want returned, can be any combination of "blend", "types", "traits", "career_matches"
  def results(self, assessment_id, data = [], image_pack = None, number_of_matches = None, experience_levels = None):
    query_params = "?data=" + ",".join(data)
    if image_pack != None:
      query_params += "&image_pack=" + image_pack
    if number_of_matches != None:
      query_params += "&number_of_matches=" + str(number_of_matches)
    if experience_levels != None:
      query_params += "&experience_levels=" + ",".join(str(x) for x in experience_levels)
    data = self.get("/assessments/" + assessment_id + query_params)
    return Assessment(data)