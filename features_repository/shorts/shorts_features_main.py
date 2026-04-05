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

"""Main entry point for Shorts feature configurations - combines all ABCD categories"""

from features_repository.shorts.a_shorts_features import get_attract_features
from features_repository.shorts.b_shorts_features import get_brand_features
from features_repository.shorts.c_shorts_features import get_connect_features
from features_repository.shorts.d_shorts_features import get_direct_features
from features_repository.shorts.shorts_other_features import get_other_features


def get_shorts_feature_configs():
  """Gets all supported Shorts features organized by ABCD category
  
  Combines features from:
  - Attract (A): Attention-grabbing elements
  - Brand (B): Brand visibility and presence
  - Connect (C): Audience connection and engagement
  - Direct (D): Call-to-action and conversion
  - Other: Platform-specific and format features
  
  Returns:
    list: Combined list of all feature configurations
  """
  all_features = (
      get_attract_features() +
      get_brand_features() +
      get_connect_features() +
      get_direct_features() +
      get_other_features()
  )
  
  return all_features
