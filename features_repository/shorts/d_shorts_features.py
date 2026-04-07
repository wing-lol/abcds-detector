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
          name="Call to Action (Text)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the call-to-action (CTA) message is visualized/displayed as text/supers in the ad.
                """,
          prompt_template="""
                    Analyze if the CTA is displayed as text/supers.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR CTA IN TEXT/SUPERS:
                    
                    DEFINING CTA TEXT:
                    1. CTA MESSAGE TYPES:
                        - "Click here"
                        - "Learn more"
                        - "Shop now"
                        - "Download"
                        - "Sign up"
                        - "Visit us"
                        - "Buy now"
                        - Any actionable instruction
                    
                    2. TEXT DISPLAY:
                        - Text supers/overlay
                        - On-screen text
                        - Clear and visible
                        - Readable size

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "cta_text_present": boolean,
                            "cta_message": str,
                            "text_clarity": str,
                            "frequency": int
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): CTA text/supers visible
                    - NOT DETECTED (false): No CTA text displayed

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear CTA text supers
                    - 0.7-0.8: Good CTA visibility
                    - 0.5-0.6: CTA text present but subtle
                    - 0.3-0.4: Minimal CTA visibility
                    - 0.0-0.2: No CTA text detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
    #   VideoFeature(
    #       id="d_audio_cta",
    #       name="Audio Call to Action",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.DIRECT,
    #       video_segment=VideoSegment.FULL_VIDEO,
    #       evaluation_criteria="TODO",
    #       prompt_template="TODO",
    #       extra_instructions=[],
    #       evaluation_method=EvaluationMethod.LLMS,
    #       evaluation_function="",
    #       include_in_evaluation=True,
    #       group_by=VideoSegment.FULL_VIDEO,
    #   ),
      VideoFeature(
          id="d_free_text",
          name="Word 'Free' mentioned (Text)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the word 'free' is displayed as text in the ad at any time.
                """,
          prompt_template="""
                    Analyze if the word 'free' appears as text/supers in the video.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR TEXT 'FREE':
                    
                    DEFINING TEXT 'FREE':
                    1. TEXT DISPLAY:
                        - Word 'free' in supers/text
                        - Clearly visible
                        - On-screen long enough to read
                    
                    2. CONTEXT:
                        - Can be standalone
                        - Part of larger message
                        - Any text format

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "free_text_present": boolean,
                            "text_content": str,
                            "visibility": str,
                            "frequency": int
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Word 'free' displayed as text
                    - NOT DETECTED (false): Word 'free' not in text

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear 'free' text multiple times
                    - 0.7-0.8: Good text visibility of 'free'
                    - 0.5-0.6: 'Free' text visible but subtle
                    - 0.3-0.4: Minimal 'free' visibility
                    - 0.0-0.2: No 'free' text detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_free_speech",
          name="Word 'Free' mentioned (Speech)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the word 'free' is mentioned in the audio (voice-over or dialogue) at any time.
                """,
          prompt_template="""
                    Analyze if the word 'free' is mentioned in audio/speech.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR AUDIO MENTION OF 'FREE':
                    
                    DEFINING AUDIO 'FREE':
                    1. VOICE MENTION:
                        - Voice-over speaking 'free'
                        - Character dialogue mentioning 'free'
                        - Clear pronunciation
                    
                    2. AUDIBILITY:
                        - Clearly audible
                        - Understandable context

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "free_speech_present": boolean,
                            "mention_type": str,
                            "frequency": int,
                            "clarity": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Word 'free' mentioned in audio
                    - NOT DETECTED (false): Word 'free' not mentioned

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear 'free' mention multiple times
                    - 0.7-0.8: Good audio clarity of 'free'
                    - 0.5-0.6: 'Free' mentioned but subtle
                    - 0.3-0.4: Minimal clarity
                    - 0.0-0.2: No audio 'free' detected
                """,
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
          evaluation_criteria="""
                    Detects if the ad features how or where it is possible to purchase or partake in the offer.
                """,
          prompt_template="""
                    Analyze if the ad shows how/where to purchase or partake.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PURCHASE PATH:
                    
                    DEFINING PURCHASE PATH:
                    1. PURCHASE METHODS:
                        - Website shown
                        - Store location
                        - QR code or link
                        - App indication
                        - Phone number
                    
                    2. CLARITY:
                        - How to purchase explained
                        - Where to go indicated
                        - Clear instructions provided

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "path_shown": boolean,
                            "purchase_method": str,
                            "clarity": str,
                            "method_type": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Purchase path/method clearly shown
                    - NOT DETECTED (false): No purchase path indicated

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear purchase path with multiple options
                    - 0.7-0.8: Good purchase path shown
                    - 0.5-0.6: Purchase path mentioned but subtle
                    - 0.3-0.4: Minimal path indication
                    - 0.0-0.2: No path to purchase shown
                """,
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
          evaluation_criteria="""
                    Detects if the ad features a search bar as a call-to-action element.
                """,
          prompt_template="""
                    Analyze if the ad displays a search bar.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SEARCH BAR:
                    
                    DEFINING SEARCH BAR:
                    1. SEARCH BAR CHARACTERISTICS:
                        - Search input field visible
                        - Query being typed/shown
                        - Search UI element
                        - Magnifying glass icon
                        - Search functionality indicated
                    
                    2. CONTEXT:
                        - Product search
                        - General search
                        - Integration with platform

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "search_bar_present": boolean,
                            "search_type": str,
                            "prominence": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Search bar visible
                    - NOT DETECTED (false): No search bar

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear search bar with interaction
                    - 0.7-0.8: Good search bar visibility
                    - 0.5-0.6: Search bar present but subtle
                    - 0.3-0.4: Minimal search indication
                    - 0.0-0.2: No search bar detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_relevant_call_to_action",
          name="Call to Action (Visual)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the CTA (call-to-action) is visualized after the appearance of a product, 
                    problem, need, or insight (contextually relevant timing).
                """,
          prompt_template="""
                    Analyze if CTA appears after product/problem/need/insight.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR RELEVANT CTA TIMING:
                    
                    DEFINING RELEVANT TIMING:
                    1. CONTEXT ELEMENTS:
                        - Product shown first
                        - Problem identified first
                        - Need established first
                        - Insight revealed first
                    
                    2. CTA PLACEMENT:
                        - CTA comes after context
                        - Logical flow
                        - Narrative sequence
                        - Contextually motivated

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "relevant_cta": boolean,
                            "context_element": str,
                            "cta_timing": str,
                            "relevance": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): CTA follows product/problem/need/insight
                    - NOT DETECTED (false): CTA not contextually placed

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear contextual CTA placement
                    - 0.7-0.8: Good relevant CTA
                    - 0.5-0.6: CTA mostly relevant
                    - 0.3-0.4: Weak relevance
                    - 0.0-0.2: CTA not contextually relevant
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_purchase_incentive",
          name="Purchase Incentive (Limited Time/Quantities)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad features limited time or limited quantities messaging 
                    (in both text and/or speech).
                """,
          prompt_template="""
                    Analyze if the ad mentions limited time or quantities.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SCARCITY/URGENCY MESSAGING:
                    
                    DEFINING PURCHASE INCENTIVE:
                    1. TIME LIMIT:
                        - Limited time offer
                        - Today only
                        - Deadline mentioned
                        - Expiration date
                    
                    2. QUANTITY LIMIT:
                        - Limited quantities
                        - While supplies last
                        - Stock limited
                        - Exclusive availability
                    
                    3. DELIVERY MEDIUM:
                        - Text supers
                        - Voice-over
                        - Dialogue

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "incentive_present": boolean,
                            "incentive_type": str,
                            "urgency_level": str,
                            "delivery_method": [str]
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Limited time/quantity message present
                    - NOT DETECTED (false): No scarcity messaging

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear limited time/quantity offer
                    - 0.7-0.8: Good urgency messaging
                    - 0.5-0.6: Some scarcity indication
                    - 0.3-0.4: Weak urgency
                    - 0.0-0.2: No scarcity message
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_special_offer_text",
          name="Special Offer (Text)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if there is any special offer or discount displayed as text in the ad.
                """,
          prompt_template="""
                    Analyze if special offer/discount is displayed as text.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SPECIAL OFFER TEXT:
                    
                    DEFINING SPECIAL OFFER:
                    1. OFFER TYPES:
                        - Discount percentage
                        - Discount amount
                        - Buy one get one
                        - Bundle offers
                        - Special pricing
                    
                    2. TEXT DISPLAY:
                        - Text supers
                        - On-screen text
                        - Clearly visible

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "offer_text_present": boolean,
                            "offer_type": str,
                            "offer_value": str,
                            "text_clarity": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Special offer text visible
                    - NOT DETECTED (false): No offer text displayed

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear special offer text
                    - 0.7-0.8: Good offer visibility
                    - 0.5-0.6: Offer text present but subtle
                    - 0.3-0.4: Minimal offer visibility
                    - 0.0-0.2: No offer text detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
    #   VideoFeature(
    #       id="d_special_offer_speech",
    #       name="Special Offer Speech",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.DIRECT,
    #       video_segment=VideoSegment.FULL_VIDEO,
    #       evaluation_criteria="TODO",
    #       prompt_template="TODO",
    #       extra_instructions=[],
    #       evaluation_method=EvaluationMethod.LLMS,
    #       evaluation_function="",
    #       include_in_evaluation=True,
    #       group_by=VideoSegment.FULL_VIDEO,
    #   ),
      VideoFeature(
          id="d_price_text",
          name="Price (Text)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if any price or cost is displayed as text in the ad.
                """,
          prompt_template="""
                    Analyze if price/cost is displayed as text.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRICE TEXT:
                    
                    DEFINING PRICE:
                    1. PRICE TYPES:
                        - Product price
                        - Service cost
                        - Per unit pricing
                        - Total cost
                        - Discounted price
                    
                    2. TEXT DISPLAY:
                        - Price supers/text
                        - Currency symbol
                        - Numerical amount
                        - On-screen text

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "price_text_present": boolean,
                            "price_values": [str],
                            "currency": str,
                            "text_clarity": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Price displayed as text
                    - NOT DETECTED (false): No price text

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear price text
                    - 0.7-0.8: Good price visibility
                    - 0.5-0.6: Price text present but subtle
                    - 0.3-0.4: Minimal price visibility
                    - 0.0-0.2: No price text detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="d_price_speech",
          name="Price (Speech)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if any price or cost is mentioned in the audio (voice-over or dialogue).
                """,
          prompt_template="""
                    Analyze if price/cost is mentioned in audio/speech.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PRICE IN AUDIO:
                    
                    DEFINING AUDIO PRICE:
                    1. PRICE MENTION:
                        - Voice-over stating price
                        - Character mentioning cost
                        - Clear pronunciation
                        - Understandable amount
                    
                    2. CONTEXT:
                        - Price clarity
                        - Currency mentioned
                        - Per unit or total

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "price_speech_present": boolean,
                            "price_values": [str],
                            "mention_type": str,
                            "clarity": str
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Price mentioned in audio
                    - NOT DETECTED (false): No price mentioned

                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear price mention
                    - 0.7-0.8: Good audio clarity
                    - 0.5-0.6: Price mentioned but subtle
                    - 0.3-0.4: Minimal clarity
                    - 0.0-0.2: No audio price detected
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]

  return feature_configs
