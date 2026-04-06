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
          name="Brand Visualized (Overall)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if branding (brand name, brand logo, or branded products/packaging) 
                    is shown in-situation or overlaid at any time during the video.
                """,
          prompt_template="""
                    Analyze if the video contains branding (brand name, logo, branded products, 
                    or packaging) displayed in-situation or overlaid at any time.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR BRAND PRESENCE:
                    
                    DEFINING BRANDING:
                    1. BRAND NAME:
                        - Text displaying brand name
                        - Spoken brand name
                        - Branded communications
                    
                    2. BRAND LOGO:
                        - Official brand logo
                        - Branded mark or symbol
                        - Logo variations or derivatives
                    
                    3. BRANDED PRODUCTS:
                        - Products with visible branding
                        - Branded packaging
                        - Branded merchandise
                    
                    4. DISPLAY METHODS:
                        - In-situation (product in real context)
                        - Overlaid (graphic overlay on screen)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "brand_presence": {{
                                "brand_visible": boolean,
                                "brand_elements": [str],
                                "display_type": str,
                                "frequency": int
                            }},
                            "brand_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "brand_element": str,
                                    "display_type": str,
                                    "description": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand name, logo, or branded product/packaging visible
                    - NOT DETECTED (false): No branding elements visible

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, prominent brand presence multiple times
                    - 0.7-0.8: Good brand visibility, clear and identifiable
                    - 0.5-0.6: Some brand presence but minimal or brief
                    - 0.3-0.4: Very minimal brand visibility
                    - 0.0-0.2: No brand elements detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_early",
          name="Brand Visualized (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if branding (brand name, brand logo, or branded products/packaging) 
                    is shown in-situation or overlaid within the first 3 seconds (up to 2.99s).
                """,
          prompt_template="""
                    Analyze if branding appears in the first 3 seconds of the video.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR BRAND ELEMENTS

                    DEFINING BRANDING (same as above)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "brand_early_presence": {{
                                "brand_in_first_3s": boolean,
                                "first_appearance_timestamp": float,
                                "brand_elements": [str]
                            }},
                            "timing": {{
                                "first_3s_content": str,
                                "brand_placement": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand visible in first 3 seconds
                    - NOT DETECTED (false): Brand not shown in first 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear brand presence within first 1 second
                    - 0.7-0.8: Brand visible in first 3 seconds, clear and identifiable
                    - 0.5-0.6: Brand present but towards end of 3-second window
                    - 0.3-0.4: Minimal brand visibility in first 3 seconds
                    - 0.0-0.2: Brand not visible in first 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_late",
          name="Brand Visualized (Last 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if branding (brand name, brand logo, or branded products/packaging) 
                    is shown in-situation or overlaid within the last 3 seconds of the video.
                """,
          prompt_template="""
                    Analyze if branding appears in the last 3 seconds of the video.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE LAST 3 SECONDS FOR BRAND ELEMENTS

                    DEFINING BRANDING (same as b_brand_display)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "brand_late_presence": {{
                                "brand_in_last_3s": boolean,
                                "last_appearance_timestamp": float,
                                "brand_elements": [str]
                            }},
                            "timing": {{
                                "last_3s_content": str,
                                "brand_placement": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand visible in last 3 seconds
                    - NOT DETECTED (false): Brand not shown in last 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear brand presence in final moments
                    - 0.7-0.8: Brand visible in last 3 seconds, clear and identifiable
                    - 0.5-0.6: Brand present in last 3 seconds but not prominent
                    - 0.3-0.4: Minimal brand visibility in last 3 seconds
                    - 0.0-0.2: Brand not visible in last 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_overlaid",
          name="Brand Visual (Overlaid)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if an overlaid brand logo is present at any time during the video. 
                    Overlaid means the logo is added as a graphic element on top of the video content.
                """,
          prompt_template="""
                    Analyze if an overlaid brand logo graphic appears at any time in the video.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR OVERLAID BRAND LOGO

                    DEFINING OVERLAID BRANDING:
                    1. GRAPHIC OVERLAY:
                        - Logo added on top of video
                        - Not part of natural scene
                        - Text overlay of brand name
                        - Transparent or opaque overlay
                    
                    2. PLACEMENT:
                        - Corner placement (top, bottom, sides)
                        - Center placement
                        - Full screen overlay
                        - Consistent vs variable placement

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "overlaid_brand": {{
                                "overlaid_present": boolean,
                                "overlay_type": str,
                                "placement": str,
                                "frequency": int
                            }},
                            "overlay_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "overlay_type": str,
                                    "placement": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Overlaid brand logo visible
                    - NOT DETECTED (false): No overlaid branding

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, prominent overlaid logo
                    - 0.7-0.8: Good overlaid branding visible
                    - 0.5-0.6: Some overlaid branding present
                    - 0.3-0.4: Minimal overlaid branding
                    - 0.0-0.2: No overlaid branding
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_in_situation",
          name="Brand Visual (In-situation)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if a brand logo, branded product, or branded packaging is shown 
                    ONLY in-situation (as part of the natural scene) at any time.
                """,
          prompt_template="""
                    Analyze if brand elements appear in-situation within the video.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR IN-SITUATION BRANDING

                    DEFINING IN-SITUATION BRANDING:
                    1. NATURAL CONTEXT:
                        - Brand/product shown in real usage
                        - Part of the scene, not overlaid
                        - Visible through product placement
                        - Packaging visible in natural setting
                    
                    2. CONTRAST WITH OVERLAID:
                        - Not a graphic overlay
                        - Actual product or packaging present
                        - Logo visible on product/packaging

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "in_situation_brand": {{
                                "in_situation_present": boolean,
                                "brand_elements": [str],
                                "context_type": str,
                                "frequency": int
                            }},
                            "placement_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "brand_element": str,
                                    "context": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand visible in natural scene context
                    - NOT DETECTED (false): No in-situation branding

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear in-situation brand placement
                    - 0.7-0.8: Good in-situation visibility
                    - 0.5-0.6: Some in-situation branding present
                    - 0.3-0.4: Minimal in-situation branding
                    - 0.0-0.2: No in-situation branding
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_visual_nonconsecutive",
          name="Brand Visual (3+ Times)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if any branding is present on at least 3 frames with gaps between 
                    each instance (non-consecutive). The same branding instance can appear on 
                    multiple frames, but NOT on consecutive frames.
                """,
          prompt_template="""
                    Analyze if branding appears on at least 3 non-consecutive frames.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR MULTI-FRAME NON-CONSECUTIVE BRANDING

                    DEFINING NON-CONSECUTIVE BRANDING:
                    1. FREQUENCY:
                        - Branding appears on at least 3 frames
                        - Frames must be non-consecutive (gaps between)
                        - Same branding can repeat
                        - Different branding elements can be mixed
                    
                    2. GAPS:
                        - At least 1 frame gap between appearances
                        - Non-continuous visibility
                        - Multiple separate appearances

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "nonconsecutive_brand": {{
                                "frame_count": int,
                                "meets_3plus_criteria": boolean,
                                "consecutive_pattern": str,
                                "brand_elements": [str]
                            }},
                            "frame_segments": [
                                {{
                                    "frame_number": int,
                                    "start_timestamp": float,
                                    "brand_element": str,
                                    "gap_before": float
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand on 3+ non-consecutive frames
                    - NOT DETECTED (false): Fewer than 3 frames or mostly consecutive

                    CONFIDENCE SCORING:
                    - 0.9-1.0: 4+ non-consecutive frame appearances
                    - 0.7-0.8: Clear 3 non-consecutive frames
                    - 0.5-0.6: 3 frames with some consecutive overlap
                    - 0.3-0.4: Only 2 non-consecutive frames
                    - 0.0-0.2: Fewer than 2 frames or all consecutive
                """,
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
          evaluation_criteria="""
                    Detects if the brand logo is at least 10% of the screen. The logo can be 
                    inclusive or exclusive of packaging. For the latter case, packaging is NOT 
                    included in the count.
                """,
          prompt_template="""
                    Analyze if the brand logo appears at least 10% of the screen size.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR LARGE LOGO PLACEMENT

                    DEFINING LARGE LOGO:
                    1. SIZE REQUIREMENTS:
                        - Logo occupies minimum 10% of screen
                        - Measure from top-left to bottom-right
                        - Can include packaging or be logo-only
                    
                    2. MEASUREMENT:
                        - Estimate frame area percentage
                        - Account for logo dimensions
                        - Consider scaling with zoom
                    
                    3. LOGO VS PACKAGING:
                        - Logo-only: Just the brand mark
                        - Inclusive: Logo with packaging
                        - Not counted: Packaging without logo

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "large_logo": {{
                                "logo_present": boolean,
                                "screen_percentage": float,
                                "meets_10pct_criteria": boolean,
                                "logo_type": str
                            }},
                            "logo_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "screen_percentage": float,
                                    "description": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Logo at least 10% of screen
                    - NOT DETECTED (false): Logo smaller than 10%

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Logo 20%+ of screen
                    - 0.7-0.8: Logo 15-20% of screen
                    - 0.5-0.6: Logo 10-15% of screen
                    - 0.3-0.4: Logo 7-10% of screen
                    - 0.0-0.2: Logo less than 7%
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_mention",
          name="Brand Mentioned",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the brand is mentioned through an audible logo (jingle), 
                    brand-specific audio signature, or voice-over mention of the brand name 
                    at any time.
                """,
          prompt_template="""
                    Analyze if the brand is mentioned audibly through audio or voice.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR BRAND MENTIONS

                    DEFINING BRAND MENTION:
                    1. AUDIO LOGO/JINGLE:
                        - Brand-specific sound signature
                        - Recognizable audio mark
                        - Jingle or theme
                    
                    2. VOICE MENTION:
                        - Voice-over speaking brand name
                        - Character dialogue mentioning brand
                        - Clear, audible brand name
                    
                    3. AUDIBILITY:
                        - Clear and understandable
                        - Distinct from background
                        - Purposeful mention

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "brand_mention": {{
                                "mentioned": boolean,
                                "mention_type": str,
                                "frequency": int,
                                "clarity": str
                            }},
                            "mention_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "mention_type": str,
                                    "content": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand mentioned audibly
                    - NOT DETECTED (false): No audible brand mention

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, distinct brand mention
                    - 0.7-0.8: Good brand mention, clearly audible
                    - 0.5-0.6: Brand mention present but not prominent
                    - 0.3-0.4: Weak or unclear brand mention
                    - 0.0-0.2: No audible brand mention
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_mention_early",
          name="Brand Mention (Speech) (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the brand name is mentioned in speech/audio within the 
                    first 3 seconds of the video.
                """,
          prompt_template="""
                    Analyze if the brand name is mentioned in speech within the first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR BRAND SPEECH MENTION

                    DEFINING BRAND MENTION:
                    1. VOICE-OVER:
                        - Narrator speaking brand name
                        - Clear pronunciation
                    
                    2. DIALOGUE:
                        - Character speaking brand name
                        - Natural conversation context
                    
                    3. TIMING:
                        - Must occur within first 3 seconds
                        - Clear and audible

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "early_mention": {{
                                "mentioned_in_first_3s": boolean,
                                "mention_timestamp": float,
                                "mention_type": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand mentioned in first 3 seconds
                    - NOT DETECTED (false): Brand not mentioned or after 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear brand mention within first 1 second
                    - 0.7-0.8: Brand mentioned in first 3 seconds, clear
                    - 0.5-0.6: Brand mention near end of first 3 seconds
                    - 0.3-0.4: Weak mention in first 3 seconds
                    - 0.0-0.2: Brand not mentioned in first 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_mention_late",
          name="Brand Mention (Speech) (Last 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the brand name is mentioned in speech/audio within the 
                    last 3 seconds of the video.
                """,
          prompt_template="""
                    Analyze if the brand name is mentioned in speech within the last 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE LAST 3 SECONDS FOR BRAND SPEECH MENTION

                    DEFINING BRAND MENTION (same as b_brand_mention_early)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "late_mention": {{
                                "mentioned_in_last_3s": boolean,
                                "mention_timestamp": float,
                                "mention_type": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand mentioned in last 3 seconds
                    - NOT DETECTED (false): Brand not mentioned in last 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear brand mention in final moments
                    - 0.7-0.8: Brand mentioned in last 3 seconds clearly
                    - 0.5-0.6: Brand mention in last 3 seconds but subtle
                    - 0.3-0.4: Weak mention in last 3 seconds
                    - 0.0-0.2: Brand not mentioned in last 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_mention_see_say",
          name="Brand Mention (Speech) (See & Say)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the brand is mentioned in audio and visualized on the same 
                    frame at any time in the video (audio-visual synchronization).
                """,
          prompt_template="""
                    Analyze if brand is mentioned in audio while being visualized on screen 
                    in the same frame.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SIMULTANEOUS AUDIO-VISUAL BRAND

                    DEFINING SEE & SAY:
                    1. SIMULTANEOUS PRESENCE:
                        - Brand name spoken while visible
                        - Logo shown while mentioned
                        - Synchronized audio and visual
                    
                    2. CONTEXT:
                        - Can be voice-over with visual
                        - Character dialogue with visible product
                        - Any combination at same time

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "see_say": {{
                                "simultaneous": boolean,
                                "frequency": int,
                                "audio_visual_sync": str
                            }},
                            "sync_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "visual_element": str,
                                    "audio_mention": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand mentioned and visualized simultaneously
                    - NOT DETECTED (false): No simultaneous audio-visual brand interaction

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear simultaneous brand audio and visual
                    - 0.7-0.8: Good synchronization of audio and visual
                    - 0.5-0.6: Some synchronization present
                    - 0.3-0.4: Minimal synchronization
                    - 0.0-0.2: No synchronization
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_mention_see_say_early",
          name="Brand Mention (Speech) (See & Say) (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the brand is mentioned and visualized simultaneously 
                    in the first 3 seconds of the video.
                """,
          prompt_template="""
                    Analyze if brand is mentioned and visualized simultaneously in first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR SIMULTANEOUS AUDIO-VISUAL BRAND

                    DEFINING SEE & SAY (same as b_brand_mention_see_say)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "early_see_say": {{
                                "simultaneous_in_first_3s": boolean,
                                "timestamp": float
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand audio-visual sync in first 3 seconds
                    - NOT DETECTED (false): No such sync in first 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear simultaneous brand in first 1-2 seconds
                    - 0.7-0.8: Good synchronization in first 3 seconds
                    - 0.5-0.6: Sync near end of first 3 seconds
                    - 0.3-0.4: Weak synchronization in first 3 seconds
                    - 0.0-0.2: No synchronization in first 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_jingle",
          name="Brand Jingle",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the brand name is mentioned as part of a jingle or brand-specific 
                    audio signature (recognizable musical phrase).
                """,
          prompt_template="""
                    Analyze if the brand name appears in a jingle or audio signature.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR JINGLE WITH BRAND NAME

                    DEFINING JINGLE:
                    1. CHARACTERISTICS:
                        - Recognizable musical phrase
                        - Brand-associated music
                        - Sung or instrumental
                        - Repeatable audio signature
                    
                    2. BRAND INTEGRATION:
                        - Brand name in lyrics (if sung)
                        - Clear association with brand
                        - Signature audio mark

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "jingle": {{
                                "jingle_present": boolean,
                                "includes_brand_name": boolean,
                                "jingle_type": str,
                                "recognizability": str
                            }},
                            "jingle_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "description": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand name in jingle/audio signature
                    - NOT DETECTED (false): No jingle with brand name

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear, recognizable brand jingle
                    - 0.7-0.8: Good jingle with brand name
                    - 0.5-0.6: Jingle present, brand name somewhat clear
                    - 0.3-0.4: Weak jingle or unclear brand reference
                    - 0.0-0.2: No jingle or brand name not present
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_brand_elements",
          name="Multiple Brand Elements",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad includes the brand in 2 or more different audio or 
                    visual ways (e.g., visual logo AND audio mention, or multiple visual 
                    representations).
                """,
          prompt_template="""
                    Analyze if the brand is presented in 2 or more different ways (audio/visual).

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR MULTIPLE BRAND REPRESENTATIONS

                    DEFINING MULTIPLE ELEMENTS:
                    1. VISUAL WAYS:
                        - Logo (overlaid or in-situation)
                        - Product/packaging
                        - Brand name text
                        - Visual elements/colors
                    
                    2. AUDIO WAYS:
                        - Voice mention
                        - Jingle/audio signature
                        - Branded music
                        - Sound effects
                    
                    3. COMBINATIONS:
                        - At least 2 different methods
                        - Can be visual+visual or audio+audio or mixed

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "brand_elements": {{
                                "total_elements": int,
                                "meets_2plus_criteria": boolean,
                                "visual_elements": [str],
                                "audio_elements": [str]
                            }},
                            "element_breakdown": {{
                                "visual_count": int,
                                "audio_count": int,
                                "descriptions": [str]
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Brand in 2+ different audio/visual ways
                    - NOT DETECTED (false): Brand in only 1 way

                    CONFIDENCE SCORING:
                    - 0.9-1.0: 3+ brand elements represented
                    - 0.7-0.8: Clear 2 brand elements
                    - 0.5-0.6: 2 elements but one is subtle
                    - 0.3-0.4: Claims of 2 but only 1 clear
                    - 0.0-0.2: Only 1 brand element
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_visualized",
          name="Product Visualized (Overall)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if a product or branded packaging is visible at any time 
                    during the video.
                """,
          prompt_template="""
                    Analyze if a product or branded packaging is visible at any time.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT PRESENCE

                    DEFINING PRODUCT:
                    1. PRODUCT TYPES:
                        - Physical product
                        - Branded packaging
                        - Product variant/models
                        - Product in use
                    
                    2. VISIBILITY:
                        - Clear view of product
                        - Product identifiable
                        - Branded packaging visible

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "product_presence": {{
                                "product_visible": boolean,
                                "product_type": str,
                                "frequency": int,
                                "context": str
                            }},
                            "product_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "product_type": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product or packaging visible
                    - NOT DETECTED (false): No product visible

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product presence throughout
                    - 0.7-0.8: Good product visibility
                    - 0.5-0.6: Some product visibility
                    - 0.3-0.4: Minimal product visibility
                    - 0.0-0.2: No product visible
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_visualized_early",
          name="Product Visualized (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if a product or branded packaging is visible in the first 3 seconds 
                    (up to 2.99s) of the video.
                """,
          prompt_template="""
                    Analyze if product or packaging is visible in the first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR PRODUCT

                    DEFINING PRODUCT (same as b_product_visualized)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "early_product": {{
                                "product_in_first_3s": boolean,
                                "first_appearance_timestamp": float,
                                "product_type": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product visible in first 3 seconds
                    - NOT DETECTED (false): Product not shown in first 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product in first 1 second
                    - 0.7-0.8: Product visible in first 3 seconds
                    - 0.5-0.6: Product visible near end of first 3 seconds
                    - 0.3-0.4: Minimal product visibility
                    - 0.0-0.2: No product in first 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_visualized_late",
          name="Product Visualized (Last 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if a product or branded packaging is visible in the last 3 seconds 
                    of the video.
                """,
          prompt_template="""
                    Analyze if product or packaging is visible in the last 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE LAST 3 SECONDS FOR PRODUCT

                    DEFINING PRODUCT (same as b_product_visualized)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "late_product": {{
                                "product_in_last_3s": boolean,
                                "last_appearance_timestamp": float,
                                "product_type": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product visible in last 3 seconds
                    - NOT DETECTED (false): Product not shown in last 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product in final moments
                    - 0.7-0.8: Product visible in last 3 seconds
                    - 0.5-0.6: Product visible in last 3 seconds but subtle
                    - 0.3-0.4: Minimal product visibility
                    - 0.0-0.2: No product in last 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_closeup",
          name="Product Close-ups (30% of frame)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features close-up scenes of the product (at least 30% of frame).
                """,
          prompt_template="""
                    Analyze if product is shown in close-up (30%+ of frame).

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT CLOSE-UPS

                    DEFINING CLOSE-UP:
                    1. SIZE REQUIREMENT:
                        - Product fills 30% or more of frame
                        - Prominently featured
                        - Viewer can see details
                    
                    2. CONTEXT:
                        - Can be in-situation or product-focused
                        - Various angles acceptable
                        - Multiple close-ups acceptable

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "product_closeup": {{
                                "closeup_present": boolean,
                                "frame_percentage": float,
                                "frequency": int
                            }},
                            "closeup_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "frame_percentage": float
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product close-up (30%+) present
                    - NOT DETECTED (false): Product smaller than 30%

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Multiple clear product close-ups
                    - 0.7-0.8: Good product close-ups (40%+)
                    - 0.5-0.6: Product close-ups (30-40%)
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
          id="b_product_extreme_closeup",
          name="Product Extreme Close-ups (60% of frame)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features extreme close-up scenes of the product 
                    (at least 60% of frame).
                """,
          prompt_template="""
                    Analyze if product is shown in extreme close-up (60%+ of frame).

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT EXTREME CLOSE-UPS

                    DEFINING EXTREME CLOSE-UP:
                    1. SIZE REQUIREMENT:
                        - Product fills 60% or more of frame
                        - Very prominent display
                        - Details clearly visible
                    
                    2. CONTEXT:
                        - Maximum product focus
                        - Multiple angles acceptable
                        - Emphasizes product details

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "product_extreme_closeup": {{
                                "extreme_closeup_present": boolean,
                                "frame_percentage": float,
                                "frequency": int
                            }},
                            "extreme_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "frame_percentage": float
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Extreme product close-up (60%+) present
                    - NOT DETECTED (false): Product smaller than 60%

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Multiple extreme close-ups (80%+)
                    - 0.7-0.8: Clear extreme close-ups (70%+)
                    - 0.5-0.6: Extreme close-ups (60-70%)
                    - 0.3-0.4: Borderline extreme (50-60%)
                    - 0.0-0.2: No extreme close-up or less than 50%
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_mention_combined",
          name="Product Mention (Speech or Text)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product is featured in audio (voice-over or character speech) 
                    or in text supers at any time.
                """,
          prompt_template="""
                    Analyze if product is mentioned in audio or text.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT MENTION

                    DEFINING PRODUCT MENTION:
                    1. AUDIO MENTION:
                        - Voice-over mentioning product
                        - Character dialogue about product
                        - Product name spoken
                    
                    2. TEXT MENTION:
                        - Product name in supers/text
                        - Product features in text
                        - Promotional text about product

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "product_mention": {{
                                "mentioned": boolean,
                                "mention_types": [str],
                                "frequency": int
                            }},
                            "mention_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "mention_type": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product mentioned in audio or text
                    - NOT DETECTED (false): No product mention

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product mention in audio and/or text
                    - 0.7-0.8: Good product mention visible
                    - 0.5-0.6: Some product mention present
                    - 0.3-0.4: Weak or unclear mention
                    - 0.0-0.2: No product mention
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_mention_speech",
          name="Product Mention (Speech)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product is mentioned in the audio (voice-over or 
                    character speech) at any time.
                """,
          prompt_template="""
                    Analyze if product name is mentioned in audio/speech.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT SPEECH MENTION

                    DEFINING PRODUCT SPEECH MENTION:
                    1. VOICE-OVER:
                        - Narrator speaking product name
                        - Product features mentioned
                    
                    2. DIALOGUE:
                        - Characters discussing product
                        - Product name in conversation

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "speech_mention": {{
                                "mentioned_in_speech": boolean,
                                "mention_type": str,
                                "clarity": str
                            }},
                            "speech_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "content": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product mentioned in speech
                    - NOT DETECTED (false): No product speech mention

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product speech mention
                    - 0.7-0.8: Good product mention in audio
                    - 0.5-0.6: Some product mention in speech
                    - 0.3-0.4: Weak or unclear mention
                    - 0.0-0.2: No product mention
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_mention_speech_early",
          name="Product Mention (Speech) (First 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product is mentioned in speech within the first 3 seconds.
                """,
          prompt_template="""
                    Analyze if product is mentioned in speech within first 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR PRODUCT SPEECH MENTION

                    DEFINING PRODUCT SPEECH MENTION (same as b_product_mention_speech)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "early_speech_mention": {{
                                "mentioned_in_first_3s": boolean,
                                "mention_timestamp": float
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product mentioned in first 3 seconds
                    - NOT DETECTED (false): Product not mentioned in first 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product mention in first 1-2 seconds
                    - 0.7-0.8: Product mentioned in first 3 seconds
                    - 0.5-0.6: Product mention near end of first 3 seconds
                    - 0.3-0.4: Weak mention in first 3 seconds
                    - 0.0-0.2: No mention in first 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_mention_speech_late",
          name="Product Mention (Speech) (Last 3s)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product is mentioned in speech within the last 3 seconds.
                """,
          prompt_template="""
                    Analyze if product is mentioned in speech within last 3 seconds.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE LAST 3 SECONDS FOR PRODUCT SPEECH MENTION

                    DEFINING PRODUCT SPEECH MENTION (same as b_product_mention_speech)

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "late_speech_mention": {{
                                "mentioned_in_last_3s": boolean,
                                "mention_timestamp": float
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product mentioned in last 3 seconds
                    - NOT DETECTED (false): Product not mentioned in last 3 seconds

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product mention in final moments
                    - 0.7-0.8: Product mentioned in last 3 seconds
                    - 0.5-0.6: Product mention in last 3 seconds but subtle
                    - 0.3-0.4: Weak mention in last 3 seconds
                    - 0.0-0.2: No mention in last 3 seconds
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_mention_text",
          name="Product Mention (Text)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product is mentioned in text/supers at any time.
                """,
          prompt_template="""
                    Analyze if product is mentioned in text or supers.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT MENTION IN TEXT

                    DEFINING PRODUCT TEXT MENTION:
                    1. TEXT OVERLAY:
                        - Product name in supers
                        - Promotional text about product
                        - Product features listed
                        - Call-to-action about product
                    
                    2. PROMINENCE:
                        - Clearly visible text
                        - On-screen long enough to read

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "text_mention": {{
                                "mentioned_in_text": boolean,
                                "text_content": str,
                                "readability": str,
                                "duration": float
                            }},
                            "text_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "text_content": str
                                }}
                            ]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product mentioned in text/supers
                    - NOT DETECTED (false): No product text mention

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear product text mention
                    - 0.7-0.8: Good product mention in text
                    - 0.5-0.6: Some product mention in text
                    - 0.3-0.4: Weak or unclear text mention
                    - 0.0-0.2: No product text mention
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="b_product_focus",
          name="Product Focused Narrative",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the product plays a key role in the narrative - meaning the 
                    product is central to the story or message being conveyed.
                """,
          prompt_template="""
                    Analyze if the product plays a key role in the video narrative.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRODUCT NARRATIVE FOCUS

                    DEFINING PRODUCT FOCUS:
                    1. KEY ROLE:
                        - Product central to the story
                        - Narrative revolves around product
                        - Product is the solution
                        - Product drives the action
                    
                    2. NARRATIVE CONTEXT:
                        - Product use is shown
                        - Benefit delivery via product
                        - Product is protagonist/focus
                        - Problem-solution with product

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "product_focus": {{
                                "key_role": boolean,
                                "narrative_centrality": str,
                                "focus_percentage": float
                            }},
                            "narrative_analysis": {{
                                "story_role": str,
                                "problem_solution": boolean,
                                "product_benefit_shown": boolean
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Product plays key narrative role
                    - NOT DETECTED (false): Product is secondary or not central

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Product is protagonist/central focus
                    - 0.7-0.8: Strong product focus in narrative
                    - 0.5-0.6: Moderate product focus
                    - 0.3-0.4: Minimal product narrative focus
                    - 0.0-0.2: Product not central to narrative
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]

  return feature_configs
