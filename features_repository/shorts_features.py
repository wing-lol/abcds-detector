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
                - **Extreme Close-Up (ECU):** Subject fills >80% of frame.
                - **Close-Up (CU):** Subject fills 60%-80% of frame.
                - **Medium Shot (MS):** Subject fills 30%-59% of frame (not counted toward tight framing density).
                - **Wide/Long Shot (LS):** Subject fills <30% of frame (not counted toward tight framing density).

                ### 2. EVALUATION LOGIC:
                1. **Calculate feature_density_score:** (Total CU+ECU duration) / (Total video duration) = raw float value.
                2. **Detection Decision:** Set detected=True if feature_density_score > 0.1 (Incidental or above). Otherwise detected=False.
                3. **Confidence Score Mapping:** Use the density tier to set confidence_score:
                   - Density 0.9-1.0 → confidence_score = 0.95
                   - Density 0.7-0.8 → confidence_score = 0.80
                   - Density 0.4-0.6 → confidence_score = 0.65
                   - Density 0.1-0.3 → confidence_score = 0.40
                4. **Hook Bonus:** If the first 3 seconds contain CU+ECU shots, add +0.1 to confidence_score (cap at 1.0).
                5. **Rationale & Evidence:** Cite specific timestamps and shot durations that comprise the CU+ECU segments. Ignore solid backgrounds; focus on the subject's physical bounding box.

                ### 3. FORMAT RESPONSE AS JSON:
                {{
                    "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                    "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                    "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                    "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                    "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                    "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                    "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                    "feature_density_score": "float (0.0 to 1.0; calculated as (Total CU+ECU duration) / (Total video duration))",
                    "feature_specifics": {{
                        "peak_sfr_percentage": "float (0-100; highest Subject-to-Frame Ratio observed in the CU+ECU segments)",
                        "primary_subject_class": "string (e.g., Product, Human_Face)",
                        "framing_cadence": "string (e.g., Static, Fast-Cutting)",
                        "occlusion_level": "string (e.g., None, Partial, Heavy)"
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
            Act as a professional Cinematographer and Video Analyst. Your goal is to analyze the audio track of this video specifically for human vocal presence.

            VIDEO METADATA: {metadata_summary}

            ### 1. METRIC DEFINITIONS:
            - **Feature Feature Density Score:** (Total duration of audible human speech) / (Total video duration). It is referred to as feature_density_score in the JSON file.
            *Example: If there is a 2s intro greeting and a 3s closing call-to-action in a 10s video, Feature Feature Density Score is 0.5.*
            - **Vocal Clarity:** The ease with which the voice is understood (0.0 - 1.0). High score = studio quality/clear; Low score = muffled, heavy background noise, or distorted.

            ### 2. VOCAL CATEGORIES:
            - **Voice Over (VO):** Narrative voice added in post-production.
            - **Dialogue:** On-camera person speaking.
            - **Ambient Speech:** Overheard background talking.
            - **Synthetic/AI Voice:** Clear AI-generated narration (text-to-speech).

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "vocal_clarity_score": float,
                    "primary_voice_type": "string (e.g., Voice_Over, Dialogue, Mixed)",
                    "speech_cadence": "string (e.g., Rapid, Slow)",
                    "background_noise_level": "string (e.g., Low, High)"
                }}
            }}

            ### EVALUATION STEPS:
            1. Identify all time stamps where a human (or AI) voice is audible.
            2. Calculate the **feature_density_score** (Total Speech Time / Total Duration).
            3. Evaluate the **vocal_clarity_score**—reduce this if background music or noise makes speech hard to follow.
            4. Determine if the "Hook" (0:00-0:02) contains speech, as this is a high-retention signal.
        """,
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
                Act as a professional Cinematographer and Video Analyst. Your goal is to 
                analyze the video for instances where a person looks directly into the camera lens 
                to address the viewer.

                VIDEO METADATA: {metadata_summary}

                ### 1. METRIC DEFINITIONS:
                - **Feature Density Score:** (Total duration of direct eye contact / address) / (Total video duration). 
                - **Eye Contact Intensity:** A measure of how consistently the subject maintains 
                gaze without looking away at scripts or monitors (0.0 - 1.0).

                ### 2. ADDRESS MODES:
                - **Direct Address:** Subject is looking into the lens and speaking.
                - **Silent Gaze:** Subject maintains eye contact without speaking (e.g., reacting to a sound).
                - **Glance:** Brief, intermittent eye contact (less than 0.5s).
                - **Off-Camera:** Subject is looking at a secondary point (3/4 profile), not the viewer.

                ### FORMAT RESPONSE AS JSON:
                {{
                    "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                    "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                    "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                    "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                    "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                    "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                    "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                    "feature_density_score": float,
                    "feature_specifics": {{
                        "eye_contact_intensity": float,
                        "subject_distance": "string (e.g., Close-Up, Medium)",
                        "address_style": "string (e.g., Intimate, Presentational)",
                        "emotional_delivery": "string"
                    }}
                }}

                ### EVALUATION STEPS:
                1. Identify all segments where the subject's pupils are directed at the camera lens.
                2. Calculate the **feature_density_score** by dividing direct address time by total duration.
                3. Assess **eye_contact_intensity**—lower this if the subject is clearly reading a teleprompter or looking at themselves on the phone screen rather than the lens.
                4. Check the "Hook" (0:00-0:02); direct address at the start is a major retention driver.
            """,
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

        ### 1. METRIC DEFINITIONS:
        - **Feature Density Score:** (Total duration where text overlays are visible) / (Total video duration).
        - **Synchronicity Score:** (0.0 - 1.0) measure of how well text timing matches spoken words. 
          1.0 = frame-perfect captions; 0.5 = static text roughly related; 0.0 = no relation.

        ### 2. SUPERS CATEGORIES:
        - **Dynamic Captions:** Word-by-word or phrase-by-phrase synced text.
        - **Static Callouts:** Persistent text (e.g., "50% OFF" or "Product Name").
        - **Kinetic Typography:** Stylized, moving text used for emphasis.
        - **Headlines:** Large top/bottom text bars that stay throughout the video.

        ### FORMAT RESPONSE AS JSON:
        {{
            "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
            "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
            "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
            "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
            "recommended_actions": "string (Actionable next step for the editor to improve the video)",
            "strengths_to_keep": "string (What the editor did right and shouldn't change)",
            "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
            "feature_density_score": float,
            "feature_specifics": {{
                "synchronicity_score": float,
                "text_coverage_ratio": float,
                "primary_supers_type": "string (e.g., Dynamic_Captions, Headlines)",
                "readability_score": float
            }}
        }}

        ### EVALUATION STEPS:
        1. Identify all segments where text is overlaid on the video.
        2. Compare the text content against the audio track for verbatim or supportive matching.
        3. Calculate the **feature_density_score** based on text visibility duration.
        4. Assess the **synchronicity_score**—lower this if text lingers too long or appears after the audio has passed.
        5. Verify if text is in the "Mobile Safe Zone" (central area, not blocked by platform UI).
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

            ### 1. METRIC DEFINITIONS:
            - **Product Close-Up (CU):** Product occupies 30% to 59% of the frame area.
            - **Feature Density Score:** (Total duration of Product CU shots) / (Total video duration).

            ### 2. DYNAMIC SCORING (0.0 - 1.0):
            - 0.9-1.0: Product CU is the primary visual anchor (Density > 60%).
            - 0.6-0.8: Product is featured in CU at key intervals (Density 30-60%).
            - 0.1-0.5: Product CU is incidental or brief (Density < 30%).

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "average_sfr_percentage": float,
                    "product_identifiability": float,
                    "framing_style": "string (e.g., Handheld, Studio-Static)"
                }}
            }}

            ### EVALUATION LOGIC:
            - Only count segments where the Product is the main subject and fills 30%-59% of the frame.
            - If the product fills >60%, it exceeds this feature and belongs in the 'Extreme' category.
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

            ### 1. METRIC DEFINITIONS:
            - **Product Extreme Close-Up (ECU):** Product occupies 60% or more of the frame area.
            - **Feature Density Score:** (Total duration of Product ECU shots) / (Total video duration).

            ### 2. DYNAMIC SCORING (0.0 - 1.0):
            - 0.9-1.0: Macro-heavy edit; high detail focus (Density > 40%).
            - 0.6-0.8: Strategic use of macro shots for texture/detail (Density 15-40%).
            - 0.1-0.5: Incidental or very brief macro moments (Density < 15%).

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "peak_sfr_percentage": float,
                    "texture_visibility": "string (e.g., Low, Medium, High)",
                    "lighting_quality": "string (e.g., Flat, Cinematic)"
                }}
            }}

            ### EVALUATION LOGIC:
            - Only count segments where the Product fills 60% or more of the frame.
            - Focus on detail: ECU shots are intended to show the "hero" aspects of the product.
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

            SCORE ON THREE DIMENSIONS (0-100 each):

            1. INTERACTION DEPTH (40%)
            - Focus: Physical contact and active engagement.
            - Criteria: Is the product being handled, worn, consumed, or operated?
            - 90-100: Detailed, multi-step interaction or sustained use (>4s).
            - 70-89: Clear physical interaction but brief (2-4s).
            - 0-69: Minimal touching or product is merely a prop in the frame.

            2. CONTEXTUAL REALISM (30%)
            - Focus: The "Where" and "Who". 
            - Criteria: Is the environment a "lived-in" space (home, gym, office) vs. a sterile studio? 
            - 90-100: Authentic daily-life setting with natural lighting and relatable user behavior.
            - 70-89: Recognizable setting but feels slightly "staged" or over-polished.
            - 0-69: Infomercial style, white backgrounds, or disconnected from reality.

            3. UTILITY DEMONSTRATION (30%)
            - Focus: The "Why".
            - Criteria: Does the interaction show the product's purpose/benefit without needing a voiceover?
            - 90-100: The usage clearly solves a pain point or achieves a goal (e.g., thirst quenched, app task finished).
            - 70-89: Product is used correctly but the "benefit" is implied rather than obvious.
            - 0-69: Random interaction that doesn't showcase what the product actually does.

            FINAL CALCULATION:
            Overall Score = (Interaction * 0.4) + (Realism * 0.3) + (Utility * 0.3)

            FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "interaction_depth_score": int,
                    "contextual_realism_score": int,
                    "utility_demo_score": int
                }}
            }}

            SCORING GUIDANCE:
            - HIGH (80+): A "Day-in-the-life" feel. User solves a problem using the product in a real room.
            - MED (50-79): Product is used, but it feels like a "commercial." Correct use, but overly scripted.
            - LOW (<50): Product is just sitting there, or being held like a trophy for the camera.
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
            Act as a Linguistic and  Video Analyst. Your goal is to measure 'Tone Informality.'

            VIDEO METADATA:
            {metadata_summary}

            ### 1. METRIC DEFINITIONS:
            - **Feature Density Score:** (Duration of conversational/casual speech) / (Total speech duration).
            - **Informality Rating:** (0.0 - 1.0) 1.0 = "POV/FaceTime" style; 0.5 = Standard commercial; 0.0 = Corporate/Medical.

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "slang_presence": boolean,
                    "filler_word_frequency": "string (e.g., Low, Medium, High)",
                    "script_type": "string (e.g., Formal, Conversational)"
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

        ### 1. METRIC DEFINITIONS:
        - **Feature Density Score:** (Duration of comedic setups/payoffs) / (Total video duration).
        - **Humor Type:** "Observational", "Slapstick", "Deadpan", "Satirical".

        ### FORMAT RESPONSE AS JSON:
        {{
            "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
            "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
            "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
            "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
            "recommended_actions": "string (Actionable next step for the editor to improve the video)",
            "strengths_to_keep": "string (What the editor did right and shouldn't change)",
            "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
            "feature_density_score": float,
            "feature_specifics": {{
                "humor_mechanism": "string (e.g., Slapstick, Deadpan)",
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

            SCORE ON THREE DIMENSIONS (0-100 each):

            1. CHARACTER PROMINENCE (40% weight)
               Character is clear protagonist with distinct personality/role
               Look for: Clear lead character, distinct personality traits, on-screen presence
               - 90-100: Strong, well-developed protagonist
               - 70-89: Clear character with distinct personality
               - 50-69: Character present but underdeveloped
               - 0-49: No clear character focus

            2. CHARACTER JOURNEY/TRANSFORMATION (30% weight)
               Character shows visible journey, change, or problem-solving
               Look for: Before/after transformation, challenge faced, goal achieved, emotional arc
               - 90-100: Clear narrative journey with visible transformation
               - 70-89: Character shows clear journey or growth
               - 50-69: Some journey element but subtle
               - 0-49: No journey or transformation shown

            3. AUDIENCE RELATABILITY (30% weight)
               Character is relatable to target audience (emotional, realistic, authentic)
               Look for: Authentic emotion, realistic situation, audience alignment, genuine engagement
               - 90-100: Highly relatable, authentic emotion
               - 70-89: Mostly relatable character
               - 50-69: Somewhat relatable
               - 0-49: Not relatable or inauthentic

            FINAL CALCULATION:
            Overall Score = (Prominence × 0.40) + (Journey × 0.30) + (Relatability × 0.30)

            FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "character_type": "string",
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

        ### 1. METRIC DEFINITIONS:
        - **Feature Density Score:** (Total duration of the spoken CTA) / (Total video duration).
        - **CTA Urgency:** (0.0 - 1.0) 1.0 = Explicit command with time-sensitivity (e.g., "Click the link below."); 
          0.5 = General suggestion (e.g., "Check us out"); 0.1 = Brand mention only.

        ### 2. CTA DELIVERY MODES:
        - **Direct Address:** On-screen talent looks at camera and gives the CTA.
        - **Voice-Over (VO):** Narrator delivers the CTA over b-roll or product shots.
        - **Off-Camera:** Secondary character or background voice mentions the action.

        ### FORMAT RESPONSE AS JSON:
        {{
            "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
            "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
            "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
            "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
            "recommended_actions": "string (Actionable next step for the editor to improve the video)",
            "strengths_to_keep": "string (What the editor did right and shouldn't change)",
            "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
            "feature_density_score": float,
            "feature_specifics": {{
                "cta_urgency_score": float,
                "delivery_method": "string",
                "cta_type": "string",
                "placement_type": "string"
            }}
        }}

        ### EVALUATION LOGIC:
        1. Scan the audio track for imperative verbs (Shop, Buy, Click, Visit, Try, Download).
        2. Calculate the **feature_density_score** by summing the duration of these verbal triggers.
        3. Assess **feature_density_score** based on vocal clarity and "The Ask"—if the CTA is muffled or buried under loud music, lower the score.
        4. Note the placement: A CTA at the very end is standard; a CTA in the first 5 seconds is a "Fast-Action" strategy.
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

            SCORE ON THREE DIMENSIONS (0-100 each):

            1. OFFER TYPE CLARITY (40% weight)
               Clear announcement of what offer is (discount %, deal, promotion type)
               Look for: "20% off", "Free with purchase", "Buy one get one", "Limited time deal"
               - 90-100: Very clear offer type with specific details (e.g., "20% off")
               - 70-89: Clear offer mentioned with reasonable detail
               - 50-69: Offer mentioned but details vague or implied
               - 0-49: No offer details in audio

            2. DELIVERY EMPHASIS (35% weight)
               Strong emphasis given through voice tone, repetition, or prominence
               Look for: Emphatic tone, repeated mention, early in spot, vocal excitement
               - 90-100: Strong emphasis with enthusiastic delivery
               - 70-89: Clear emphasis given in delivery
               - 50-69: Mentioned with moderate emphasis
               - 0-49: Buried or casual mention

            3. OFFER PROMINENCE (25% weight)
               Offer featured continuously or at strategic moments in video
               Look for: Multiple mentions, mentioned early, highlighted throughout
               - 90-100: Prominent throughout, multiple emphatic mentions
               - 70-89: Clear prominence in video
               - 50-69: Mentioned but not prominent
               - 0-49: Single casual mention

            FINAL CALCULATION:
            Overall Score = (OfferClarity × 0.40) + (Emphasis × 0.35) + (Prominence × 0.25)

            FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "offer_type": "string",
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
        Act as a professional Cinematographer and Social Media Strategist. Your goal is to 
        quantify the 'UGC Authenticity' of the production style for this video.
        
        VIDEO METADATA: {metadata_summary}

        ### 1. METRIC DEFINITIONS:
        - **Feature Density Score:** (Duration of shots that appear native/UGC) / (Total video duration). 
        - **Authenticity Rating:** (0.0 - 1.0) 1.0 = Indistinguishable from an organic user upload; 
          0.5 = High-quality "Studio-UGC" (professional gear mimicking a mobile look); 
          0.0 = Traditional high-budget glossy commercial.

        ### 2. PRODUCTION MARKERS:
        - **UGC/Lo-Fi:** Visible handheld jitter, natural/ambient lighting, mobile sensor resolution, "face-to-lens" intimacy.
        - **Studio-UGC:** Polished vertical framing, stabilized movement, crisp external-mic audio, but retaining a casual feel.
        - **High-Production:** Cinema-grade lenses, shallow depth of field, artificial 3-point lighting, professional color grading.

        ### FORMAT RESPONSE AS JSON:
        {{
            "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
            "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
            "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
            "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
            "recommended_actions": "string (Actionable next step for the editor to improve the video)",
            "strengths_to_keep": "string (What the editor did right and shouldn't change)",
            "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
            "feature_density_score": float,
            "feature_specifics": {{
                "camera_stability": "string",
                "lighting_type": "string",
                "equipment_look": "string",
                "environment_realism": "string"
            }}
        }}

        ### EVALUATION LOGIC:
        1. Observe camera physics: Mobile devices have distinct micro-jitters; cinema rigs have "weight."
        2. Check for "Safe Zone" awareness: Is the subject framed to avoid being covered by top social media UI (avatars, descriptions)?
        3. Calculate **feature_density_score** by identifying the total runtime of "authentic-looking" footage.
        4. Lower the **Authenticity Rating** if the video uses professional motion graphics or studio-exclusive color palettes.
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
            Act as a Social Media Trends Analyst and Video Strategist. Your goal is to 
            quantify the 'UGC Authenticity' of the production style.
            
            VIDEO METADATA: {metadata_summary}

            ### 1. PRODUCTION MARKERS:
            - **Native/Lo-Fi:** Handheld jitter, natural ambient lighting, mobile sensor resolution, face-to-lens intimacy.
            - **Studio-Hybrid:** Vertical framing and casual tone but with professional lighting or stabilized movement.
            - **Commercial/Glossy:** Cinema lenses, 3-point lighting, professional color grading, or traditional ad pacing.

            ### 2. DENSITY & QUALITY LOGIC:
            - **Feature Density Score:** (Duration of shots that appear native/organic) / (Total video duration). Map to the following:
                * 0.9-1.0: Indistinguishable from an organic user post.
                * 0.7-0.8: High-quality Studio-UGC (mimics mobile but feels "clean").
                * 0.4-0.6: Polished commercial with minor native elements.
                * 0.0-0.3: Traditional high-budget commercial style.

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "camera_stability": "string",
                    "lighting_type": "string",
                    "edit_style": "string"
                }}
            }}

            ### EVALUATION LOGIC:
            - **The Hook:** If the first 3 seconds are "Native" in style, increase the feature_density_score.
            - **Intent:** Distinguish between intentional Lo-Fi style and poor production quality.
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

            ### 1. EMOJI TYPES:
            - **Standard:** Unicode emoji characters within text overlays.
            - **Animated:** Emojis that pop, shake, or move.
            - **Stickers:** Large, graphical emoji-style elements or platform-native stickers.

            ### 2. DENSITY & QUALITY LOGIC:
            - **Feature Density Score:** (Sum of seconds with visible emojis) / (Total video duration). Adjust based on:
                * 0.9-1.0: Strategic use (syncs with audio, emphasizes key points).
                * 0.6-0.8: Moderate use, primarily decorative.
                * 0.1-0.5: Incidental or poorly placed (covers key subjects).
                * 0.0: No emojis detected.

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "emoji_count_estimate": int,
                    "style": "string",
                    "placement": "string",
                    "primary_purpose": "string"
                }}
            }}

            ### EVALUATION LOGIC:
            - **Placement:** Lower the quality score if emojis are in the "Dead Zone" (bottom/right where UI buttons sit).
            - **Relevance:** Higher impact if the emoji matches the spoken word or emotional tone.
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
            Evaluate: How effectively does the character connect with the viewer via direct lens address?

            VIDEO METADATA: {metadata_summary}

            SCORE ON THREE DIMENSIONS (0-100 each):

            1. GAZE CONTINUITY & INTENSITY (45% weight)
               Focus: Are the eyes locked on the lens? Is it a "FaceTime" feel?
               - 90-100: Constant, unwavering eye contact that feels personal.
               - 70-89: Frequent direct looks, clear address to viewer.
               - 0-49: Looking at self on screen or off-camera; incidental gaze.

            2. DELIVERY INTIMACY (30% weight)
               Focus: Conversational proximity and vocal tone.
               - 90-100: Casual, peer-to-peer tone; feels unscripted and close.
               - 70-89: Clear address but slightly presentational.
               - 0-69: Corporate or formal delivery; distant.

            3. TEMPORAL DOMINANCE (25% weight)
               Focus: How much of the narrative is led by this direct address?
               - 90-100: Character address drives the entire video narrative.
               - 70-89: Significant segments of direct address.
               - 0-69: Brief intro/outro address only.

            FINAL CALCULATION:
            Overall Score = (Gaze × 0.45) + (Intimacy × 0.30) + (Dominance × 0.25)

            FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "gaze_consistency": "string",
                    "delivery_style": "string",
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
            High scores indicate the brand feels like part of the environment, not a forced ad.
            """,
          prompt_template="""
            Act as a Brand Integration Analyst. 
            Evaluate: Is the brand naturally secondary within the organic content?

            VIDEO METADATA:
            {metadata_summary}

            SCORE ON THREE DIMENSIONS (0-100 each):

            1. NARRATIVE INTEGRATION (40% weight)
               Focus: Does the brand exist as a natural prop or mention in a larger story?
               - 90-100: Brand is seamless; story makes sense even without the logo.
               - 70-89: Brand is clearly secondary but narrative-aligned.
               - 0-69: Narrative feels forced around the brand (Ad-like).

            2. VISUAL SUBTLETY (35% weight)
               Focus: Is the brand positioned to avoid "Ad Blindness"?
               - 90-100: Brand is clear but not the focal point (e.g., on clothing or background).
               - 70-89: Brand is visible but doesn't dominate the center frame.
               - 0-69: Brand is center-frame, dominant, or high-contrast (Forced focus).

            3. CONTEXTUAL RELEVANCE (25% weight)
               Focus: Does the brand fit the "Lived-in" environment?
               - 90-100: Perfectly fits the setting (e.g., gym brand in a gym).
               - 70-89: Logical fit, but feels slightly staged.
               - 0-69: Out of place; studio environment.

            FINAL CALCULATION:
            Overall Score = (Narrative × 0.40) + (Subtle × 0.35) + (Context × 0.25)

            FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "integration_method": "string",
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

            ### DEFINITION:
            An 'Everyday Person' is an organic creator or real user who feels 
            unpolished and relatable. This feature is FALSE if the person is a 
            professional actor, a famous celebrity, or a fictional character.

            ### FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
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

            SCORE ON THREE DIMENSIONS (0-100 each):

            1. PRACTICAL UTILITY (45% weight)
               Focus: Is the product being used for its actual purpose naturally?
               - 90-100: Product usage is active but effortless (part of the background action).
               - 70-89: Usage is clear but slightly emphasized for the camera.
               - 0-69: Product is just "held" or static; trophy-like.

            2. ENVIRONMENTAL REALISM (30% weight)
               Focus: Authenticity of the "Lived-in" space.
               - 90-100: Messy, real-world, or non-studio environment.
               - 70-89: Clean setting but clearly a home/office.
               - 0-69: Sterile white background or over-lit studio.

            3. VISUAL WEIGHT (25% weight)
               Focus: Subject-to-Frame Ratio (SfR) balance.
               - 90-100: Product occupies <20% of frame while in use.
               - 70-89: Product occupies 20-35% of frame.
               - 0-69: Product is dominant (>50% of frame).

            FINAL CALCULATION:
            Overall Score = (Utility × 0.45) + (Realism × 0.30) + (Weight × 0.25)

            FORMAT RESPONSE AS JSON:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "usage_type": "string",
                    "environment_type": "string",
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
            
            Metrics:
            - feature_density_score: 1.0 (True 9:16), 0.5 (Letterboxed/Square), 0.0 (Horizontal).

            JSON ONLY:
            {{
                "detected": "boolean (True if the feature is present and meets criteria, False otherwise)",
                "detected_confidence_score": "float (0.0 to 1.0 indicating certainty of detection)",
                "detected_evidence": "string (Description of the visual/audio cues and timestamps supporting the score)",
                "key_driver_category": "string (Categorical reason for the score. MUST be a short Enum-like string without spaces)",
                "recommended_actions": "string (Actionable next step for the editor to improve the video)",
                "strengths_to_keep": "string (What the editor did right and shouldn't change)",
                "first_appearance_timestamp": "float (When this feature first appeared in seconds, e.g., 2.5)",
                "feature_density_score": float,
                "feature_specifics": {{
                    "format": "string (e.g., 9:16, 1:1, 16:9)",
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
