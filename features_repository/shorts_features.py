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

"""Module with the supported ABCD feature configurations for Shorts"""


from models import (
    VideoFeature,
    VideoSegment,
    EvaluationMethod,
    VideoFeatureCategory,
    VideoFeatureSubCategory,
)


def get_shorts_feature_configs() -> list[VideoFeature]:
  """Gets all the supported ABCD/Shorts features
  
  Returns original shorts features PLUS new organized ABCD features
  (Attract, Brand, Connect, Direct, Other)
  
  Returns:
    feature_configs: list of feature configurations
  """
  # Get original shorts features
  feature_configs = [
      
      
    VideoFeature(
          id="shorts_product_context",
          name="Product Context",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                Product/service is shown being actively used or interacted with by a person
                in a realistic context that mirrors how potential users would encounter it.
                Includes: holding, using, consuming, or interacting with the product/service
                to demonstrate practical value rather than presenting it as a promotional showcase.
                """,
          prompt_template="""
                Evaluate: Is the product/service actively USED/INTERACTED with in a realistic context?

                BRAND/PRODUCT CONTEXT:
                Brand: {brand}
                Product: {product}
                Industry: {vertical}

                VIDEO METADATA:
                {metadata_summary}

                SCORE ON TWO DIMENSIONS (each 0-100):

                1. INTERACTION PRESENCE (60% of overall score)
                   - Is someone actually USING/INTERACTING with the product?
                   - Examples that COUNT:
                     ✓ Person holding product, person using/consuming it, service interaction, app usage
                     ✗ Product shown on table, product in background, voiceover describing features

                   Measure:
                   - Interaction visible? (yes/no)
                   - Total seconds of visible use (if yes)
                   - Type: physical|consumption|operational|service|digital
                   
                   Score:
                   - 90-100: Clear, extended use (5+ seconds), obvious purpose
                   - 70-89: Visible use (2-5 seconds), somewhat clear
                   - 50-69: Brief use visible (<2 seconds), unclear
                   - 0-49: No genuine use shown

                2. CONTEXT AUTHENTICITY (40% of overall score)
                   - Is the usage scenario realistic, not promotional?
                   - Real-world setting (home, street, café, workplace)?
                   - Natural user behavior or staged/scripted?

                   Score:
                   - 90-100: Real-world setting, natural behavior, relatable scenario
                   - 70-89: Mostly authentic setting, some natural behavior
                   - 50-69: Mixed/ambiguous setting or behavior
                   - 0-49: Clearly staged/studio, artificial/promotional feel

                FINAL CALCULATION:
                Overall Score = (Interaction Score × 0.6) + (Authenticity Score × 0.4)

                FORMAT RESPONSE AS JSON:
                {{
                    "detected": boolean,
                    "confidence_score": float,
                    "evaluation": {{
                        "interaction_analysis": {{
                            "use_visible": boolean,
                            "use_type": str,
                            "duration_seconds": float,
                            "interaction_score": int,
                            "key_moments": str
                        }},
                        "context_analysis": {{
                            "setting_type": str,
                            "behavior_authenticity": str,
                            "context_score": int,
                            "realism_description": str
                        }},
                        "final_score": {{
                            "interaction_score": int,
                            "context_score": int,
                            "weighted_overall": float
                        }}
                    }}
                }}

                EXAMPLES - HIGH SCORE (80+):
                - Person drinks from coffee cup in morning routine
                - User opens phone app and uses it
                - Person applies skincare product on face

                EXAMPLES - MEDIUM SCORE (50-79):
                - Product briefly shown being held with unclear use
                - Use visible but in somewhat staged setting
                - Clear use but very short duration

                EXAMPLES - LOW SCORE (<50):
                - Product shown on shelf with no interaction
                - Voiceover describes features, no usage shown
                - Product held briefly for branding only
                - Studio product showcase with no use demonstration
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
    ),
    
    VideoFeature(
        id="relevant_call_to_action",
        name="Relevant Call-To-Action",
        category=VideoFeatureCategory.SHORTS,
        sub_category=VideoFeatureSubCategory.NONE,
        video_segment=VideoSegment.FULL_VIDEO,
        evaluation_criteria="""
            A 'Call To Action' phrase is heard or mentioned in the audio or speech at any time in the video.
        """,
        prompt_template="""
            Is any call to action heard or mentioned in the speech of the video?
        """,
        extra_instructions=[
            "Consider the following criteria for your answer: {criteria}",
            "Some examples of call to actions are: {call_to_actions}",
            (
                "Provide the exact timestamp when the call to actions are"
                " heard or mentioned in the speech of the video."
            ),
        ],
        evaluation_method=EvaluationMethod.LLMS,
        evaluation_function="",
        include_in_evaluation=True,
        group_by=VideoSegment.FULL_VIDEO,
    ),
    
    VideoFeature(
        id="call_to_action_text",
        name="Call To Action (Text)",
        category=VideoFeatureCategory.SHORTS,
        sub_category=VideoFeatureSubCategory.NONE,
        video_segment=VideoSegment.FULL_VIDEO,
        evaluation_criteria="""
            A 'Call To Action' phrase is detected in the video supers (overlaid text) at any time in the video.
        """,
        prompt_template="""
            Is any call to action detected in any text overlay at any time in the video?
        """,
        extra_instructions=[
            "Consider the following criteria for your answer: {criteria}",
            "Some examples of call to actions are: {call_to_actions}",
            (
                "Look through each frame in the video carefully and answer"
                " the question."
            ),
            (
                "Provide the exact timestamp when the call to action is"
                " detected in any text overlay in the video."
            ),
        ],
        evaluation_method=EvaluationMethod.LLMS,
        evaluation_function="",
        include_in_evaluation=True,
        group_by=VideoSegment.FULL_VIDEO,
    )
    

  ]
  
  return feature_configs