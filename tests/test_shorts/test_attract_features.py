#!/usr/bin/env python3

"""Run ABCD assessment for ATTRACT (A) features only"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from configuration import Configuration
from main import execute_abcd_assessment_for_videos

def run_evaluation():
    """Run ABCD Detector evaluation on test video with ATTRACT features only"""
    
    print("\n" + "=" * 70)
    print("🎬 RUNNING ABCD ASSESSMENT WITH ATTRACT (A) FEATURES ONLY")
    print("=" * 70 + "\n")
    
    # Get API key from environment variable
    api_key = os.getenv("KNOWLEDGE_GRAPH_API_KEY", "")
    if not api_key:
        print("⚠️  WARNING: KNOWLEDGE_GRAPH_API_KEY environment variable not set")
        print("   Set it with: export KNOWLEDGE_GRAPH_API_KEY='your-api-key'\n")
    
    # Initialize configuration
    config = Configuration()
    
    # ATTRACT features to evaluate (13 total)
    attract_features = [
        "a_heartbeat_story_arc",
        "a_fast_pacing_full",
        "a_fast_pacing_early",
        "a_tight_framing",
        "a_tight_framing_early",
        "a_has_sound",
        "a_has_music",
        "a_sound_effects",
        "a_dialogue_single",
        "a_dialogue_multiple",
        "a_supers_combined",
        "a_bright_colors",
        "a_high_contrast",
    ]
    
    # Set Google Cloud parameters
    config.set_parameters(
        project_id="branderator-smart-demo",
        project_zone="us-central1",
        bucket_name="solomon_abcd_ds",
        knowledge_graph_api_key=api_key,
        bigquery_dataset="abcd_detector_ds",
        bigquery_table="abcd_assessments_solomon",
        assessment_file="",
        extract_brand_metadata=False,
        use_annotations=False,
        use_llms=True,
        run_long_form_abcd=False,
        run_shorts=True,
        features_to_evaluate=attract_features,  # Only ATTRACT features
        creative_provider_type="GCS",
        verbose=True,
    )
    
    # Set brand details
    config.set_brand_details(
        brand_name="Salomon",
        brand_variations="Salomon, Salomon Group, S/LAB",
        products="XT-6, Speedcross 6, XA Pro 3D V9",
        products_categories="Trail Running, Road Running, Hiking",
        call_to_actions="Tomorrow is Yours, Unleash the best version"
    )
    
    # Set LLM parameters
    config.set_llm_params(
        llm_name="gemini-2.5-pro",
        location="us-central1",
        max_output_tokens=65535,
        temperature=0,
        top_p=0.95,
    )
    
    # Set video to evaluate
    config.set_videos([
        "gs://solomon_abcd_ds/videos/p8cvwBx4FFk.mp4"
    ])
    
    # Run evaluation
    print("📹 Video: gs://solomon_abcd_ds/videos/p8cvwBx4FFk.mp4")
    print(f"🏷️  Features: ATTRACT (A) category only ({len(attract_features)} features)")
    print("🔍 Running evaluation...")
    print("⏳ This will take a few minutes (LLM inference on video)...\n")
    
    try:
        execute_abcd_assessment_for_videos(config)
        print("\n" + "=" * 70)
        print("✅ ATTRACT FEATURES EVALUATION COMPLETE!")
        print("=" * 70)
        return 0
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = run_evaluation()
    sys.exit(exit_code)
