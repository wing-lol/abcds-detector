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
          name="Heartbeat Story (First 3 Seconds)",
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
                    - 0.3-0.4: Weak hook or appears around the 3-second mark
                    - 0.0-0.2: No clear hook or appears after 3 seconds

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
          evaluation_criteria="""
                    Detects if the video contains fast pacing throughout. Fast pacing is defined as 
                    5 or more shots (hard cuts, soft transitions, camera changes, or movement) 
                    occurring within ANY consecutive 3-second window of the video.
                """,
          prompt_template="""
                    Analyze if the short-form video demonstrates fast pacing with 5+ shot changes 
                    in any 3-second consecutive window.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR PACING:
                    Look for rapid shot changes including:
                    1. HARD CUTS:
                        - Abrupt transitions between scenes
                        - Direct scene changes
                        - Immediate subject switches
                    
                    2. SOFT TRANSITIONS:
                        - Fades
                        - Dissolves
                        - Cross-fades
                        - Wipes
                    
                    3. CAMERA CHANGES:
                        - Different camera angles
                        - Zoom in/out
                        - Pan movements
                        - Tilt movements
                    
                    4. MOVEMENT:
                        - Significant subject movement
                        - On-screen action changes
                        - Scene dynamics

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if 5+ shots in any 3-second window
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "pacing_analysis": {{
                                "overall_pacing_speed": str,  # "Slow" | "Moderate" | "Fast"
                                "average_shot_duration": float,  # seconds
                                "fastest_3sec_window": {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "shot_count": int,
                                    "meets_criteria": boolean
                                }},
                                "total_shot_count": int
                            }},
                            "shot_analysis": {{
                                "transition_types": [str],  # "Cut", "Fade", "Dissolve", etc.
                                "camera_movements": [str],
                                "transitions_per_second": float,
                                "consistency": str  # How consistently fast paced
                            }},
                            "pacing_segments": [
                                {{
                                    "start_time": float,
                                    "end_time": float,
                                    "shot_count": int,
                                    "pace_level": str,
                                    "transition_types": [str]
                                }}
                            ],
                            "overall_assessment": {{
                                "meets_fast_pacing_criteria": boolean,
                                "fastest_window_shots": int,
                                "pacing_intensity": str,  # "Very Fast" | "Fast" | "Moderate"
                                "viewer_engagement_impact": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): At least one 3-second window contains 5+ shots
                    - NOT DETECTED (false): No 3-second window contains 5+ shots
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Multiple windows with 6+ shots, very consistent fast pacing
                    - 0.7-0.8: Clear 3-second window with 5+ shots, generally fast-paced
                    - 0.5-0.6: One window with 5+ shots but pacing varies
                    - 0.3-0.4: Some fast segments but inconsistent
                    - 0.0-0.2: Minimal shot changes, slow pacing overall

                    IMPORTANT NOTES:
                    1. Count ALL types of transitions (cuts, fades, camera changes, movement)
                    2. Analyze ANY consecutive 3-second window, not just the beginning
                    3. Movement counts as a shot change when it's significant
                    4. Evaluate throughout entire video for pacing patterns
                    5. Consider viewer engagement impact of pacing choices
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="a_fast_pacing_early",
          name="Fast Pacing Early (first 3 seconds)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the video contains fast pacing within the first 3 seconds. 
                    Fast pacing is defined as 5 or more shot changes (hard cuts, soft transitions, 
                    camera changes, or movement) occurring in the opening 3-second window.
                """,
          prompt_template="""
                    Analyze if the short-form video demonstrates fast pacing in the first 3 seconds 
                    with 5 or more shot changes.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-3.00s) FOR:
                    1. HARD CUTS:
                        - Abrupt transitions between scenes
                        - Direct scene changes
                        - Immediate subject switches
                    
                    2. SOFT TRANSITIONS:
                        - Fades
                        - Dissolves
                        - Cross-fades
                        - Wipes
                    
                    3. CAMERA CHANGES:
                        - Different camera angles
                        - Zoom in/out
                        - Pan movements
                        - Tilt movements
                    
                    4. MOVEMENT:
                        - Significant subject movement
                        - On-screen action changes
                        - Dynamic scene changes

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if 5+ shots in first 3 seconds
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "timing_analysis": {{
                                "first_3_sec_content": str,  # Overall description
                                "shot_count_first_3s": int,
                                "meets_criteria": boolean,
                                "average_shot_duration": float  # seconds
                            }},
                            "shot_breakdown": {{
                                "hard_cuts": int,
                                "soft_transitions": int,
                                "camera_changes": int,
                                "movement_changes": int,
                                "total_transitions": int
                            }},
                            "pacing_details": [
                                {{
                                    "shot_number": int,
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "transition_type": str,
                                    "description": str
                                }}
                            ],
                            "engagement_impact": {{
                                "pacing_intensity": str,  # "Very Fast" | "Fast" | "Moderate"
                                "attention_grabbing": boolean,
                                "viewer_retention_factor": str,  # How likely to retain viewer
                                "early_hook_effectiveness": str
                            }},
                            "overall_assessment": {{
                                "first_3s_pacing_level": str,
                                "shot_density": float,  # shots per second
                                "comparison_to_full_video": str  # If applicable
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): First 3 seconds contain 5 or more distinct shots
                    - NOT DETECTED (false): First 3 seconds contain fewer than 5 shots
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: First 3s has 7+ shots with consistent rapid pacing
                    - 0.7-0.8: First 3s clearly has 5+ shots with evident fast pacing
                    - 0.5-0.6: First 3s has exactly 5 shots or borderline pacing
                    - 0.3-0.4: First 3s has 3-4 shots, slightly under criteria
                    - 0.0-0.2: First 3s has very few shots, slow pacing

                    IMPORTANT NOTES:
                    1. Precisely measure the first 3.00 seconds
                    2. Count ALL transition types equally
                    3. Early pacing sets viewer expectations for entire video
                    4. Quick pacing in first 3s increases likelihood of watch-through
                    5. Consider how early shots introduce content/product
                """,
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
          evaluation_criteria="""
                    Detects if one or more shots showcase the largest subject(s), product(s), 
                    animation(s), environment(s), or any object are tightly framed at any point 
                    during the video. Tight framing means the subject is prominently featured, 
                    filling most of the frame with minimal background or negative space.
                """,
          prompt_template="""
                    Analyze if the short-form video contains tight framing shots where subject(s), 
                    product(s), or key elements are prominently featured and fill most of the frame.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR TIGHT FRAMING:
                    
                    DEFINING TIGHT FRAMING:
                    1. SUBJECT PROMINENCE:
                        - Subject fills majority of frame (60%+ of frame area)
                        - Minimal background or negative space
                        - Clear focus on primary element
                        - Limited distracting elements outside subject
                    
                    2. FRAMING TYPES:
                        - Close-up shots
                        - Macro photography
                        - Zoomed-in perspectives
                        - Cropped compositions
                        - Fill-the-frame compositions
                    
                    3. SUBJECT CATEGORIES:
                        - Product in tight frame
                        - Person's face/upper body tight
                        - Animation or graphic elements
                        - Environmental features (architecture, nature)
                        - Text or design elements
                    
                    4. COMPOSITIONAL CHARACTERISTICS:
                        - Subject extends close to frame edges
                        - Minimal "breathing room" around subject
                        - Intentional close framing (not cropped in error)
                        - Subject remains clearly identifiable

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if 1+ frames with tight framing
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "tight_framing_detection": {{
                                "tight_framing_present": boolean,
                                "frames_with_tight_framing": int,
                                "overall_framing_style": str,  # "Wide" | "Medium" | "Close" | "Tight"
                                "subject_prominence": str  # "Minimal" | "Moderate" | "High" | "Dominant"
                            }},
                            "framing_analysis": {{
                                "primary_subject_type": [str],  # "Product", "Person", "Environment", etc.
                                "frame_fill_percentage": float,  # % of frame filled by subject
                                "background_elements": str,  # How much background visible
                                "framing_consistency": str,  # "Varied" | "Consistent" | "Mixed"
                                "compositional_approach": str  # Style of framing
                            }},
                            "tight_framing_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "subject_type": str,
                                    "fraiming_tightness": str,  # "Loosely framed" | "Medium framed" | "Tightly framed"
                                    "frame_percentage_filled": float,
                                    "description": str
                                }}
                            ],
                            "visual_impact": {{
                                "subject_clarity": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "attention_focus": boolean,
                                "product_visibility": str,  # If product: "Not visible" | "Somewhat visible" | "Clearly visible" | "Dominant"
                                "emotional_connection_potential": str
                            }},
                            "overall_assessment": {{
                                "tight_framing_criteria_met": boolean,
                                "tightest_framing_section": {{
                                    "timestamp": float,
                                    "description": str
                                }},
                                "framing_effectiveness": str,  # "Ineffective" | "Moderate" | "Highly Effective"
                                "viewer_focus_potential": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): One or more shots feature tight framing with subject filling 60%+ of frame
                    - NOT DETECTED (false): All shots feature wide or loose framing with significant background
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Multiple tight framing shots, 70%+ of frame filled, excellent subject prominence
                    - 0.7-0.8: Clear tight framing sections, 60-70% frame fill, good subject emphasis
                    - 0.5-0.6: Some tight framing but minimal background still visible
                    - 0.3-0.4: Occasional tight shots but mostly medium/wide framing
                    - 0.0-0.2: Primarily wide/loose framing, minimal tight shots if any

                    IMPORTANT NOTES:
                    1. Subject must fill majority of frame (60%+) to qualify as "tight"
                    2. Look for ANY subject type: product, person, environment, animation, etc.
                    3. Even brief tight-framed moments count toward detection
                    4. Evaluate framing intention - intentional close composition, not accidental crops
                    5. Consider how tight framing creates focus and viewer engagement
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="a_tight_framing_early",
          name="Tight Framing Early (first 3 seconds)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if one or more shots showcase the largest subject(s), product(s), 
                    animation(s), environment(s), or any object are tightly framed within the 
                    first 3 seconds of the video. Tight framing means the subject fills most 
                    of the frame with minimal background.
                """,
          prompt_template="""
                    Analyze if the short-form video contains tight framing shots in the first 
                    3 seconds where key elements fill most of the frame.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE THE FIRST 3 SECONDS (0-2.99s) FOR TIGHT FRAMING:
                    
                    DEFINING TIGHT FRAMING:
                    1. SUBJECT PROMINENCE:
                        - Subject fills majority of frame (60%+ of frame area)
                        - Minimal background or negative space
                        - Clear focus on primary element
                        - Limited distracting elements
                    
                    2. EARLY IMPACT:
                        - Occurs within first 3 seconds
                        - Sets immediate visual focus
                        - Captures viewer attention early
                        - Establishes subject importance
                    
                    3. SUBJECT TYPES:
                        - Product in tight frame
                        - Person's face/upper body
                        - Animation or graphic elements
                        - Environmental or architectural features
                        - Key visual elements
                    
                    4. COMPOSITIONAL APPROACH:
                        - Close-up perspective
                        - Subject extends near frame edges
                        - Intentional intimate framing
                        - Subject clearly identifiable

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if tight framing in first 3 seconds
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "early_framing_detection": {{
                                "tight_framing_in_first_3s": boolean,
                                "first_3s_overall_style": str,  # "Wide" | "Medium" | "Close" | "Tight"
                                "frames_with_tight_framing": int,
                                "when_tight_framing_appears": float  # Timestamp of first tight frame
                            }},
                            "framing_analysis": {{
                                "primary_subject_type": [str],
                                "average_frame_fill_percentage": float,
                                "background_visibility": str,
                                "framing_progression": str,  # How framing changes in first 3s
                                "early_hook_potential": str  # How well early tight framing hooks viewer
                            }},
                            "early_tight_framing_moments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "subject": str,
                                    "tightness_level": str,  # "Medium" | "Tight" | "Very Tight"
                                    "frame_percentage_filled": float,
                                    "description": str
                                }}
                            ],
                            "first_3s_assessment": {{
                                "viewer_engagement_start": str,
                                "subject_clarity": str,
                                "focus_and_attention": str,
                                "retention_potential": str
                            }},
                            "overall_assessment": {{
                                "tight_framing_in_opening": boolean,
                                "meets_first_3s_criteria": boolean,
                                "earliest_tight_shot_timing": float,
                                "early_framing_effectiveness": str,  # "Ineffective" | "Moderate" | "Highly Effective"
                                "immediate_visual_focus": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Tight framing (60%+ frame fill) appears within first 3 seconds
                    - NOT DETECTED (false): First 3 seconds feature wide/loose framing throughout
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Tight framing within first 1-2 seconds, subject dominates frame
                    - 0.7-0.8: Tight framing appears within first 3 seconds, clear tight composition
                    - 0.5-0.6: Somewhat tight framing in first 3s but with visible background
                    - 0.3-0.4: Only brief moments of tightness or appears right at 3-second mark
                    - 0.0-0.2: No tight framing in first 3 seconds at all

                    IMPORTANT NOTES:
                    1. Frame timing is critical - must occur within first 3.00 seconds
                    2. Early tight framing creates strong hook and viewer interest
                    3. Subject should fill minimum 60% of frame area
                    4. First impression sets tone for entire video watch
                    5. Consider how early framing impacts viewer retention
                """,
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
          evaluation_criteria="""
                    Detects if the video includes any audible sound throughout the duration. 
                    Sound includes music, sound effects (water splashing, 'crunch' sounds, etc.), 
                    voice-over, dialogue, ambient audio, or any other audio track.
                """,
          prompt_template="""
                    Analyze if the short-form video contains any audible sound or audio track.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR AUDIO ELEMENTS:
                    1. MUSIC:
                        - Background music
                        - Licensed tracks
                        - Original compositions
                        - Music beat patterns
                    
                    2. SOUND EFFECTS:
                        - Water splashing
                        - Crunch sounds
                        - Whoosh transitions
                        - Impact sounds
                        - Environmental sounds
                    
                    3. VOICE & DIALOGUE:
                        - Voice-over narration
                        - Character dialogue
                        - Spoken text
                        - Ambient speech
                    
                    4. OTHER AUDIO:
                        - Ambient sounds
                        - Natural environmental audio
                        - Mechanical sounds
                        - Any identifiable audio track

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if any sound is present
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "audio_presence": {{
                                "has_audio": boolean,
                                "audio_type": str,  # "Music", "SFX", "Voice", "Mixed", "Ambient"
                                "audio_coverage": str,  # "Partial" | "Throughout" | "Strategic"
                                "audio_prominence": str  # "Background" | "Mid-level" | "Prominent" | "Dominant"
                            }},
                            "audio_breakdown": {{
                                "has_music": boolean,
                                "music_type": [str],
                                "has_sound_effects": boolean,
                                "sfx_types": [str],
                                "has_voice": boolean,
                                "voice_type": str,  # "VO", "Dialogue", "Speech", "Ambient"
                                "has_ambient_audio": boolean,
                                "ambient_types": [str]
                            }},
                            "audio_timeline": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "audio_type": str,
                                    "description": str,
                                    "prominence": str
                                }}
                            ],
                            "audio_quality": {{
                                "clarity": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "volume_level": str,  # "Low" | "Medium" | "High"
                                "audio_mixing": str,  # "Unbalanced" | "Balanced" | "Well-mixed"
                                "professional_level": str  # "Amateur" | "Semi-pro" | "Professional"
                            }},
                            "overall_assessment": {{
                                "audio_present": boolean,
                                "audio_contributes_to_message": boolean,
                                "audio_effectiveness": str,  # "Ineffective" | "Moderate" | "Highly Effective"
                                "enhances_viewer_experience": boolean
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Any identifiable sound or audio is present
                    - NOT DETECTED (false): Video is completely silent with no audio track
                    
                    CONFIDENCE SCORING:
                    - 0.95-1.0: Clear, prominent audio throughout entire video
                    - 0.8-0.9: Audio present most of video, clear and audible
                    - 0.6-0.7: Audio present but intermittent or subtle
                    - 0.4-0.5: Very minimal audio, barely audible
                    - 0.0-0.3: Essentially silent or audio completely absent

                    IMPORTANT NOTES:
                    1. Even faint or subtle audio counts as sound being present
                    2. Music, effects, and voice are all valid forms of sound
                    3. Silence within video segments doesn't negate overall sound presence
                    4. Evaluate the entire video duration, not just portions
                    5. Consider audio quality and how it contributes to message
                """,
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
          evaluation_criteria="""
                    Detects if the video contains any background music, licensed tracks, 
                    original compositions, or music with beat patterns at any point during 
                    the video duration.
                """,
          prompt_template="""
                    Analyze if the short-form video contains any music or musical audio tracks.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR MUSIC:
                    
                    DEFINING MUSIC:
                    1. MUSIC TYPES:
                        - Background music
                        - Licensed music tracks
                        - Original compositions
                        - Music with identifiable beat/rhythm
                        - Instrumental music
                        - Music with vocals
                    
                    2. MUSIC CHARACTERISTICS:
                        - Identifiable melody or harmony
                        - Rhythmic beat patterns
                        - Instrumental or vocal performances
                        - Genre identifiable (pop, rock, electronic, etc.)
                        - Music distinct from sound effects or speech
                    
                    3. MUSIC COVERAGE:
                        - Throughout entire video
                        - Intermittent music segments
                        - Opening/closing music
                        - Background during dialogue
                        - Strategic music moments
                    
                    4. MUSIC CONTEXT:
                        - Supports brand/product message
                        - Creates emotional tone
                        - Enhances viewer engagement
                        - Complements visual content

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "music_presence": {{
                                "has_music": boolean,
                                "music_type": str,
                                "music_coverage": str,
                                "music_prominence": str
                            }},
                            "music_analysis": {{
                                "music_genre": [str],
                                "has_recognizable_beat": boolean,
                                "vocal_present": boolean,
                                "instrumental_elements": [str],
                                "music_tone": str
                            }},
                            "music_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "music_type": str,
                                    "genre": str,
                                    "duration": float,
                                    "description": str
                                }}
                            ],
                            "music_quality": {{
                                "clarity": str,
                                "production_quality": str,
                                "audio_mix_quality": str,
                                "volume_level": str
                            }},
                            "music_effectiveness": {{
                                "supports_message": boolean,
                                "emotional_impact": str,
                                "brand_alignment": str,
                                "viewer_engagement_factor": str
                            }},
                            "overall_assessment": {{
                                "music_present": boolean,
                                "total_music_duration": float,
                                "music_quality_rating": str,
                                "music_effectiveness": str,
                                "creative_impact": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Any identifiable music track or musical audio present
                    - NOT DETECTED (false): No music present, only dialogue, effects, or silence
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear music throughout or in major portions
                    - 0.8-0.9: Good music present, professional quality
                    - 0.6-0.7: Music present but minimal or lower quality
                    - 0.4-0.5: Very faint music or ambient musical elements only
                    - 0.0-0.3: No identifiable music or essentially silent

                    IMPORTANT NOTES:
                    1. Distinguish music from sound effects or ambient audio
                    2. Identifiable melody/beat indicates music
                    3. Even background music counts
                    4. Licensed and original compositions both count
                    5. Evaluate how music contributes to overall effectiveness
                """,
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
          evaluation_criteria="""
                    Detects if the video contains any sound effects such as water splashing, 
                    crunch sounds, whoosh transitions, impact sounds, or other deliberate 
                    audio effects (not music or voice) at any point during the video.
                """,
          prompt_template="""
                    Analyze if the short-form video contains sound effects or deliberate audio effects.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SOUND EFFECTS:
                    
                    DEFINING SOUND EFFECTS:
                    1. SOUND EFFECT TYPES:
                        - Impact/collision sounds (crashes, booms, hits)
                        - Transition effects (whoosh, swipe, zip sounds)
                        - Environmental effects (water, wind, fire, rain)
                        - Material sounds (crunch, splash, pour, rustle)
                        - Mechanical sounds (beeps, clicks, machinery)
                        - Creature/animal sounds (footsteps, growls)
                    
                    2. EFFECT CHARACTERISTICS:
                        - Synthetic or recorded audio
                        - Deliberate placement with visual moments
                        - Designed to enhance/emphasize action
                        - Distinct from background music
                        - Distinct from dialogue/voice
                    
                    3. TIMING & PLACEMENT:
                        - Synchronized with visual elements
                        - Emphasizes cuts or transitions
                        - Highlights product interactions
                        - Creates rhythm or pacing
                        - Adds dramatic effect

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,
                        "confidence_score": float,
                        "evaluation": {{
                            "effect_presence": {{
                                "has_sound_effects": boolean,
                                "effect_types": [str],
                                "effect_coverage": str,
                                "effect_prominence": str
                            }},
                            "effect_analysis": {{
                                "impact_sounds_present": boolean,
                                "transition_effects_present": boolean,
                                "environmental_effects_present": boolean,
                                "material_sounds_present": boolean,
                                "mechanical_sounds_present": boolean,
                                "distinct_effect_count": int
                            }},
                            "effect_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "effect_type": str,
                                    "effect_name": str,
                                    "visual_context": str,
                                    "synchronization": str,
                                    "description": str
                                }}
                            ],
                            "effect_quality": {{
                                "clarity": str,
                                "production_quality": str,
                                "audio_mix_quality": str,
                                "timing_accuracy": str
                            }},
                            "effect_sync": {{
                                "visual_alignment": str,
                                "timing_precision": boolean,
                                "supports_action": boolean,
                                "enhances_engagement": boolean
                            }},
                            "overall_assessment": {{
                                "effects_present": boolean,
                                "total_effect_duration": float,
                                "effect_quality_rating": str,
                                "effect_effectiveness": str,
                                "creative_impact": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): One or more distinct sound effects present and audible
                    - NOT DETECTED (false): No sound effects, only music, dialogue, or silence
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Multiple clear, professional effects, well-synchronized
                    - 0.8-0.9: Several good quality effects, mostly well-timed
                    - 0.6-0.7: One or more effects present, decent quality/sync
                    - 0.4-0.5: Subtle or faint effects, minimal impact
                    - 0.0-0.3: No identifiable effects or barely noticeable

                    IMPORTANT NOTES:
                    1. Distinguish effects from background music or ambient sound
                    2. Effects should be intentional, not accidental audio
                    3. Consider visual-audio synchronization
                    4. Evaluate how effects enhance message or create engagement
                    5. Synthetic and natural recorded sounds both count
                    6. Even brief effects count toward detection
                """,
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
          evaluation_criteria="""
                    Detects if a human speaks on-camera with a visible face and clear 
                    audio synchronization. This includes any on-camera dialogue whether 
                    from one speaker.
                """,
          prompt_template="""
                    Analyze if the short-form video features a human speaking on-camera 
                    with a visible face and synchronized audio.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR SINGLE-PERSON DIALOGUE:
                    
                    DEFINING ON-CAMERA DIALOGUE:
                    1. VISIBLE FACE REQUIREMENTS:
                        - Human face clearly visible on-camera
                        - Face is not obscured or turned away
                        - At least 60% of face visible
                        - Face remains identifiable
                        - Not just silhouette or extreme close-up of mouth/eyes
                    
                    2. DIALOGUE CHARACTERISTICS:
                        - Person is speaking/talking
                        - Mouth movements synchronized with audio
                        - Clear speech or voice content
                        - Not just lip movement without audio
                        - Audible and understandable speech
                    
                    3. SPEAKER COUNT:
                        - Single person doing all speaking
                        - No other people speaking in the scene
                        - Narrator remains same throughout
                        - Voice-over does not count unless person is visible speaking
                    
                    4. AUDIO-VISUAL SYNCHRONIZATION:
                        - Lip movements match audio timing
                        - Speech appears natural and synchronized
                        - No obvious dubbing or sync issues
                        - Audio and visual aligned properly

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if single person on-camera dialogue
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "dialogue_detection": {{
                                "on_camera_dialogue_present": boolean,
                                "speaker_count": int,
                                "is_single_speaker": boolean,
                                "face_visibility_percentage": float
                            }},
                            "speaker_analysis": {{
                                "face_visibility": str,  # "Not visible" | "Partially visible" | "Clearly visible" | "Fully visible"
                                "face_prominence": str,  # "Background" | "Secondary" | "Primary" | "Dominant"
                                "speaker_appearance": str,  # Age range, gender, distinctive features if visible
                                "face_expression": str,  # "Neutral" | "Smiling" | "Serious" | "Engaged"
                                "eye_contact_with_camera": boolean
                            }},
                            "audio_synchronization": {{
                                "lip_movement_sync": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "audio_clarity": str,  # "Hard to hear" | "Audible" | "Clear" | "Very clear"
                                "speech_naturalness": str,  # "Unnatural" | "Somewhat awkward" | "Natural" | "Very natural"
                                "no_dubbing_issues": boolean
                            }},
                            "dialogue_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "speaker_visible": boolean,
                                    "face_visibility": str,
                                    "dialog_content_summary": str,
                                    "sync_quality": str,
                                    "duration": float
                                }}
                            ],
                            "engagement_potential": {{
                                "personal_connection": str,  # How personal/relatable is the speaker
                                "credibility": str,  # Speaker appears credible/trustworthy
                                "viewer_attention": str,  # How engaging is the speaker
                                "brand_alignment": str
                            }},
                            "overall_assessment": {{
                                "meets_single_dialogue_criteria": boolean,
                                "total_dialogue_duration": float,  # seconds
                                "face_visibility_consistent": boolean,
                                "audio_sync_quality": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "dialogue_effectiveness": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Single person speaks on-camera with visible face and synchronized audio
                    - NOT DETECTED (false): No on-camera dialogue, face not visible, or audio not synchronized
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear on-camera speech, face clearly visible 80%+ of time, perfect sync
                    - 0.7-0.8: Good on-camera dialogue, face mostly visible, solid audio sync
                    - 0.5-0.6: On-camera dialogue present but face partially hidden or sync issues minor
                    - 0.3-0.4: Some on-camera dialogue but face obscured frequently or sync not great
                    - 0.0-0.2: No visible on-camera dialogue or face not visible

                    IMPORTANT NOTES:
                    1. Face must be clearly visible (at least 60% shown)
                    2. Only single speaker counts for this feature
                    3. Audio and visual must be properly synchronized
                    4. Voice-over alone does not count - speaker must be visible
                    5. Evaluate both face visibility and audio sync quality
                """,
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
          evaluation_criteria="""
                    Detects if multiple people speak on-camera with visible faces and 
                    clear audio synchronization. This requires 2 or more speakers with 
                    faces visible and dialogue that's clearly synchronized to audio.
                """,
          prompt_template="""
                    Analyze if the short-form video features multiple people speaking 
                    on-camera with visible faces and synchronized audio.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR MULTI-PERSON DIALOGUE:
                    
                    DEFINING MULTI-SPEAKER ON-CAMERA DIALOGUE:
                    1. MULTIPLE SPEAKERS:
                        - 2 or more distinct people speaking
                        - Each person has identifiable voice/speech
                        - Different speakers take turns or speak together
                        - All speakers are on-camera (visible)
                    
                    2. VISIBLE FACE REQUIREMENTS:
                        - Each speaker's face is clearly visible
                        - At least 60% of each face is shown
                        - Faces are not obscured or turned away
                        - Faces remain identifiable
                        - When someone speaks, their face should be visible
                    
                    3. DIALOGUE CHARACTERISTICS:
                        - All speakers have audible, clear speech
                        - Dialogue is understandable
                        - Proper synchronization between voice and lips
                        - Natural conversation or interaction
                        - Each speaker distinctly audible
                    
                    4. INTERACTION PATTERNS:
                        - Conversation between people
                        - Turn-taking in dialogue
                        - Natural back-and-forth exchange
                        - Collaborative or confrontational dialogue
                        - Question and answer format
                    
                    5. AUDIO-VISUAL SYNCHRONIZATION:
                        - Lip movements match voice timing for each speaker
                        - Speech appears natural and synchronized
                        - No obvious dubbing issues
                        - Audio clearly tied to visible speakers

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if 2+ people on-camera with dialogue
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "multi_speaker_detection": {{
                                "on_camera_dialogue_present": boolean,
                                "total_speakers": int,
                                "speakers_with_visible_faces": int,
                                "is_multiple_speaker": boolean,
                                "minimum_2_speakers_met": boolean
                            }},
                            "speaker_analysis": [
                                {{
                                    "speaker_number": int,
                                    "appearance_order": str,  # "First", "Second", "Third", etc.
                                    "face_visibility": str,  # "Not visible" | "Partially" | "Clearly visible" | "Fully visible"
                                    "visual_prominence": str,  # "Background" | "Secondary" | "Primary" | "Dominant"
                                    "distinctive_features": str,  # Description of speaker
                                    "face_expression": str,
                                    "screen_time_percentage": float,
                                    "dialogue_duration": float  # seconds speaking
                                }}
                            ],
                            "dialogue_characteristics": {{
                                "interaction_type": str,  # "Conversation" | "Q&A" | "Collaborative" | "Confrontational"
                                "dialogue_flow": str,  # "Natural" | "Scripted" | "Forced" | "Spontaneous"
                                "turn_taking_pattern": str,  # How speakers exchange dialogue
                                "total_dialogue_duration": float,  # seconds
                                "engagement_level": str
                            }},
                            "audio_synchronization": {{
                                "overall_lip_sync_quality": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "speaker_distinction": str,  # How clear each speaker's voice is
                                "audio_clarity": str,  # "Hard to hear" | "Audible" | "Clear" | "Very clear"
                                "no_dubbing_issues": boolean
                            }},
                            "exchange_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "speaker_number": int,
                                    "face_visible": boolean,
                                    "dialogue_content_summary": str,
                                    "sync_quality": str
                                }}
                            ],
                            "engagement_potential": {{
                                "personal_connection": str,
                                "relatability": str,
                                "credibility": str,  # Both speakers appear credible
                                "viewer_interest": str  # How engaging is the interaction
                            }},
                            "overall_assessment": {{
                                "meets_multiple_dialogue_criteria": boolean,
                                "speaker_count_sufficient": boolean,  # At least 2
                                "all_faces_visible": boolean,  # When speaking
                                "audio_video_sync_quality": str,
                                "multi_speaker_effectiveness": str,  # "Ineffective" | "Moderate" | "Highly Effective"
                                "dialogue_impact": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): 2+ people speak on-camera with visible faces and synchronized audio
                    - NOT DETECTED (false): Only 1 speaker, faces not visible, or poor audio sync
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: 3+ speakers, all faces clearly visible when speaking, excellent sync
                    - 0.7-0.8: 2+ speakers, faces mostly visible, good natural dialogue and sync
                    - 0.5-0.6: 2 speakers present but faces sometimes hidden or sync issues minor
                    - 0.3-0.4: 2 speakers but faces partially obscured frequently or sync not great
                    - 0.0-0.2: Fewer than 2 speakers, faces not visible, or no clear dialogue

                    IMPORTANT NOTES:
                    1. Minimum 2 speakers required (not counting voice-over)
                    2. All speakers must have visible faces (at least 60% when speaking)
                    3. Each speaker's dialogue must be audible and clear
                    4. Audio-visual synchronization must be good across all speakers
                    5. Natural dialogue interaction increases effectiveness
                    6. Evaluate when each speaker appears and their visibility
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
    #   VideoFeature(
    #       id="a_direct_camera",
    #       name="Direct Camera Address",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.ATTRACT,
    #       video_segment=VideoSegment.FULL_VIDEO,
    #       evaluation_criteria="TODO",
    #       prompt_template="TODO",
    #       extra_instructions=[],
    #       evaluation_method=EvaluationMethod.LLMS,
    #       evaluation_function="",
    #       include_in_evaluation=True,
    #       group_by=VideoSegment.FULL_VIDEO,
    #   ),
    #   VideoFeature(
    #       id="a_has_supers",
    #       name="Has Supers",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_supers_combined",
          name="Text Supers aligned with Audio",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the speech heard in the ad matches or is contextually supportive 
                    of the overlaid text shown on screen. This feature evaluates how well text 
                    supers align with and reinforce the audio message being delivered.
                """,
          prompt_template="""
                    Analyze if the speech heard in the ad matches or is contextually supportive 
                    of the overlaid text shown on screen.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR AUDIO-TEXT ALIGNMENT:
                    
                    DEFINING AUDIO-TEXT MATCH:
                    1. DIRECT MATCH:
                        - Text overlay contains exact words being spoken
                        - Speech and text appear simultaneously
                        - Clear repetition of message through dual channels
                        - Text emphasizes key spoken phrases
                        - Identical or nearly identical wording
                    
                    2. CONTEXTUAL SUPPORT:
                        - Text reinforces the meaning of spoken content
                        - Text provides additional context to speech
                        - Text summarizes key points being discussed
                        - Text elaborates on spoken message
                        - Text and speech complement each other thematically
                    
                    3. TIMING & SYNC:
                        - Text appears when relevant audio is spoken
                        - Text stays on screen during relevant speech
                        - Synchronized display of visual and audio information
                        - Text transitions align with topic changes
                        - No conflicting or unrelated information timing
                    
                    4. COMMUNICATION EFFECTIVENESS:
                        - Dual reinforcement strengthens message
                        - Accessibility for hearing-impaired viewers
                        - Improved information retention
                        - Better engagement through multi-sensory delivery
                        - Clarity and understanding enhanced

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if text and audio match or support each other
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "audio_text_presence": {{
                                "has_text_overlay": boolean,
                                "has_relevant_speech": boolean,
                                "audio_text_interaction_present": boolean,
                                "total_text_duration": float
                            }},
                            "alignment_analysis": {{
                                "match_type": str,  # "Direct Match" | "Contextual Support" | "None" | "Conflicting"
                                "match_coverage": float,  # % of text that aligns with audio
                                "alignment_quality": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "consistency": str,  # How consistently text and audio align
                                "reinforcement_level": str  # "Weak" | "Moderate" | "Strong" | "Very Strong"
                            }},
                            "text_audio_segments": [
                                {{
                                    "start_timestamp": float,
                                    "end_timestamp": float,
                                    "text_content": str,
                                    "audio_content_summary": str,
                                    "alignment_type": str,  # "Direct Match" | "Contextual Support" | "Unrelated"
                                    "alignment_quality": str,
                                    "description": str
                                }}
                            ],
                            "audio_characteristics": {{
                                "speech_present": boolean,
                                "dialogue_type": str,  # "VO", "On-camera", "Dialogue", "Mixed"
                                "clarity": str,  # "Clear" | "Moderately clear" | "Unclear"
                                "content_relevance": str  # How relevant is audio to overall message
                            }},
                            "text_characteristics": {{
                                "text_types": [str],  # "Caption", "Logo", "CTA", "Product Name", "Key Message"
                                "font_size": str,  # "Small" | "Medium" | "Large" | "Very Large"
                                "readability": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "duration_adequate": boolean  # Time on screen sufficient to read
                            }},
                            "overall_assessment": {{
                                "audio_text_aligned": boolean,
                                "alignment_strength": str,  # "Weak" | "Moderate" | "Strong" | "Very Strong"
                                "message_reinforcement": boolean,
                                "effectiveness": str,  # "Ineffective" | "Moderate" | "Highly Effective"
                                "viewer_engagement_potential": str,
                                "accessibility_level": str  # How accessible for all viewers
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): Speech and text overlay match or contextually support each other
                    - NOT DETECTED (false): No text overlay, no relevant speech, or conflicting information
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: Clear direct match or strong contextual support, excellent alignment
                    - 0.7-0.8: Good alignment between speech and text, mostly matching or supportive
                    - 0.5-0.6: Some alignment but not consistent or only partial match
                    - 0.3-0.4: Minimal alignment, mostly unrelated text and speech
                    - 0.0-0.2: No text, no speech, or completely conflicting information

                    IMPORTANT NOTES:
                    1. Evaluate both direct word matches and contextual support
                    2. Consider timing - text should appear during relevant speech
                    3. Assess readability and screen time adequacy
                    4. Evaluate how well dual channels reinforce the message
                    5. Consider accessibility benefits for hearing-impaired viewers
                    6. Look for consistent alignment throughout video
                    7. Quality of alignment matters as much as presence
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
    #   VideoFeature(
    #       id="a_supers_audio_augment",
    #       name="Supers Audio Augmentation",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.ATTRACT,
    #       video_segment=VideoSegment.FULL_VIDEO,
    #       evaluation_criteria="TODO",
    #       prompt_template="TODO",
    #       extra_instructions=[],
    #       evaluation_method=EvaluationMethod.LLMS,
    #       evaluation_function="",
    #       include_in_evaluation=True,
    #       group_by=VideoSegment.FULL_VIDEO,
    #   ),
    #   VideoFeature(
    #       id="a_supers_audio_match",
    #       name="Supers Audio Matching",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.ATTRACT,
    #       video_segment=VideoSegment.FULL_VIDEO,
    #       evaluation_criteria="TODO",
    #       prompt_template="TODO",
    #       extra_instructions=[],
    #       evaluation_method=EvaluationMethod.LLMS,
    #       evaluation_function="",
    #       include_in_evaluation=True,
    #       group_by=VideoSegment.FULL_VIDEO,
    #   ),
    #   VideoFeature(
    #       id="a_large_supers",
    #       name="Large Supers",
    #       category=VideoFeatureCategory.SHORTS,
    #       sub_category=VideoFeatureSubCategory.ATTRACT,
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
          id="a_bright_colors",
          name="Bright Colors",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                    Detects if the ad incorporates bright, vibrant, and vivid colors on at least 
                    2 or more different frames. Bright visuals are characterized by high saturation, 
                    vivid hues, and colors that stand out visually from the background.
                """,
          prompt_template="""
                    Analyze if the short-form video incorporates bright colors on at least 2+ different frames.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR BRIGHT VISUALS:
                    
                    DEFINING BRIGHT COLORS:
                    1. COLOR CHARACTERISTICS:
                        - High saturation (vivid, not muted)
                        - Vibrant hues
                        - Stand out from background
                        - Noticeable visual impact
                        - Not washed out or desaturated
                    
                    2. BRIGHT COLOR TYPES:
                        - Bright reds, pinks, magentas
                        - Bright yellows, golds, oranges
                        - Bright blues, cyans, electric colors
                        - Bright greens, limes, neon colors
                        - Bright purples, violets
                        - Any high-saturation vivid color
                    
                    3. BRIGHT VISUAL ELEMENTS:
                        - Product in bright colors
                        - Clothing in bright colors
                        - Background elements in bright colors
                        - Lighting effects with bright colors
                        - Color transitions to bright shades
                    
                    4. FRAME REQUIREMENTS:
                        - Must appear on at least 2 separate frames
                        - Frames should show meaningful bright color presence
                        - Not just quick flashes or minimal appearances

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if 2+ frames with bright colors
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "bright_color_presence": {{
                                "frames_with_bright_colors": int,
                                "meets_2plus_criteria": boolean,
                                "overall_color_palette": str,  # Description
                                "brightness_level": str  # "Muted" | "Moderate" | "Vivid" | "Bright"
                            }},
                            "color_analysis": {{
                                "primary_bright_colors": [str],  # "Red", "Blue", "Yellow", etc.
                                "secondary_bright_colors": [str],
                                "color_saturation_level": str,  # "Low" | "Medium" | "High" | "Very High"
                                "color_dominance": str,  # How prominent are bright colors
                                "color_consistency": str  # Throughout video or specific moments
                            }},
                            "bright_color_frames": [
                                {{
                                    "frame_number": int,
                                    "timestamp": float,
                                    "bright_colors_present": [str],
                                    "color_saturation": str,
                                    "coverage_percentage": float,  # % of frame with bright colors
                                    "description": str
                                }}
                            ],
                            "visual_impact": {{
                                "attention_grabbing": boolean,
                                "color_effectiveness": str,  # "Low" | "Moderate" | "High"
                                "emotional_response_potential": str,
                                "brand_alignment": str  # How well colors align with brand
                            }},
                            "overall_assessment": {{
                                "bright_colors_present": boolean,
                                "minimum_frame_count_met": boolean,
                                "visual_brightness_rating": str,  # "Dim" | "Moderate" | "Bright" | "Very Bright"
                                "creative_effectiveness": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): 2 or more frames contain bright, vibrant colors
                    - NOT DETECTED (false): Fewer than 2 frames with bright colors, or colors are muted/desaturated
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: 4+ frames with very bright, vivid colors; high visual impact
                    - 0.7-0.8: 2-3 frames with clearly bright colors throughout
                    - 0.5-0.6: 2 frames with bright colors but some are less vivid
                    - 0.3-0.4: Only 2 frames borderline bright, mostly muted palette
                    - 0.0-0.2: Fewer than 2 bright frames or predominantly desaturated colors

                    IMPORTANT NOTES:
                    1. Colors must be BRIGHT and VIBRANT, not just saturated
                    2. Must appear on at least 2 DIFFERENT frames (not same frame repeated)
                    3. Consider both primary subject matter and background elements
                    4. Evaluate color saturation, not just color presence
                    5. Bright colors should create visual interest and grab attention
                    6. Consider how lighting affects color brightness perception
                """,
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
          evaluation_criteria="""
                    Detects if the ad has high color contrast on at least 2 or more different frames. 
                    High contrast means there is a significant contrast difference between colors, 
                    ensuring clear visibility and distinction between elements, including black & white, 
                    light & dark, and complementary colors.
                """,
          prompt_template="""
                    Analyze if the short-form video contains high color contrast on 2+ different frames.

                    VIDEO METADATA:
                    {metadata_summary}

                    ANALYZE FOR HIGH CONTRAST VISUALS:
                    
                    DEFINING HIGH CONTRAST:
                    1. CONTRAST TYPES:
                        - Black & white combinations
                        - Light colors against dark backgrounds
                        - Dark colors against light backgrounds
                        - Complementary colors (opposite on color wheel)
                        - High saturation differences
                        - Bright against muted colors
                    
                    2. CONTRAST CHARACTERISTICS:
                        - Significant visual difference between elements
                        - Clear distinction and separation
                        - High perceivable difference (not subtle)
                        - Creates visual pop or visual interest
                        - Makes elements stand out clearly
                    
                    3. CONTRAST CATEGORIES:
                        - Luminance contrast (light vs dark)
                        - Chromatic contrast (different colors)
                        - Saturation contrast (saturated vs muted)
                        - Value contrast (brightness levels)
                        - Color complement contrast
                    
                    4. FRAME REQUIREMENTS:
                        - Must appear on 2+ separate frames
                        - Different frames showing contrasting elements
                        - Not same frame duplicated
                        - Clear contrast visibility in each frame

                    FORMAT RESPONSE AS JSON:
                    {{
                        "detected": boolean,  # TRUE if 2+ frames with high contrast
                        "confidence_score": float,  # 0.0-1.0
                        "evaluation": {{
                            "contrast_presence": {{
                                "high_contrast_frames": int,
                                "meets_2plus_criteria": boolean,
                                "overall_contrast_level": str,  # "Low" | "Moderate" | "High" | "Very High"
                                "contrast_consistency": str  # "Sparse" | "Intermittent" | "Frequent" | "Throughout"
                            }},
                            "contrast_analysis": {{
                                "contrast_types_present": [str],  # "Black & White", "Luminance", "Chromatic", etc.
                                "primary_contrast_elements": [str],  # What's contrasting
                                "luminance_contrast_level": str,  # "Low" | "Medium" | "High" | "Very High"
                                "color_contrast_level": str,
                                "overall_visibility": str,  # How clear is the contrast
                                "visual_impact": str  # "Low" | "Moderate" | "High" | "Striking"
                            }},
                            "contrast_frames": [
                                {{
                                    "frame_number": int,
                                    "timestamp": float,
                                    "contrast_type": [str],
                                    "contrasting_elements": str,  # What's contrasting
                                    "contrast_intensity": str,  # "Subtle" | "Moderate" | "Strong" | "Very Strong"
                                    "background_color": str,
                                    "foreground_color": str,
                                    "luminance_difference": float,  # 0-100% estimated
                                    "description": str
                                }}
                            ],
                            "contrast_characteristics": {{
                                "black_white_present": boolean,
                                "light_dark_contrast": boolean,
                                "complementary_colors": boolean,
                                "saturation_differences": str,
                                "color_vibrancy_contribution": str
                            }},
                            "visual_effectiveness": {{
                                "readability": str,  # "Poor" | "Fair" | "Good" | "Excellent"
                                "visual_clarity": str,  # How clear are contrasting elements
                                "attention_grabbing": boolean,
                                "element_distinction": str,  # How well distinguished are elements
                                "viewer_focus": str
                            }},
                            "overall_assessment": {{
                                "high_contrast_criteria_met": boolean,
                                "minimum_frame_count_met": boolean,
                                "contrast_strength": str,  # "Weak" | "Moderate" | "Strong" | "Very Strong"
                                "contrast_effectiveness": str,  # "Ineffective" | "Moderate" | "Highly Effective"
                                "visual_design_quality": str
                            }}
                        }},
                        "notes": str
                    }}

                    EVALUATION CRITERIA:
                    - DETECTED (true): 2 or more frames contain high contrast with clear visual distinction
                    - NOT DETECTED (false): Fewer than 2 frames with contrast, or contrast is low/subtle
                    
                    CONFIDENCE SCORING:
                    - 0.9-1.0: 4+ frames with very high contrast, striking visual differences, excellent distinction
                    - 0.7-0.8: 2-3 frames with clearly high contrast, strong visual separation
                    - 0.5-0.6: 2 frames with decent contrast but some elements less distinct
                    - 0.3-0.4: 2 frames with borderline/subtle contrast, distinction could be clearer
                    - 0.0-0.2: Fewer than 2 frames with contrast, or predominantly low-contrast palette

                    IMPORTANT NOTES:
                    1. Contrast must be HIGH and NOTICEABLE, not subtle or low
                    2. Must appear on at least 2 DIFFERENT frames (not same frame repeated)
                    3. Include all contrast types: luminance, chromatic, saturation, value
                    4. Black & white is a strong example of high contrast
                    5. Evaluate how contrast aids visibility and visual clarity
                    6. Consider complementary colors as high contrast source
                    7. Assess how contrast contributes to overall visual design quality
                """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]

  return feature_configs
