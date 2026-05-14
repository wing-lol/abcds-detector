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

BASE_RESPONSE_FORMAT = """
            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; {density_description})
            - feature_quality_score: float (0.0 to 1.0; {quality_description})
            - feature_specifics: object containing:
{specifics_descriptions}

            **OUTPUT STRUCTURE:**
            {{
                "detected": true,
                "detected_confidence_score": 0.95,
                "detected_evidence": "string",
                "key_driver_category": "string",
                "recommended_actions": "string",
                "strengths_to_keep": "string",
                "first_appearance_timestamp": 2.5,
                "feature_density_score": 0.5,
                "feature_quality_score": 0.8,
                "feature_specifics": {{
{specifics_json}
                }}
            }}
"""


def get_shorts_feature_configs() -> list[VideoFeature]:
  """Gets all the supported ABCD/Shorts features.

  Returns original shorts features PLUS new organized ABCD features
  (Attract, Brand, Connect, Direct, Other)

  Returns:
      feature_configs: list of feature configurations

  feature_configs: list of feature configurations
  """
  # Get original shorts features
  feature_configs = [
      VideoFeature(
          id="tight_framing_index",
          name="Tight Framing & Visual Dominance",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                Quantifies the spatial dominance of the primary subject.
                Tight framing is defined by a Subject-to-Frame Ratio (SfR) of ≥60%.
                The score reflects the 'Density' (persistence) of tight framing, 
                differentiating between incidental close-ups and thematic visual dominance.
            """,
          prompt_template="""
                Act as a professional Cinematographer and Video Analyst. Your goal is to measure
                'Visual Weight' through Tight Framing detection.
            
                VIDEO METADATA: {metadata_summary}

                ### 1. SHOT CLASSIFICATION (for reference):
                - Extreme Close-Up (ECU): Subject fills >80% of frame.
                - Close-Up (CU): Subject fills 60%-80% of frame.
                - Medium Shot (MS): Subject fills 30%-59% of frame.
                - Wide/Long Shot (LS): Subject fills <30% of frame.

                ### 2. EVALUATION LOGIC:
                1. Set detected_confidence_score: Score from 0.0 to 1.0 based on
                   how clearly the subject fills the frame and how unambiguous the shot
                   type is (regardless of duration).
                2. Detection Decision: Set `detected` to True if
                   `detected_confidence_score` >= 0.4. Otherwise set to False.
                3. Calculate feature_density_score: (Total CU+ECU duration) /
                   (Total video duration) = raw float value between 0.0 and 1.0.
                4. Calculate feature_quality_score: 
                   - Base score on the "Goldilocks Zone" of density (ideal is 30%-60%).
                   - Give a bonus if the first 3 seconds (The Hook) contain tight framing.
                   - Score from 0.0 to 1.0 reflecting effectiveness.
                5. Rationale & Evidence: Cite specific timestamps and shot durations.
"""
          + BASE_RESPONSE_FORMAT.format(
              density_description="proportion of video in CU/ECU",
              quality_description="effectiveness of tight framing",
              specifics_descriptions="""                    - peak_sfr_percentage: float (highest ratio observed)
                    - primary_subject_class: string (e.g., Product, Human_Face)
                    - framing_cadence: string (e.g., Static, Fast-Cutting)""",
              specifics_json="""                    "peak_sfr_percentage": 0.85,
                    "primary_subject_class": "Product",
                    "framing_cadence": "Static" """,
          ),
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_human_voice",
          name="Human Voice Presence",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Quantifies the presence, duration, and quality of human speech. 
            Voice includes Voice-Overs (VO), direct-to-camera dialogue, or background 
            narration. The metric measures 'Vocal Density' (percentage of video containing 
            speech) and assesses the clarity and role of the speaker.
        """,
          prompt_template="""
            Act as a professional Cinematographer and Video Analyst. 
            Your goal is to analyze the audio track of this video specifically for human vocal presence.

            VIDEO METADATA: {metadata_summary}

            ### 1. DEFINITIONS (for reference):
            - Voice Over (VO): Narrative voice added in post-production.
            - Dialogue: On-camera person speaking.
            - Ambient Speech: Overheard background talking.
            - Synthetic/AI Voice: Clear AI-generated narration (text-to-speech).
            - Vocal Clarity: The ease with which the voice is understood (0.0 - 1.0). 
              High score = studio quality/clear; Low score = muffled, heavy background noise.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how clearly the 
               voice is audible and identifiable (regardless of duration). High score for clear, 
               isolated voice; lower score for muffled voice or heavy background noise overlap.
            2. Detection Decision: Set `detected` to True if `detected_confidence_score` >= 0.4. 
               Otherwise set to False.
            3. Calculate feature_density_score: (Total duration of audible human speech) / 
               (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Vocal Clarity (0.0 to 1.0).
               - Give a bonus (+0.1) if the speech starts in the first 3 seconds (The Hook).
               - Score from 0.0 to 1.0 reflecting effectiveness.
            5. Rationale & Evidence: Cite specific timestamps and durations.

            ### 3. FORMAT RESPONSE AS JSON:
"""
          + BASE_RESPONSE_FORMAT.format(
              density_description=(
                  "calculated as (Total Speech Time / Total Duration)"
              ),
              quality_description="effectiveness based on clarity and hook",
              specifics_descriptions="""                - vocal_clarity_score: float
                - primary_voice_type: string (e.g., Voice_Over, Dialogue, Mixed)
                - speech_cadence: string (e.g., Constant, Intermittent, Rapid, Slow)
                - background_noise_level: string (e.g., Low, Medium, High)""",
              specifics_json="""                    "vocal_clarity_score": 0.8,
                    "primary_voice_type": "Voice_Over",
                    "speech_cadence": "Constant",
                    "background_noise_level": "Low" """,
          ),
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_direct_to_camera",
          name="Direct to Camera",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
                Quantifies the duration and intensity of direct eye contact between the 
                on-screen subject and the camera lens. This feature measures the 
                'Direct Address Density' and assesses the intimacy of the framing 
                (e.g., face-to-face address).
            """,
          prompt_template="""
                Act as a professional Cinematographer and Video Analyst. 
                Your goal is to analyze the video for instances where a person looks 
                directly into the camera lens to address the viewer.

                VIDEO METADATA: {metadata_summary}

                ### 1. ADDRESS MODES (for reference):
                - Direct Address: Subject is looking into the lens and speaking.
                - Silent Gaze: Subject maintains eye contact without speaking.
                - Glance: Brief, intermittent eye contact (less than 0.5s).
                - Off-Camera: Subject is looking at a secondary point, not the viewer.

                ### 2. EVALUATION LOGIC:
                1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
                   clearly the subject's pupils are directed at the camera lens (regardless 
                   of duration). High score for locked gaze; lower score if looking at 
                   scripts/monitors or if eyes are blurry.
                2. Detection Decision: Set `detected` to True if 
                   `detected_confidence_score` >= 0.4. Otherwise set to False.
                3. Calculate feature_density_score: (Total duration of direct eye 
                   contact / address) / (Total video duration) = raw float value between 0.0 and 1.0.
                4. Calculate feature_quality_score: 
                   - Base score on Eye Contact Intensity (0.0 to 1.0).
                   - Give a bonus (+0.1) if direct address starts in the first 2 seconds (Hook).
                   - Score from 0.0 to 1.0 reflecting effectiveness.
                5. Rationale & Evidence: Cite specific timestamps and durations.
"""
          + BASE_RESPONSE_FORMAT.format(
              density_description="proportion of video with direct address",
              quality_description="effectiveness based on intensity and hook",
              specifics_descriptions="""                    - eye_contact_intensity: float
                    - subject_distance: string (e.g., Close-Up, Medium)
                    - address_style: string (e.g., Intimate, Presentational)
                    - emotional_delivery: string""",
              specifics_json="""                    "eye_contact_intensity": 0.9,
                    "subject_distance": "Close-Up",
                    "address_style": "Intimate",
                    "emotional_delivery": "Confident" """,
          ),
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_has_supers",
          name="Supers & Text-Audio Synchronicity",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.ATTRACT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
        Quantifies the presence, accuracy, and synchronization of text overlays (supers) 
        with the spoken audio. This measures 'Text Density' and the 'Synchronicity Score' 
        to determine how effectively the visual text reinforces the spoken message.
    """,
          prompt_template="""
            Act as a professional Cinematographer and Video Analyst. Your goal is to 
            Analyze the video for SUPERS (text overlays) and their relationship to the audio.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. SUPERS CATEGORIES (for reference):
            - Dynamic Captions: Word-by-word or phrase-by-phrase synced text.
            - Static Callouts: Persistent text (e.g., "50% OFF" or "Product Name").
            - Kinetic Typography: Stylized, moving text used for emphasis.
            - Headlines: Large top/bottom text bars that stay throughout the video.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how clearly the text is legible and identifiable as a creative overlay (regardless of duration). High score for clear, contrasty text; lower score for blurry, small, or overlapping text.
            2. Detection Decision: Set `detected` to True if `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Total duration where text overlays are visible) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Synchronicity (how well text matches spoken words) and Readability (0.0 to 1.0).
               - Give a bonus (+0.1) if the text is in the "Mobile Safe Zone".
               - Score from 0.0 to 1.0 reflecting effectiveness.
            5. Rationale & Evidence: Cite specific timestamps and text content.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with 
              text overlays)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on 
              synchronicity and readability)
            - feature_specifics: object containing:
                - synchronicity_score: float
                - text_coverage_ratio: float
                - primary_supers_type: string (e.g., Dynamic_Captions, Headlines)
                - readability_score: float

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "synchronicity_score": float,
                    "text_coverage_ratio": float,
                    "primary_supers_type": string,
                    "readability_score": float
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_product_closeup",
          name="Product Close-Up",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Quantifies segments where the product occupies at least 30% of the frame. 
            This measures standard product visibility and presence within a recognizable 
            context or environment.
        """,
          prompt_template="""
            Act as a professional Cinematographer and Video Analyst. Your goal is to 
            measure 'Product Presence' via Close-Up detection.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. SHOT CLASSIFICATION (for reference):
            - Product Close-Up (CU): Product occupies 30% to 59% of the frame area.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the product is identifiable and in focus (regardless of 
               duration). High score for clear branding and full view; lower 
               score for blurry or obstructed views.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Total duration of Product CU 
               shots) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Product Identifiability (0.0 to 1.0) and Framing 
                 Style (is it centered or following rule of thirds?).
               - Score from 0.0 to 1.0 reflecting effectiveness.
            5. Rationale & Evidence: Cite specific timestamps and shot durations.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with 
              product close-up)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on 
              identifiability and framing)
            - feature_specifics: object containing:
                - average_sfr_percentage: float
                - product_identifiability: float
                - framing_style: string (e.g., Handheld, Studio-Static)

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "average_sfr_percentage": float,
                    "product_identifiability": float,
                    "framing_style": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_product_extreme_closeup",
          name="Product Extreme Close-Up",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.BRAND,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Quantifies segments where the product is the dominant visual element, 
            occupying 60% or more of the frame. This measures 'Macro' focus and 
            high-detail product showcasing.
        """,
          prompt_template="""
            Act as a professional Cinematographer and Video Analyst. Your goal is to 
            measure 'Product Dominance' via Extreme Close-Up (ECU) detection.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. SHOT CLASSIFICATION (for reference):
            - Product Extreme Close-Up (ECU): Product occupies 60% or more of the frame area.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how clearly the product's fine details and textures are visible and in focus (regardless of duration). High score for macro shots showing product quality; lower score for blurry or out-of-focus ECU shots.
            2. Detection Decision: Set `detected` to True if `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Total duration of Product ECU shots) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Texture Visibility and Lighting Quality (0.0 to 1.0).
               - Score from 0.0 to 1.0 reflecting effectiveness in showcasing high detail.
            5. Rationale & Evidence: Cite specific timestamps and shot durations.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with product ECU)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on texture and lighting)
            - feature_specifics: object containing:
                - peak_sfr_percentage: float
                - texture_visibility: string (e.g., Low, Medium, High)
                - lighting_quality: string (e.g., Flat, Cinematic)

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "peak_sfr_percentage": float,
                    "texture_visibility": string,
                    "lighting_quality": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_product_context_index",
          name="Product Context & Usage Quality",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Evaluates the 'Show, Don't Tell' quality. Quantifies physical 
            interaction, environmental realism, and utility demonstration. 
            Measures both the duration of usage (Density) and the effectiveness 
            of the demonstration (Quality Score).   
            """,
          prompt_template="""
            Act as a professional Cinematographer and Video Analyst. 
            Analyze the 'Product-in-Use' effectiveness.

            VIDEO METADATA:
            {metadata_summary}

            ### 1. SCORE DIMENSIONS (for reference):
            - INTERACTION DEPTH (40% weight): Physical contact and active engagement.
            - CONTEXTUAL REALISM (30% weight): "Lived-in" space vs. sterile studio.
            - UTILITY DEMONSTRATION (30% weight): Shows product's purpose/benefit.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly identifiable the product and its usage are (regardless of 
               duration or quality score). High score for clear, unambiguous 
               demonstration; lower score for blurry or obscured usage.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of active product usage) 
               / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Score each of the three dimensions in Step 1 from 0 to 100.
               - Calculate the weighted total: `(Interaction Depth * 0.40) + 
                 (Contextual Realism * 0.30) + (Utility Demonstration * 0.30)`.
               - Divide the weighted total by 100 to get the final 
                 `feature_quality_score` as a float between 0.0 and 1.0.
            5. Rationale & Evidence: Cite specific timestamps and actions 
               supporting the scores.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with 
              active product usage)
            - feature_quality_score: float (0.0 to 1.0; weighted average of quality 
              dimensions)
            - feature_specifics: object containing:
                - interaction_depth_score: int
                - contextual_realism_score: int
                - utility_demo_score: int

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "interaction_depth_score": int,
                    "contextual_realism_score": int,
                    "utility_demo_score": int
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_casual_language",
          name="Casual Language",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Quantifies the informality of the script. Measures the use of everyday language, 
            slang, contractions, and conversational filler vs. formal/corporate scripted speech.
        """,
          prompt_template="""
            Act as a Linguistic and Video Analyst. Your goal is to measure 
            'Tone Informality.'

            VIDEO METADATA:
            {metadata_summary}

            ### 1. DEFINITIONS (for reference):
            - Informality Rating: (0.0 - 1.0) 1.0 = "POV/FaceTime" style; 
              0.5 = Standard commercial; 0.0 = Corporate/Medical.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can identify slang, filler words, or conversational 
               structures (regardless of duration). High score for clear audio 
               and obvious slang; lower score for ambiguous or subtle informality.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of conversational/casual 
               speech) / (Total speech duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on the Informality Rating (0.0 to 1.0). Higher score 
                 for more casual/authentic tone.
               - Score from 0.0 to 1.0 reflecting effectiveness in sounding native.
            5. Rationale & Evidence: Cite specific phrases and timestamps.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of speech 
              that is casual)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on 
              informality)
            - feature_specifics: object containing:
                - slang_presence: boolean
                - filler_word_frequency: string (e.g., Low, Medium, High)
                - script_type: string (e.g., Formal, Conversational)

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "slang_presence": boolean,
                    "filler_word_frequency": string,
                    "script_type": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_humor_index",
          name="Humor & Comedic Timing",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
        Detects and quantifies attempts at humor, including wit, physical comedy, 
        satire, or comedic timing.
    """,
          prompt_template="""
            Act as a Creative Strategist. Analyze the video for 'Comedic Intent.'

            VIDEO METADATA:
            {metadata_summary}

            ### 1. DEFINITIONS (for reference):
            - Humor Type: "Observational", "Slapstick", "Deadpan", "Satirical".

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can identify attempts at humor or comedic timing 
               (regardless of duration). High score for clear obvious jokes or 
               comedic delivery; lower score for ambiguous or dry humor.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of comedic setups/payoffs) 
               / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Edge Factor (how daring or unique the humor is) 
                 and Comedic Timing (0.0 to 1.0).
               - Score from 0.0 to 1.0 reflecting effectiveness.
            5. Rationale & Evidence: Cite specific timestamps and comedic moments.

                ### 3. FORMAT RESPONSE AS JSON:

                **FIELD DESCRIPTIONS:**
                - detected: boolean (True if feature is present, False otherwise)
                - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
                  of detection)
                - detected_evidence: string (Description of cues and timestamps)
                - key_driver_category: string (Categorical reason for the score)
                - recommended_actions: string (Actionable next step for the editor)
                - strengths_to_keep: string (What the editor did right)
                - first_appearance_timestamp: float (When this feature first appeared)
                - feature_density_score: float (0.0 to 1.0; proportion of video 
                  containing humor)
                - feature_quality_score: float (0.0 to 1.0; effectiveness based on timing and edge factor)
                - feature_specifics: object containing:
                    - humor_mechanism: string (e.g., Slapstick, Deadpan)
                    - edge_factor: float

                **OUTPUT STRUCTURE:**
                {{
                    "detected": boolean,
                    "detected_confidence_score": float,
                    "detected_evidence": string,
                    "key_driver_category": string,
                    "recommended_actions": string,
                    "strengths_to_keep": string,
                    "first_appearance_timestamp": float,
                    "feature_density_score": float,
                    "feature_quality_score": float,
                    "feature_specifics": {{
                        "humor_mechanism": string,
                        "edge_factor": float
                    }}
                }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="character_driven",
          name="Character-Driven",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.CONNECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Video features a relatable character whose journey or transformation resonates with audience.
            Evaluates character prominence, relatability, and narrative journey shown.
            """,
          prompt_template="""
            Act as a Narrative Strategist and Video Analyst. Your goal is to measure 
            'Character Dominance' and 'Persona-Led Storytelling.'

            VIDEO METADATA:
            {metadata_summary}

            ### 1. SCORE DIMENSIONS (for reference):
            - CHARACTER PROMINENCE (40% weight): Protagonist with distinct personality/role.
            - CHARACTER JOURNEY (30% weight): Visible journey, change, or problem-solving.
            - AUDIENCE RELATABILITY (30% weight): Relatable to target audience.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the character is identifiable as a protagonist 
               (regardless of duration). High score for clear lead role; lower 
               score for ambiguous or background characters.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of character prominence) 
               / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Score each of the three dimensions in Step 1 from 0 to 100.
               - Calculate the weighted total: `(Character Prominence * 0.40) + 
                 (Character Journey * 0.30) + (Audience Relatability * 0.30)`.
               - Divide the weighted total by 100 to get the final 
                 `feature_quality_score` as a float between 0.0 and 1.0.
            5. Rationale & Evidence: Cite specific timestamps and actions 
               supporting the scores.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with character prominence)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on dimensions)
            - feature_specifics: object containing:
                - character_type: string
                - prominence_score: int
                - journey_score: int
                - relatability_score: int

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "character_type": string,
                    "prominence_score": int,
                    "journey_score": int,
                    "relatability_score": int
                }}
            }}""",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_audio_cta",
          name="Call to Action (Audio)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
        Detects and quantifies spoken instructions that direct the viewer to take 
        action. This includes verbal commands from Voice-Overs (VO) or on-screen talent. 
        Measures 'CTA Density' and 'Urgency Level' to determine the strength of the 
        conversion signal.
    """,
          prompt_template="""
            Act as a Direct Response Marketing Analyst. Your goal is to identify and 
            quantify the spoken Call to Action (CTA).
            
            VIDEO METADATA: {metadata_summary}

            ### 1. CTA DELIVERY MODES (for reference):
            - Direct Address: On-screen talent looks at camera and gives the CTA.
            - Voice-Over (VO): Narrator delivers the CTA over b-roll or product shots.
            - Off-Camera: Secondary character or background voice mentions the action.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the spoken CTA is audible and identifiable (regardless of 
               duration). High score for clear, imperative commands; lower 
               score for ambiguous or buried mentions.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Total duration of the spoken 
               CTA) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on CTA Urgency (0.0 to 1.0). 1.0 = Explicit command 
                 with time-sensitivity; 0.5 = General suggestion; 0.1 = Brand mention only.
               - Score from 0.0 to 1.0 reflecting effectiveness.
            5. Rationale & Evidence: Cite specific timestamps and the verbatim 
               text of the CTA.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video 
              containing spoken CTA)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on 
              urgency)
            - feature_specifics: object containing:
                - cta_urgency_score: float
                - delivery_method: string
                - cta_type: string
                - placement_type: string

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "cta_urgency_score": float,
                    "delivery_method": string,
                    "cta_type": string,
                    "placement_type": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="special_offer_speech",
          name="Special Offer (Speech)",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.DIRECT,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Audio/voiceover explicitly announces special offer, discount, or deal.
            Evaluates clarity of offer type, specific details mentioned, and delivery emphasis.
            """,
          prompt_template="""
            Act as a Direct Response Marketing Analyst. Your goal is to evaluate: Is there a SPECIAL OFFER announced in speech?

            VIDEO METADATA:
            {metadata_summary}

            ### 1. SCORE DIMENSIONS (for reference):
            - OFFER TYPE CLARITY (40% weight): Clear announcement of what offer is.
            - DELIVERY EMPHASIS (35% weight): Strong emphasis given through voice tone.
            - OFFER PROMINENCE (25% weight): Featured continuously or at strategic moments.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the special offer is audible and identifiable (regardless 
               of duration). High score for explicit, detailed offers; lower 
               score for vague or implied offers.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of offer announcement) 
               / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Score each of the three dimensions in Step 1 from 0 to 100.
               - Calculate the weighted total: `(Offer Clarity * 0.40) + 
                 (Delivery Emphasis * 0.35) + (Offer Prominence * 0.25)`.
               - Divide the weighted total by 100 to get the final 
                 `feature_quality_score` as a float between 0.0 and 1.0.
            5. Rationale & Evidence: Cite specific timestamps and the verbatim 
               text of the offer.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with 
              offer announcement)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on 
              dimensions)
            - feature_specifics: object containing:
                - offer_type: string
                - offer_clarity_score: int
                - emphasis_score: int
                - prominence_score: int

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "offer_type": string,
                    "offer_clarity_score": int,
                    "emphasis_score": int,
                    "prominence_score": int
                }}
            }}""",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_production_style_index",
          name="Production Style",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
        Quantifies the visual 'Lo-Fi' vs. 'Hi-Fi' characteristics of the video. 
        Measures the presence of UGC (User Generated Content) markers such as 
        handheld camera movement, natural lighting, and native mobile aesthetics. 
        Assesses if the video feels like an 'organic post' or a 'produced commercial.'
    """,
          prompt_template="""
            Act as a professional Cinematographer and Social Media Strategist. 
            Your goal is to quantify the 'UGC Authenticity' of the production 
            style for this video.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. PRODUCTION MARKERS (for reference):
            - UGC/Lo-Fi: Visible handheld jitter, natural/ambient lighting, 
              mobile sensor resolution, "face-to-lens" intimacy.
            - Studio-UGC: Polished vertical framing, stabilized movement, 
              crisp external-mic audio, but retaining a casual feel.
            - High-Production: Cinema-grade lenses, shallow depth of field, 
              artificial 3-point lighting, professional color grading.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can identify the production style markers (regardless 
               of duration). High score for clear UGC or clear studio markers; 
               lower score for ambiguous or mixed styles.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of shots that appear 
               native/UGC) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on the Authenticity Rating (0.0 to 1.0). 1.0 = 
                 Indistinguishable from an organic user upload; 0.5 = Studio-UGC; 0.0 = High-budget commercial.
               - Score from 0.0 to 1.0 reflecting effectiveness in appearing native.
            5. Rationale & Evidence: Cite specific timestamps and production markers.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video that is UGC style)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on authenticity)
            - feature_specifics: object containing:
                - camera_stability: string
                - lighting_type: string
                - equipment_look: string
                - environment_realism: string

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "camera_stability": string,
                    "lighting_type": string,
                    "equipment_look": string,
                    "environment_realism": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_sfv_adaptation_high",
          name="Short Form Video Adaptation",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Quantifies the 'Native Emulation' of the production. Measures how effectively 
            the video mimics organic social content through lo-fi aesthetics, handheld 
            camera physics, and non-commercial editing patterns.
        """,
          prompt_template="""
            Act as a Social Media Trends Analyst and Video Strategist. 
            Your goal is to quantify the 'UGC Authenticity' of the production 
            style.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. PRODUCTION MARKERS (for reference):
            - Native/Lo-Fi: Handheld jitter, natural ambient lighting, 
              mobile sensor resolution, face-to-lens intimacy.
            - Studio-Hybrid: Vertical framing and casual tone but with 
              professional lighting or stabilized movement.
            - Commercial/Glossy: Cinema lenses, 3-point lighting, 
              professional color grading, or traditional ad pacing.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can identify the native/organic style markers 
               (regardless of duration). High score for clear native feel; 
               lower score for ambiguous or glossy commercial styles.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of shots that appear 
               native/organic) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on the Authenticity Rating (0.0 to 1.0). 1.0 = 
                 Indistinguishable from an organic user post; 0.5 = Studio-Hybrid; 0.0 = Traditional commercial.
               - Score from 0.0 to 1.0 reflecting effectiveness in sounding/looking native.
            5. Rationale & Evidence: Cite specific timestamps and style types.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video that appears native)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on authenticity)
            - feature_specifics: object containing:
                - camera_stability: string
                - lighting_type: string
                - edit_style: string

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "camera_stability": string,
                    "lighting_type": string,
                    "edit_style": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_emoji_usage",
          name="Emoji Usage",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Detects intentional creative emoji use: 1. Standard characters in text, 
            2. Animated effects, 3. Emoji-style stickers/graphics, 
            4. Platform-specific features. Excludes incidental background captures.
        """,
          prompt_template="""
            Act as a Visual Researcher and Social Media Analyst. Your goal is to 
            identify and quantify the use of emojis as creative overlays.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. EMOJI TYPES (for reference):
            - Standard: Unicode emoji characters within text overlays.
            - Animated: Emojis that pop, shake, or move.
            - Stickers: Large, graphical emoji-style elements or platform-native stickers.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can identify emojis as intentional creative overlays 
               (regardless of duration). High score for clear, isolated emojis; 
               lower score for blurry or background captures.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Sum of seconds with visible 
               emojis) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Relevance (do they match the tone/content?) and 
                 Placement (avoiding dead zones).
               - Score from 0.0 to 1.0 reflecting effectiveness.
            5. Rationale & Evidence: Cite specific timestamps and emoji types used.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with visible emojis)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on relevance and placement)
            - feature_specifics: object containing:
                - emoji_count_estimate: int
                - style: string
                - placement: string
                - primary_purpose: string

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "emoji_count_estimate": int,
                    "style": string,
                    "placement": string,
                    "primary_purpose": string
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_personal_character_talk",
          name="Direct to Camera Character Talk",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Evaluates the intimacy and continuity of direct lens address. 
            Measures the 'Breaking of the Fourth Wall' through gaze and conversational delivery.
            """,
          prompt_template="""
            Act as a Cinematographer and Parasocial Interaction Specialist. 
            Evaluate: How effectively does the character connect with the viewer 
            via direct lens address?

            VIDEO METADATA: {metadata_summary}

            ### 1. SCORE DIMENSIONS (for reference):
            - GAZE CONTINUITY & INTENSITY (45% weight): Eyes locked on lens, "FaceTime" feel.
            - DELIVERY INTIMACY (30% weight): Casual, peer-to-peer tone.
            - TEMPORAL DOMINANCE (25% weight): How much of the narrative is led by direct address.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the character is identifiable as addressing the lens 
               (regardless of duration). High score for locked gaze and clear 
               address; lower score for ambiguous looks or profile shots.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of direct lens address) 
               / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Score each of the three dimensions in Step 1 from 0 to 100.
               - Calculate the weighted total: `(Gaze Continuity * 0.45) + 
                 (Delivery Intimacy * 0.30) + (Temporal Dominance * 0.25)`.
               - Divide the weighted total by 100 to get the final 
                 `feature_quality_score` as a float between 0.0 and 1.0.
            5. Rationale & Evidence: Cite specific timestamps and character 
               actions supporting the scores.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with 
              direct lens address)
            - feature_quality_score: float (0.0 to 1.0; weighted average of quality 
              dimensions)
            - feature_specifics: object containing:
                - gaze_consistency: string
                - delivery_style: string
                - gaze_intensity_score: int
                - delivery_intimacy_score: int

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "gaze_consistency": string,
                    "delivery_style": string,
                    "gaze_intensity_score": int,
                    "delivery_intimacy_score": int
                }}
            }}""",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_native_brand_context",
          name="Brand Secondary Element",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Evaluates if the brand is positioned as a secondary, natural element. 
            High scores indicate the brand feels like part of the environment, 
            not a forced ad.
            """,
          prompt_template="""
            Act as a Brand Integration Analyst. 
            Evaluate: Is the brand naturally secondary within the organic content?

            VIDEO METADATA:
            {metadata_summary}

            ### 1. SCORE DIMENSIONS (for reference):
            - NARRATIVE INTEGRATION (40% weight): Brand exists as a natural prop or mention.
            - VISUAL SUBTLETY (35% weight): Positioned to avoid "Ad Blindness".
            - CONTEXTUAL RELEVANCE (25% weight): Fits the "Lived-in" environment.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the brand is identifiable (regardless of duration). High 
               score for clear logos or products; lower score for blurry or 
               background mentions.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of brand visibility) 
               / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Score each of the three dimensions in Step 1 from 0 to 100.
               - Calculate the weighted total: `(Narrative Integration * 0.40) + 
                 (Visual Subtlety * 0.35) + (Contextual Relevance * 0.25)`.
               - Divide the weighted total by 100 to get the final 
                 `feature_quality_score` as a float between 0.0 and 1.0.
            5. Rationale & Evidence: Cite specific timestamps and visual cues.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with brand visibility)
            - feature_quality_score: float (0.0 to 1.0; weighted average of quality dimensions)
            - feature_specifics: object containing:
                - integration_method: string
                - narrative_score: int
                - visual_subtle_score: int
                - context_score: int

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "integration_method": string,
                    "narrative_score": int,
                    "visual_subtle_score": int,
                    "context_score": int
                }}
            }}""",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_personal_character_type",
          name="Everyday Persona Validation",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Determines if the video is led by a relatable 'everyday person' or creator. 
            Returns negative if the character is a professional actor, celebrity, 
            or fictional/animated entity.
        """,
          prompt_template="""
            Evaluate if the primary character in this ad is an 'Everyday Person'.

            VIDEO METADATA: {metadata_summary}

            ### 1. DEFINITION (for reference):
            An 'Everyday Person' is an organic creator or real user who feels 
            unpolished and relatable. This feature is FALSE if the person is a 
            professional actor, a famous celebrity, or a fictional character.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can identify the character type (regardless of 
               duration). High score for clear creator style; lower score for 
               ambiguous or polished actors.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4 AND `is_everyday_person` is 
               True. Otherwise set to False.
            3. Calculate feature_density_score: (Duration of everyday person on 
               screen) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Base score on Authenticity Rating (0.0 to 1.0). 1.0 = 
                 Indistinguishable from an organic user; 0.0 = Obvious professional actor.
               - Score from 0.0 to 1.0 reflecting effectiveness in looking authentic.
            5. Rationale & Evidence: Cite specific timestamps and reasons.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video with everyday person on screen)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on authenticity)
            - feature_specifics: object containing:
                - is_everyday_person: boolean
                - is_commercial_actor: boolean
                - is_celebrity: boolean
                - is_fictional_mascot: boolean

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "is_everyday_person": boolean,
                    "is_commercial_actor": boolean,
                    "is_celebrity": boolean,
                    "is_fictional_mascot": boolean
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_product_context",
          name="Secondary Product Context",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria="""
            Evaluates if the product is positioned as a secondary element rather than the main focus of the ad, 
            appearing in a natural and realistic context.
            """,
          prompt_template="""
            Act as a Product Stylist and Video Analyst. 
            Evaluate: Is the product used naturally as a secondary element in a realistic context?
    
            VIDEO METADATA:
            {metadata_summary}

            ### 1. SCORE DIMENSIONS (for reference):
            - PRACTICAL UTILITY (45% weight): Product used for its actual purpose naturally.
            - ENVIRONMENTAL REALISM (30% weight): Messy, real-world environment.
            - VISUAL WEIGHT (25% weight): Product occupies <20% of frame while in use.

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly the product is identifiable as a secondary element 
               (regardless of duration). High score for clear, natural 
               integration; lower score for ambiguous or forced placement.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Calculate feature_density_score: (Duration where product is a 
               secondary element) / (Total video duration) = raw float value between 0.0 and 1.0.
            4. Calculate feature_quality_score: 
               - Score each of the three dimensions in Step 1 from 0 to 100.
               - Calculate the weighted total: `(Practical Utility * 0.45) + 
                 (Environmental Realism * 0.30) + (Visual Weight * 0.25)`.
               - Divide the weighted total by 100 to get the final 
                 `feature_quality_score` as a float between 0.0 and 1.0.
            5. Rationale & Evidence: Cite specific timestamps and contexts 
               supporting the scores.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (0.0 to 1.0; proportion of video where 
              product is secondary)
            - feature_quality_score: float (0.0 to 1.0; weighted average of quality 
              dimensions)
            - feature_specifics: object containing:
                - usage_type: string
                - environment_type: string
                - utility_score: int
                - realism_score: int
                - visual_weight_score: int

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "usage_type": string,
                    "environment_type": string,
                    "utility_score": int,
                    "realism_score": int,
                    "visual_weight_score": int
                }}
            }}""",
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
      VideoFeature(
          id="shorts_video_format",
          name="Vertical Format Designed For Mobile",
          category=VideoFeatureCategory.SHORTS,
          sub_category=VideoFeatureSubCategory.NONE,
          video_segment=VideoSegment.FULL_VIDEO,
          evaluation_criteria=(
              "Verifies 9:16 portrait ratio and detects"
              " letterboxing/pillarboxing."
          ),
          prompt_template="""
            Verify if the video is optimized for mobile (9:16). 
    
            VIDEO METADATA:
            {metadata_summary}
            
            ### 1. SCORE MAPPING (for reference):
            - feature_density_score: 1.0 (True 9:16), 0.5 (Letterboxed/Square), 
              0.0 (Horizontal).

            ### 2. EVALUATION LOGIC:
            1. Set detected_confidence_score: Score from 0.0 to 1.0 based on how 
               clearly you can determine the aspect ratio and presence of 
               letterboxing (regardless of duration). High score for clear visual boundaries.
            2. Detection Decision: Set `detected` to True if 
               `detected_confidence_score` >= 0.4. Otherwise set to False.
            3. Set feature_density_score: Based on the format (1.0 for 9:16, 
               0.5 for square/letterboxed, 0.0 for horizontal).
            4. Calculate feature_quality_score: 
               - 1.0 if the video is True 9:16 AND compliant with the Mobile 
                 Safe Zone (no key content cut off by UI).
               - 0.5 if True 9:16 but violates Safe Zone.
               - 0.0 if not optimized for vertical viewing.
            5. Rationale & Evidence: Cite the aspect ratio and presence of 
               letterboxing.

            ### 3. FORMAT RESPONSE AS JSON:

            **FIELD DESCRIPTIONS:**
            - detected: boolean (True if feature is present, False otherwise)
            - detected_confidence_score: float (0.0 to 1.0 indicating certainty 
              of detection)
            - detected_evidence: string (Description of cues and timestamps)
            - key_driver_category: string (Categorical reason for the score)
            - recommended_actions: string (Actionable next step for the editor)
            - strengths_to_keep: string (What the editor did right)
            - first_appearance_timestamp: float (When this feature first appeared)
            - feature_density_score: float (1.0 for 9:16, 0.5 for Letterboxed/Square, 0.0 for Horizontal)
            - feature_quality_score: float (0.0 to 1.0; effectiveness based on safe zone compliance)
            - feature_specifics: object containing:
                - format: string (e.g., 9:16, 1:1, 16:9)
                - is_letterboxed: boolean
                - safe_zone_compliant: boolean

            **OUTPUT STRUCTURE:**
            {{
                "detected": boolean,
                "detected_confidence_score": float,
                "detected_evidence": string,
                "key_driver_category": string,
                "recommended_actions": string,
                "strengths_to_keep": string,
                "first_appearance_timestamp": float,
                "feature_density_score": float,
                "feature_quality_score": float,
                "feature_specifics": {{
                    "format": string,
                    "is_letterboxed": boolean,
                    "safe_zone_compliant": boolean
                }}
            }}
        """,
          extra_instructions=[],
          evaluation_method=EvaluationMethod.LLMS,
          evaluation_function="",
          include_in_evaluation=True,
          group_by=VideoSegment.FULL_VIDEO,
      ),
  ]

  return feature_configs
