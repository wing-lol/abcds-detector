#!/usr/bin/env python3

###########################################################################
#
#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

"""Module with DIRECT (D) feature configurations for Shorts"""

from models import (
    VideoFeature,
    VideoSegment,
    EvaluationMethod,
    VideoFeatureCategory,
    VideoFeatureSubCategory,
)


def get_direct_features() -> list[VideoFeature]:
  """Gets all DIRECT (D) ABCD features for Shorts
  
  Returns:
    feature_configs: list of DIRECT feature configurations
  """
  feature_configs = [
      VideoFeature(
          id="d_call_to_action_supers",
          name="Call to Action Supers",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_audio_cta",
          name="Audio Call to Action",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_free_text",
          name="Free Text",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_free_speech",
          name="Free Speech",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_path_to_purchase",
          name="Path to Purchase",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_search_bar",
          name="Search Bar",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_relevant_call_to_action",
          name="Relevant Call to Action",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_purchase_incentive",
          name="Purchase Incentive",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_special_offer_text",
          name="Special Offer Text",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_special_offer_speech",
          name="Special Offer Speech",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_price_text",
          name="Price Text",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_price_speech",
          name="Price Speech",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]

  return feature_configs


def get_direct_features() -> list[VideoFeature]:
  """Gets all DIRECT (D) ABCD features for Shorts
  
  Returns:
  feature_configs: list of DIRECT feature configurations
  """
  feature_configs = [
      # TODO: Add DIRECT features here
      # Features to add:
      # - d_call_to_action_supers
      # - d_audio_cta
      # - d_free_text
      # - d_free_speech
      # - d_path_to_purchase
      # - d_search_bar
      # - d_relevant_call_to_action
      # - d_purchase_incentive
      # - d_special_offer_text
      # - d_special_offer_speech
      # - d_price_text
      # - d_price_speech
  ]
  
  return feature_configs
