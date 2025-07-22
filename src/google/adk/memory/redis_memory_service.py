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

import json
from typing import TYPE_CHECKING

from redis import Redis
from typing_extensions import override

from . import _utils
from .base_memory_service import BaseMemoryService
from .base_memory_service import SearchMemoryResponse
from .memory_entry import MemoryEntry

if TYPE_CHECKING:
  from ..events.event import Event
  from ..sessions.session import Session


def _user_key(app_name: str, user_id: str):
  return f'{app_name}:{user_id}'


class RedisMemoryService(BaseMemoryService):
  """A memory service implementation that uses Redis for storage."""

  def __init__(self, *, redis_client: Redis):
    self._redis_client = redis_client

  @override
  async def add_session_to_memory(self, session: Session):
    user_key = _user_key(session.app_name, session.user_id)
    session_events = [
        event
        for event in session.events
        if event.content and event.content.parts
    ]
    self._redis_client.hset(
        user_key, session.id, json.dumps([event.model_dump() for event in session_events])
    )

  @override
  async def search_memory(
      self, *, app_name: str, user_id: str, query: str
  ) -> SearchMemoryResponse:
    user_key = _user_key(app_name, user_id)
    session_event_lists = self._redis_client.hgetall(user_key)
    response = SearchMemoryResponse()

    for session_id, session_events_json in session_event_lists.items():
      session_events = json.loads(session_events_json)
      for event_dict in session_events:
        event = Event.model_validate(event_dict)
        if not event.content or not event.content.parts:
          continue
        if query in ' '.join(
            [part.text for part in event.content.parts if part.text]
        ):
          response.memories.append(
              MemoryEntry(
                  content=event.content,
                  author=event.author,
                  timestamp=_utils.format_timestamp(event.timestamp),
              )
          )
    return response
