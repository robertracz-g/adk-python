# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from unittest import mock

import pytest
from google.adk.memory.vertex_ai_memory_bank_service import VertexAiMemoryBankService


class MockApiClientMalformed:
  """Mocks the API Client with a malformed response."""

  def __init__(self, response):
    self.response = response
    self.async_request = mock.AsyncMock(return_value=self.response)


@pytest.mark.asyncio
async def test_search_memory_malformed_response():
  """Tests that search_memory handles malformed API responses gracefully."""
  malformed_response = {
      'retrievedMemories': [
          {
              # Valid entry
              'memory': {'fact': 'valid_fact'},
              'updateTime': '2024-12-12T12:12:12.123456Z',
          },
          {
              # Missing memory dict
              'updateTime': '2024-12-12T12:12:12.123456Z',
          },
          {
              # Memory is None
              'memory': None,
              'updateTime': '2024-12-12T12:12:12.123456Z',
          },
          {
              # Missing fact
              'memory': {'other': 'thing'},
              'updateTime': '2024-12-12T12:12:12.123456Z',
          },
      ]
  }

  mock_client = MockApiClientMalformed(malformed_response)

  with mock.patch(
      'google.adk.memory.vertex_ai_memory_bank_service.VertexAiMemoryBankService._get_api_client',
      return_value=mock_client,
  ):
    service = VertexAiMemoryBankService()
    result = await service.search_memory(
        app_name='app', user_id='user', query='query'
    )

    # Should only return the one valid memory
    assert len(result.memories) == 1
    assert result.memories[0].content.parts[0].text == 'valid_fact'
