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

"""Test script for a_heartbeat_story_arc feature"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from features_repository.shorts.a_shorts_features import get_attract_features


def test_feature_structure():
    """Test that the heartbeat feature is properly structured"""
    
    print(f"\n{'='*60}")
    print(f"Testing a_heartbeat_story_arc feature structure")
    print(f"{'='*60}\n")
    
    try:
        attract_features = get_attract_features()
        heartbeat_feature = next((f for f in attract_features if f.id == "a_heartbeat_story_arc"), None)
        
        if not heartbeat_feature:
            print("❌ Feature not found!")
            return False
        
        # Check required fields
        checks = [
            ("ID", heartbeat_feature.id == "a_heartbeat_story_arc"),
            ("Name", len(heartbeat_feature.name) > 0),
            ("Category", heartbeat_feature.category.value == "SHORTS"),
            ("Sub-category", heartbeat_feature.sub_category.value == "NONE"),
            ("Video Segment", heartbeat_feature.video_segment.value == "FULL_VIDEO"),
            ("Evaluation Criteria", heartbeat_feature.evaluation_criteria and "TODO" not in heartbeat_feature.evaluation_criteria),
            ("Prompt Template", heartbeat_feature.prompt_template and "TODO" not in heartbeat_feature.prompt_template),
            ("Evaluation Method", heartbeat_feature.evaluation_method.value == "LLMS"),
            ("Include in Evaluation", heartbeat_feature.include_in_evaluation == True),
        ]
        
        all_passed = True
        for check_name, check_result in checks:
            status = "✓" if check_result else "❌"
            print(f"{status} {check_name}: {check_result}")
            all_passed = all_passed and check_result
        
        return all_passed
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test feature structure
    structure_ok = test_feature_structure()
    
    if structure_ok:
        print("\n✓ Feature structure is valid!")
        print("\n📋 Feature Summary:")
        try:
            attract_features = get_attract_features()
            heartbeat = next((f for f in attract_features if f.id == "a_heartbeat_story_arc"), None)
            if heartbeat:
                print(f"  ID: {heartbeat.id}")
                print(f"  Name: {heartbeat.name}")
                print(f"  Evaluation Method: {heartbeat.evaluation_method.value}")
                print(f"  Video Segment: {heartbeat.video_segment.value}")
                print(f"  Criteria length: {len(heartbeat.evaluation_criteria)} chars")
                print(f"  Prompt length: {len(heartbeat.prompt_template)} chars")
        except Exception as e:
            print(f"  Error: {e}")
        sys.exit(0)
    else:
        print("\n❌ Feature structure has issues!")
        sys.exit(1)
