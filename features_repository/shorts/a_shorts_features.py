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

"""Module with ATTRACT (A) feature configurations for Shorts"""

from models import (
    VideoFeature,
    VideoSegment,
    EvaluationMethod,
    VideoFeatureCategory,
    VideoFeatureSubCategory,
)


def get_attract_features() -> list[VideoFeature]:
  """Gets all ATTRACT (A) ABCD features for Shorts
  
  Returns:
    feature_configs: list of ATTRACT feature configurations
  """
  feature_configs = [
      VideoFeature(
          id="a_heartbeat_story_arc",
          name="Heartbeat Story Arc",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the video reveals a key message, strong scene/visual tease, or 
                    conclusion within the first 3 seconds (up to 2.99 seconds). This creates 
                    a "heartbeat" moment that captures immediate viewer attention and encourages 
                    continued watching.
                """,
          prompt_template="""
                    Analyze if the short-form video contains a "Heartbeat Story Arc" - 
                    a compelling hook that reveals key information within the first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR HEARTBEAT MOMENTS IN THE FIRST 3 SECONDS (0-2.99s):
                    
                    Look for one or more of these elements:
                    1. KEY MESSAGE REVEALED:
                        - Important product benefit stated
                        - Punchline or humor delivered
                        - Emotional statement made
                        - Narrative hook established
                        - Problem statement introduced
                    
                    2. STRONG VISUAL TEASE:
                        - Striking visual moment
                        - Product dramatically revealed
                        - Unexpected scene change
                        - Visually compelling before/after
                        - Attention-grabbing motion or action
                    
                    3. CONCLUSION/RESOLUTION:
                        - Story conclusion shown early
                        - Result or outcome revealed
                        - Transformation demonstrated
                        - Question answered
                        - Climax moment
                    
                    4. NARRATIVE HOOK:
                        - Question posed that demands answer
                        - Mystery presented
                        - Challenge introduced
                        - Curiosity gap created
                        - Call to action established

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if heartbeat moment exists in first 3 seconds
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "timing_analysis": {{
                                "first_3_seconds_content": str,  # What happens in 0-2.99s
                                "heartbeat_start_timestamp": float,  # When hook begins
                                "heartbeat_end_timestamp": float,    # When hook ends
                                "early_reveal": boolean              # Is it early enough?
                            }},
                            "heartbeat_type": {{
                                "message_revealed": boolean,
                                "message_details": str,
                                "visual_tease": boolean,
                                "visual_description": str,
                                "conclusion_shown": boolean,
                                "conclusion_details": str,
                                "narrative_hook": boolean,
                                "hook_description": str,
                                "dominant_type": str  # Most prominent element
                            }},
                            "engagement_indicators": {{
                                "hook_strength": str,  # "Weak" | "Moderate" | "Strong"
                                "viewer_retention_potential": str,  # How likely to keep watching
                                "emotional_impact": str,  # "Low" | "Medium" | "High"
                                "clarity": str,  # How clear is the hook message
                                "relevance": str  # How relevant to the overall message
                            }},
                            "supporting_elements": {{
                                "audio_contribution": str,  # How audio supports the hook
                                "visual_contribution": str,  # How visuals support the hook
                                "text_overlay_contribution": str,  # Any text supers in first 5s
                                "pacing_contribution": str  # How pacing affects hook
                            }},
                            "key_moments": [
                                {{
                                    "timestamp": float,
                                    "description": str,
                                    "element_type": str,  # "Message" | "Visual" | "Conclusion" | "Hook"
                                    "impact_score": float  # 0.0-1.0
                                }}
                            ]
                        }},
                        "notes": str  # Additional context or observations
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Video clearly shows a heartbeat moment in first 3 seconds
                    - NOT DETECTED (false): Video lacks a compelling early hook or it appears after 3 seconds
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, unmistakable heartbeat moment early on
                    - 0.7-0.8: Strong hook with clear early reveal
                    - 0.5-0.6: Moderate hook but timing or clarity could be better
                    - 0.3-0.4: Weak hook or appears around the 5-second mark
                    - 0.0-0.2: No clear hook or appears after 5 seconds

                    IMPORTANT NOTES:
                    1. Timing is critical - must occur within first 3 seconds (up to 2.99s)
                    2. Look for ANY of the four element types (not just one)
                    3. Hook should feel organic to the story, not forced
                    4. Consider how the hook creates desire to see more of the video
                    5. Evaluate whether the hook is relevant to the product/message
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="a_fast_pacing_full",
          name="Fast Pacing Full Video",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_fast_pacing_early",
          name="Fast Pacing Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_tight_framing",
          name="Tight Framing",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_tight_framing_early",
          name="Tight Framing Early",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_has_sound",
          name="Has Sound",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_has_music",
          name="Has Music",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_sound_effects",
          name="Sound Effects",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_human_voice",
          name="Human Voice",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_dialogue_single",
          name="Single Dialogue",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_dialogue_multiple",
          name="Multiple Dialogue",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_direct_camera",
          name="Direct Camera Address",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_has_supers",
          name="Has Supers",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_supers_combined",
          name="Supers Combined",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_supers_audio_augment",
          name="Supers Audio Augmentation",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_supers_audio_match",
          name="Supers Audio Matching",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_large_supers",
          name="Large Supers",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_bright_colors",
          name="Bright Colors",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_high_contrast",
          name="High Contrast",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
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
