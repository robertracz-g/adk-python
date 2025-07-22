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
import time
from typing import Any
from typing import Optional
import uuid

from redis import Redis
from typing_extensions import override

from ..events.event import Event
from .base_session_service import BaseSessionService
from .base_session_service import GetSessionConfig
from .base_session_service import ListSessionsResponse
from .session import Session
from .state import State


def _app_key(app_name: str) -> str:
  return f'app:{app_name}'


def _user_key(app_name: str, user_id: str) -> str:
  return f'user:{app_name}:{user_id}'


def _session_key(app_name: str, user_id: str, session_id: str) -> str:
  return f'session:{app_name}:{user_id}:{session_id}'


class RedisSessionService(BaseSessionService):
  """A session service implementation that uses Redis for storage."""

  def __init__(self, *, redis_client: Redis):
    self._redis_client = redis_client

  @override
  async def create_session(
      self,
      *,
      app_name: str,
      user_id: str,
      state: Optional[dict[str, Any]] = None,
      session_id: Optional[str] = None,
  ) -> Session:
    session_id = (
        session_id.strip()
        if session_id and session_id.strip()
        else str(uuid.uuid4())
    )
    session = Session(
        app_name=app_name,
        user_id=user_id,
        id=session_id,
        state=state or {},
        last_update_time=time.time(),
    )
    session_key = _session_key(app_name, user_id, session_id)
    self._redis_client.set(session_key, session.model_dump_json())
    return await self._merge_state(session)

  @override
  async def get_session(
      self,
      *,
      app_name: str,
      user_id: str,
      session_id: str,
      config: Optional[GetSessionConfig] = None,
  ) -> Optional[Session]:
    session_key = _session_key(app_name, user_id, session_id)
    session_json = self._redis_client.get(session_key)
    if not session_json:
      return None
    session = Session.model_validate_json(session_json)

    if config:
      if config.num_recent_events:
        session.events = session.events[-config.num_recent_events :]
      if config.after_timestamp:
        i = len(session.events) - 1
        while i >= 0:
          if session.events[i].timestamp < config.after_timestamp:
            break
          i -= 1
        if i >= 0:
          session.events = session.events[i + 1 :]

    return await self._merge_state(session)

  async def _merge_state(self, session: Session) -> Session:
    app_key = _app_key(session.app_name)
    app_state = self._redis_client.hgetall(app_key)
    if app_state:
      for key, value in app_state.items():
        session.state[State.APP_PREFIX + key.decode()] = json.loads(value)

    user_key = _user_key(session.app_name, session.user_id)
    user_state = self._redis_client.hgetall(user_key)
    if user_state:
      for key, value in user_state.items():
        session.state[State.USER_PREFIX + key.decode()] = json.loads(value)
    return session

  @override
  async def list_sessions(
      self, *, app_name: str, user_id: str
  ) -> ListSessionsResponse:
    session_keys = self._redis_client.keys(
        _session_key(app_name, user_id, '*')
    )
    sessions = []
    for session_key in session_keys:
      session_json = self._redis_client.get(session_key)
      if session_json:
        session = Session.model_validate_json(session_json)
        session.events = []
        session.state = {}
        sessions.append(session)
    return ListSessionsResponse(sessions=sessions)

  @override
  async def delete_session(
      self, *, app_name: str, user_id: str, session_id: str
  ) -> None:
    session_key = _session_key(app_name, user_id, session_id)
    self._redis_client.delete(session_key)

  @override
  async def append_event(self, session: Session, event: Event) -> Event:
    await super().append_event(session=session, event=event)
    session.last_update_time = event.timestamp

    if event.actions and event.actions.state_delta:
      for key, value in event.actions.state_delta.items():
        if key.startswith(State.APP_PREFIX):
          app_key = _app_key(session.app_name)
          self._redis_client.hset(
              app_key, key.removeprefix(State.APP_PREFIX), json.dumps(value)
          )
        elif key.startswith(State.USER_PREFIX):
          user_key = _user_key(session.app_name, session.user_id)
          self._redis_client.hset(
              user_key, key.removeprefix(State.USER_PREFIX), json.dumps(value)
          )

    session_key = _session_key(session.app_name, session.user_id, session.id)
    self._redis_client.set(session_key, session.model_dump_json())
    return event
