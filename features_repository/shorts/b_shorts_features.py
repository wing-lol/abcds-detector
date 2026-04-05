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

"""Module with BRAND (B) feature configurations for Shorts"""

from models import (
    VideoFeature,
    VideoSegment,
    EvaluationMethod,
    VideoFeatureCategory,
    VideoFeatureSubCategory,
)


def get_brand_features() -> list[VideoFeature]:
  """Gets all BRAND (B) ABCD features for Shorts
  
  Returns:
    feature_configs: list of BRAND feature configurations
  """
  feature_configs = [
      VideoFeature(
          id="b_brand_display",
          name="Brand Display",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_early",
          name="Brand Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FIRST_3_SECONDS,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FIRST_3_SECONDS,
      ),
      VideoFeature(
          id="b_brand_late",
          name="Brand Late",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_overlaid",
          name="Brand Overlaid",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_in_situation",
          name="Brand In Situation",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_visual_nonconsecutive",
          name="Brand Visual Non-consecutive",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_large_brand_logo",
          name="Large Brand Logo",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_mention",
          name="Brand Mention",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_mention_early",
          name="Brand Mention Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FIRST_3_SECONDS,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FIRST_3_SECONDS,
      ),
      VideoFeature(
          id="b_brand_mention_late",
          name="Brand Mention Late",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_mention_see_say",
          name="Brand Mention See-Say",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_mention_see_say_early",
          name="Brand Mention See-Say Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FIRST_3_SECONDS,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FIRST_3_SECONDS,
      ),
      VideoFeature(
          id="b_jingle",
          name="Jingle",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_brand_elements",
          name="Brand Elements",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_visualized",
          name="Product Visualized",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_visualized_early",
          name="Product Visualized Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FIRST_3_SECONDS,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FIRST_3_SECONDS,
      ),
      VideoFeature(
          id="b_product_visualized_late",
          name="Product Visualized Late",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_closeup",
          name="Product Closeup",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_extreme_closeup",
          name="Product Extreme Closeup",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_mention_combined",
          name="Product Mention Combined",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_mention_speech",
          name="Product Mention Speech",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_mention_speech_early",
          name="Product Mention Speech Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FIRST_3_SECONDS,
          evaluation_criteria="TODO",
          prompt_template="TODO",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FIRST_3_SECONDS,
      ),
      VideoFeature(
          id="b_product_mention_speech_late",
          name="Product Mention Speech Late",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_mention_text",
          name="Product Mention Text",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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
          id="b_product_focus",
          name="Product Focus",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
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


def get_brand_features() -> list[VideoFeature]:
  """Gets all BRAND (B) ABCD features for Shorts
  
  Returns:
  feature_configs: list of BRAND feature configurations
  """
  feature_configs = [
      # TODO: Add BRAND features here
      # Features to add:
      # - b_brand_display
      # - b_brand_early
      # - b_brand_late
      # - b_brand_overlaid
      # - b_brand_in_situation
      # - b_brand_visual_nonconsecutive
      # - b_large_brand_logo
      # - b_brand_mention
      # - b_brand_mention_early
      # - b_brand_mention_late
      # - b_brand_mention_see_say
      # - b_brand_mention_see_say_early
      # - b_jingle
      # - b_brand_elements
      # - b_product_visualized
      # - b_product_visualized_early
      # - b_product_visualized_late
      # - b_product_closeup
      # - b_product_extreme_closeup
      # - b_product_mention_combined
      # - b_product_mention_speech
      # - b_product_mention_speech_early
      # - b_product_mention_speech_late
      # - b_product_mention_text
      # - b_product_focus
  ]
  
  return feature_configs
