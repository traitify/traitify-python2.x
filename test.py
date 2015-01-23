#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import unittest
from traitify import Traitify

class TraitifyTest(unittest.TestCase):
  traitify = "Needs setup"
  assessment = None

  def setUp(self):
    self.assessment = self.traitify.create_assessment('career-deck')

  def complete_assessment(self):
    slides = self.traitify.get_slides(self.assessment.id)
    for slide in slides:
      slide.response = True
      slide.time_taken = 200
    slides = self.traitify.update_slides(self.assessment.id, slides)
    return self

  def test_decks(self):
    # Get the decks
    decks = self.traitify.get_decks()

    self.assertTrue(len(decks) > 0)

  def test_create_assessment(self):
    assessment = self.traitify.create_assessment('core')
    self.assertTrue(assessment.deck_id == "core")
    assessment = self.traitify.create_assessment('career-deck')
    self.assertTrue(assessment.deck_id == "career-deck")

  def test_get_assessment(self):
    self.assertTrue(self.traitify.get_assessment(self.assessment.id).id != None)

  def test_get_slides(self):
    slides = self.traitify.get_slides(self.assessment.id)
    self.assertTrue(len(slides) > 0)

  def test_update_slide(self):
    slides = self.traitify.get_slides(self.assessment.id)
    slide = slides[0]
    slide.response = True
    slide.time_taken = 200
    slide = self.traitify.update_slide(self.assessment.id, slide)

    self.assertTrue(slide.time_taken == 200)
    self.assertTrue(slide.response)

  def test_bulk_update_slides(self):
    slides = self.traitify.get_slides(self.assessment.id)
    for slide in slides:
      slide.response = True
      slide.time_taken = 200
    slides = self.traitify.update_slides(self.assessment.id, slides)

    for slide in slides:
      self.assertTrue(slide.time_taken == 200)
      self.assertTrue(slide.response)

  def test_get_personality_types_and_personality_blends(self):
    self.complete_assessment()
    results = self.traitify.get_personality_types(self.assessment.id)

    self.assertTrue(results["personality_types"][0].personality_type.name != None)
    self.assertTrue(results["personality_blend"].name != None)

  def test_get_personality_traits(self):
    self.complete_assessment()
    traits = self.traitify.get_personality_traits(self.assessment.id)

    self.assertTrue(traits[0].left_personality_trait.name != None)
    self.assertTrue(traits[0].right_personality_trait.name != None)

  def test_get_personality_traits_raw(self):
    self.complete_assessment()
    traits = self.traitify.get_personality_traits_raw(self.assessment.id)

    self.assertTrue(traits[0].personality_trait.name != None)
    self.assertTrue(traits[0].score > 0)

  def test_career_matches(self):
    self.complete_assessment()
    scored_careers = self.traitify.career_matches(self.assessment.id)

    self.assertTrue(scored_careers[0].career.title != None)
    self.assertTrue(scored_careers[0].score > 0)

  def test_career_matches_with_limit(self):
    self.complete_assessment()
    scored_careers = self.traitify.career_matches(self.assessment.id, 1)

    self.assertTrue(len(scored_careers) == 1)

  def test_career_matches_filtered_by_experience_level(self):
    self.complete_assessment()
    scored_careers = self.traitify.career_matches(self.assessment.id, 10, [5])

    for scored_career in scored_careers:
      if scored_career.career.experience_level != None:
        self.assertTrue(scored_career.career.experience_level.id == 5)

  def test_default_results(self):
    self.complete_assessment()
    results = self.traitify.results(self.assessment.id)

    self.assertTrue(results.id != None)
    self.assertTrue(results.personality_blend == None)
    self.assertTrue(results.personality_types == None)
    self.assertTrue(results.personality_traits == None)

  def test_results_with_traits_and_types(self):
    self.complete_assessment()
    results = self.traitify.results(self.assessment.id, ["traits", "types"])

    self.assertTrue(results.id != None)
    self.assertTrue(results.personality_blend == None)
    self.assertTrue(results.personality_types != None)
    self.assertTrue(results.personality_traits != None)

if len(sys.argv) is 1:
  print "Please pass in your Traitify app's secret key as an argument. If you don't have a Traitify account, please sign up at https://developer.traitify.com."
else:
  TraitifyTest.traitify = Traitify(sys.argv.pop())

  suite = unittest.TestLoader().loadTestsFromTestCase(TraitifyTest)
  unittest.TextTestRunner(verbosity=1).run(suite)