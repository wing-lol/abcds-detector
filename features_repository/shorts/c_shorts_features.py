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

"""Module with CONNECT (C) feature configurations for Shorts"""

from models import (
    VideoFeature,
    VideoSegment,
    EvaluationMethod,
    VideoFeatureCategory,
    VideoFeatureSubCategory,
)


def get_connect_features() -> list[VideoFeature]:
  """Gets all CONNECT (C) ABCD features for Shorts
  
  Returns:
    feature_configs: list of CONNECT feature configurations
  """
  feature_configs = [
      VideoFeature(
          id="c_people_overall",
          name="People Detected (Overall)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if there are any people (humans, characters, or on-camera talent) 
                    visible in the video at any time.
                """,
          prompt_template="""
                    Analyze if the video contains any people (humans, characters, on-camera talent).

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PEOPLE PRESENCE:
                    
                    DEFINING PEOPLE:
                    1. ON-CAMERA TALENT:
                        - Visible people/actors
                        - Presenters or hosts
                        - Real people shown
                    
                    2. CHARACTERS:
                        - Animated characters
                        - Mascots or brand characters
                        - People representations

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "people_present": boolean,
                            "people_type": str,
                            "frequency": int,
                            "screen_time_percentage": float
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): People visible in video
                    - NOT DETECTED (false): No people visible

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, prominent people throughout
                    - 0.7-0.8: Good people visibility
                    - 0.5-0.6: Some people visible
                    - 0.3-0.4: Minimum people visibility
                    - 0.0-0.2: No people detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_people_early",
          name="People Detected (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if there are people visible in the first 3 seconds of the video.
                """,
          prompt_template="""
                    Analyze if people are visible in the first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR PEOPLE

                    DEFINING PEOPLE (same as c_people_overall)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "people_in_first_3s": boolean,
                            "first_appearance_timestamp": float,
                            "people_type": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): People visible in first 3 seconds
                    - NOT DETECTED (false): No people in first 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: People prominent in first 1 second
                    - 0.7-0.8: People visible in first 3 seconds
                    - 0.5-0.6: People visible near end of first 3 seconds
                    - 0.3-0.4: Minimal people visibility
                    - 0.0-0.2: No people in first 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_early_faces",
          name="Face (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if faces are featured (visible and identifiable) in the first 3 seconds.
                """,
          prompt_template="""
                    Analyze if faces are featured in the first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR FEATURED FACES

                    DEFINING FEATURED FACES:
                    1. FACE VISIBILITY:
                        - Clear face view
                        - Identifiable features
                        - Sufficient screen time
                    
                    2. FACE PROMINENCE:
                        - Primary focus vs background
                        - Camera angle showing face
                        - Not obscured

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "faces_featured": boolean,
                            "face_count": int,
                            "first_face_timestamp": float,
                            "visibility_quality": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Faces featured in first 3 seconds
                    - NOT DETECTED (false): No featured faces in first 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear featured faces in opening
                    - 0.7-0.8: Good face visibility in first 3 seconds
                    - 0.5-0.6: Some face visibility
                    - 0.3-0.4: Minimal face visibility
                    - 0.0-0.2: No featured faces
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_closeup_people",
          name="People Close-ups (30% of frame)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features close-up scenes of people (at least 30% of frame).
                """,
          prompt_template="""
                    Analyze if people are shown in close-ups (30%+ of frame).

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PEOPLE CLOSE-UPS

                    DEFINING CLOSE-UP:
                    1. SIZE REQUIREMENT:
                        - People fill 30% or more of frame
                        - Prominently featured
                        - Facial features visible
                    
                    2. CONTEXT:
                        - Can be various angles
                        - Multiple close-ups acceptable
                        - Emphasis on person/face

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "closeup_present": boolean,
                            "frame_percentage": float,
                            "frequency": int
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): People close-ups (30%+) present
                    - NOT DETECTED (false): People smaller than 30%

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Multiple clear people close-ups
                    - 0.7-0.8: Good people close-ups (40%+)
                    - 0.5-0.6: People close-ups (30-40%)
                    - 0.3-0.4: Borderline close-up (25-30%)
                    - 0.0-0.2: No close-up or less than 25%
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_product_context",
          name="Product Context",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product is featured in the context of use (shown being used 
                    in a real-world scenario or everyday situation).
                """,
          prompt_template="""
                    Analyze if the product is shown in context of use.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT CONTEXT OF USE

                    DEFINING PRODUCT CONTEXT:
                    1. USAGE CONTEXT:
                        - Product being used
                        - Real-world application
                        - Everyday scenario
                        - Problem-solution context
                    
                    2. ENVIRONMENT:
                        - Realistic setting
                        - Natural usage scenario
                        - Product benefit shown through use

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "context_present": boolean,
                            "usage_type": str,
                            "scenario_description": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product shown in use context
                    - NOT DETECTED (false): Product shown without context

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product usage context
                    - 0.7-0.8: Good context of use
                    - 0.5-0.6: Some context present
                    - 0.3-0.4: Minimal context
                    - 0.0-0.2: No context shown
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_focused_messaging",
          name="Single Focused Messaging",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad is focused on a single, clear message or theme throughout.
                """,
          prompt_template="""
                    Analyze if the ad maintains one clear, focused message.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR MESSAGE FOCUS

                    DEFINING FOCUSED MESSAGING:
                    1. MESSAGE CLARITY:
                        - One primary message
                        - Consistent throughout
                        - Not scattered or fragmented
                    
                    2. THEMATIC UNITY:
                        - All elements support main message
                        - Clear narrative direction
                        - Coherent storytelling

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "focused": boolean,
                            "primary_message": str,
                            "message_clarity": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Ad focused on one clear message
                    - NOT DETECTED (false): Multiple competing messages

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Crystal clear, single-focused message
                    - 0.7-0.8: Clear focused message
                    - 0.5-0.6: Mostly focused with some side elements
                    - 0.3-0.4: Mixed or unclear focus
                    - 0.0-0.2: No clear single message
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_expression_benefits",
          name="Expression of Benefits",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features any benefit related to the product or service 
                    (e.g., performance, quality, lifestyle improvement).
                """,
          prompt_template="""
                    Analyze if the ad expresses product or service benefits.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR BENEFIT EXPRESSION

                    DEFINING BENEFITS:
                    1. BENEFIT TYPES:
                        - Performance benefits
                        - Quality improvements
                        - Lifestyle enhancements
                        - Problem solutions
                    
                    2. EXPRESSION METHODS:
                        - Visual demonstration
                        - Voice-over explanation
                        - Text/supers
                        - Implied or shown

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "benefits_expressed": boolean,
                            "benefit_types": [str],
                            "expression_method": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Benefits clearly expressed
                    - NOT DETECTED (false): No benefits mentioned

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear benefit expression
                    - 0.7-0.8: Good benefit messaging
                    - 0.5-0.6: Some benefits mentioned
                    - 0.3-0.4: Weak or unclear benefits
                    - 0.0-0.2: No benefits expressed
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_single_feature_benefit",
          name="Single Feature/Benefit",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad is focused on highlighting a single product feature or benefit.
                """,
          prompt_template="""
                    Analyze if the ad focuses on one single feature or benefit.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SINGLE FEATURE/BENEFIT FOCUS

                    DEFINING FOCUS:
                    1. SINGULAR FOCUS:
                        - One feature highlighted
                        - One benefit emphasized
                        - All content supports this
                    
                    2. CONTRAST WITH MULTIPLE:
                        - Not multiple features
                        - Not comprehensive listing
                        - Deep dive into one aspect

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "single_focus": boolean,
                            "featured_benefit": str,
                            "focus_strength": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): One feature/benefit focused
                    - NOT DETECTED (false): Multiple features highlighted

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Exclusively single feature focus
                    - 0.7-0.8: Clear single feature emphasis
                    - 0.5-0.6: Mostly single with some secondary
                    - 0.3-0.4: Mixed focus
                    - 0.0-0.2: Multiple features equal focus
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_benefit_visualization",
          name="Visualization of Benefit",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features the product/service as solving a need or problem 
                    (problem-solution visualization).
                """,
          prompt_template="""
                    Analyze if the ad visualizes product solving a problem or need.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PROBLEM-SOLUTION VISUALIZATION

                    DEFINING VISUALIZATION:
                    1. PROBLEM IDENTIFICATION:
                        - Need or pain point identified
                        - Problem shown or implied
                        - Context of dissatisfaction
                    
                    2. SOLUTION PRESENTATION:
                        - Product solves the problem
                        - Benefit visualization
                        - Before/after scenario
                        - Solution outcome shown

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "problem_solution": boolean,
                            "problem_shown": boolean,
                            "solution_shown": boolean,
                            "visualization_type": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Problem-solution clearly visualized
                    - NOT DETECTED (false): No problem-solution visualization

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear problem-solution narrative
                    - 0.7-0.8: Good visualization of benefits
                    - 0.5-0.6: Some problem-solution elements
                    - 0.3-0.4: Weak visualization
                    - 0.0-0.2: No problem-solution shown
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_competitive_claim",
          name="Competitive Claim",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features any competitive claim (e.g., best in class, 
                    superior to competitors, market leader).
                """,
          prompt_template="""
                    Analyze if the ad makes competitive claims.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR COMPETITIVE CLAIMS

                    DEFINING COMPETITIVE CLAIMS:
                    1. CLAIM TYPES:
                        - Best in class
                        - Superior quality
                        - Market leader
                        - Comparison advantages
                        - #1 or exclusive claims
                    
                    2. EXPRESSION:
                        - Explicit statements
                        - Implied superiority
                        - Comparative messaging

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "competitive_claim_present": boolean,
                            "claim_type": str,
                            "claim_clarity": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Competitive claim present
                    - NOT DETECTED (false): No competitive claim

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, explicit competitive claim
                    - 0.7-0.8: Strong competitive positioning
                    - 0.5-0.6: Some competitive messaging
                    - 0.3-0.4: Weak or implied claim
                    - 0.0-0.2: No competitive claim
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_emotions",
          name="Emotions",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad attempts to arouse or evoke the viewer's emotions 
                    (e.g., happiness, inspiration, empathy, excitement).
                """,
          prompt_template="""
                    Analyze if the ad attempts to evoke viewer emotions.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR EMOTIONAL APPEAL

                    DEFINING EMOTIONAL APPEAL:
                    1. EMOTION TYPES:
                        - Happiness/joy
                        - Inspiration
                        - Empathy/connection
                        - Excitement/energy
                        - Nostalgia
                        - Pride/aspiration
                    
                    2. DELIVERY METHODS:
                        - Visual storytelling
                        - Music/audio
                        - Character performance
                        - Relatable scenarios

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "emotional_appeal": boolean,
                            "emotions_targeted": [str],
                            "emotional_strength": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Clear emotional appeal present
                    - NOT DETECTED (false): No emotional appeal

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Strong, clear emotional connection
                    - 0.7-0.8: Good emotional appeal
                    - 0.5-0.6: Some emotional elements
                    - 0.3-0.4: Weak emotional appeal
                    - 0.0-0.2: No emotional appeal
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="c_delight",
          name="Delight",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if there is any unexpected, surprising, or delightful element 
                    featured in the ad that creates a memorable moment.
                """,
          prompt_template="""
                    Analyze if the ad contains unexpected or delightful elements.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR DELIGHT/SURPRISE ELEMENTS

                    DEFINING DELIGHT:
                    1. SURPRISE ELEMENTS:
                        - Unexpected twist
                        - Surprising reveal
                        - Creative surprise
                        - Unconventional approach
                    
                    2. DELIGHT FACTORS:
                        - Memorable moment
                        - Novelty
                        - Playful execution
                        - Creative excellence

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "delight_present": boolean,
                            "element_description": str,
                            "memorability": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Delightful/surprising element present
                    - NOT DETECTED (false): No unexpected elements

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Highly memorable, delightful moment
                    - 0.7-0.8: Good surprise/delight element
                    - 0.5-0.6: Some unexpected elements
                    - 0.3-0.4: Mild surprise
                    - 0.0-0.2: Nothing surprising or delightful
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]

  return feature_configs
