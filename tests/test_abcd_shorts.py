#!/usr/bin/env python3

"""Run ABCD assessment with the new Heartbeat Story Arc feature"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from configuration import Configuration
from main import execute_abcd_assessment_for_videos

def run_evaluation():
    """Run ABCD Detector evaluation on test video with Heartbeat feature"""
    
    print("\n" + "=" * 70)
    print("🎬 RUNNING ABCD ASSESSMENT WITH HEARTBEAT STORY ARC FEATURE")
    print("=" * 70 + "\n")
    
    # Get API key from environment variable
    api_key = os.getenv("KNOWLEDGE_GRAPH_API_KEY", "")
    if not api_key:
        print("⚠️  WARNING: KNOWLEDGE_GRAPH_API_KEY environment variable not set")
        print("   Set it with: export KNOWLEDGE_GRAPH_API_KEY='your-api-key'\n")
    
    # Initialize configuration
    config = Configuration()
    
    # Set Google Cloud parameters
    config.set_parameters(
        project_id="branderator-smart-demo",
        project_zone="us-central1",
        bucket_name="solomon_abcd_ds",
        knowledge_graph_api_key=api_key,
        bigquery_dataset="abcd_detector_ds",
        bigquery_table="abcd_assessments_shopify_v1",
        assessment_file="",
        extract_brand_metadata=False,
        use_annotations=False,
        use_llms=True,
        run_long_form_abcd=False,
        run_shorts=True,
        features_to_evaluate=[],
        creative_provider_type="GCS",
        verbose=True,
    )
    
    # Set brand details
    config.set_brand_details(
        brand_name="Shopify",
        brand_variations="Shopify Inc., Shopify E-commerce, Shopify Online Store",
        products="Shopify E-commerce Platform",
        products_categories="E-commerce, Online Store Solutions",
        call_to_actions="Sign Up, Start Free Trial, Learn More",
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
        # "gs://solomon_abcd_ds/videos/p8cvwBx4FFk.mp4",
        "gs://recommendations-ai-test-384721_video_analysis_uploads/Shopify/shorts/781w7OGQnzM.mp4"
        # "gs://recommendations-ai-test-384721_video_analysis_uploads/Shopify/shorts/781w7OGQnzM.mp4"
    ])
    
    # Run evaluation
    print("📹 Video: gs://recommendations-ai-test-384721_video_analysis_uploads/Shopify/shorts/781w7OGQnzM.mp4")
    print("🔍 Running Shorts evaluation with Heartbeat feature...")
    print("⏳ This will take a few minutes (LLM inference on video)...\n")
    
    try:
        execute_abcd_assessment_for_videos(config)
        print("\n" + "=" * 70)
        print("✅ EVALUATION COMPLETE!")
        print("=" * 70)
        print("\n🎉 Check output above for Heartbeat Story Arc evaluation result")
        return 0
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR DURING EVALUATION")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure you ran: gcloud auth application-default login")
        print("   2. Ensure you ran: gcloud config set project branderator-smart-demo")
        print("   3. Check that APIs are enabled in GCP Console:")
        print("      - Video Intelligence API")
        print("      - Vertex AI API")
        print("      - Cloud Storage API")
        print("\nFull error trace:")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(run_evaluation())