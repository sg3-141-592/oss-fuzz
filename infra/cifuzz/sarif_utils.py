# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for outputting SARIF data."""
import copy
import os
import json


BUG_ID = 'bug'
# RULES = [
#   {
#       'id': '1',  # Needs to be a stable, opaque identifier.
#       'name': BUG_ID,
#       'shortDescription': {
#         'text': 'A bug'
#       },
#       'fullDescription': {
#         'text': 'A bug'
#       },
#       'help': {
#         'text': 'A bug'
#       }
#   }
# ]

RULES = {
  'version': '2.1.0',
  '$schema': 'http://json.schemastore.org/sarif-2.1.0-rtm.4',
  'runs': [
    {
      'tool': {
        'driver': {
          'name': 'ClusterFuzzLite/CIFuzz',
          'informationUri': 'https://google.github.io/clusterfuzzlite/',
          'rules': [
            {
              'id': 'no-unused-vars',
              'shortDescription': {
                'text': 'disallow unused variables'
              },
              'helpUri': 'https://eslint.org/docs/rules/no-unused-vars',
              'properties': {
                'category': 'Variables'
              }
            }
          ]
        }
      },
      'artifacts': [
        {
          'location': {
            'uri': 'file:///C:/dev/sarif/sarif-tutorials/samples/Introduction/simple-example.js'
          }
        }
      ],
      'results': [
      ]
    }
  ]
}

def get_sarif_data(crash_info):
  result = {
      'level': 'error',
      'message': {
          'text': '"x" is assigned a value but never used.'
      },
      'locations': [
          {
              'physicalLocation': {
                  'artifactLocation': {
                      'uri': 'file:///C:/dev/sarif/sarif-tutorials/samples/Introduction/simple-example.js',
                      'index': 0
                  },
                  'region': {
                      'startLine': 1,
                      'startColumn': 5
                  }
              }
          }
      ],
      'ruleId': 'no-unused-vars',
      'ruleIndex': 0
  }
  data = copy.deepcopy(RULES)
  data['runs'][0]['results'] = result
  return data


def write_crash_to_sarif(crash_info, workspace):
  data = get_sarif_data(crash_info)
  workspace.initialize_dir(workspace.sarif)
  with open(os.path.join(workspace.sarif, 'results.sarif'), 'w') as file_handle:
    file_handle.write(json.dumps(data))
