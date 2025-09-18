---
**Title:** Clarify `call_tool` parameter usage in test
**Description:** The comment explains that `call_tool` expects named argument `arguments` instead of positional arguments, which is a clarification for the test implementation.
**FilePath:** `tests/unittests/tools/mcp_tool/test_mcp_tool.py`
**LineNumber:** 168
**Confidence:** 4
**Rationale:** This "FIX" comment is not an issue to be fixed. It's an explanatory note clarifying the implementation detail of a mock call assertion within a unit test. The code is functioning as intended, and there is no action to be taken. It's a code comment, not a task.
**Context:**
```python
    result = await tool._run_async_impl(
        args=args, tool_context=tool_context, credential=None
    )

    assert result == expected_response
    self.mock_session_manager.create_session.assert_called_once_with(
        headers=None
    )
    # Fix: call_tool uses 'arguments' parameter, not positional args
    self.mock_session.call_tool.assert_called_once_with(
        "test_tool", arguments=args
    )

  @pytest.mark.asyncio
  async def test_run_async_impl_with_oauth2(self):
    """Test running tool with OAuth2 authentication."""
    tool = MCPTool(
        mcp_tool=self.mock_mcp_tool,
```
---
**Title:** Improve test coverage for `before_model_callback`
**Description:** The test for the `before_model_callback` in `LlmAgent` only checks for its existence, but should be expanded to include assertions about its behavior and invocation.
**FilePath:** `tests/unittests/agents/test_llm_agent_fields.py`
**LineNumber:** 230
**Confidence:** 1
**Rationale:** This is a straightforward task to improve test coverage. The TODO is clear, and the surrounding code provides all the necessary context. An engineer would need to understand how the `before_model_callback` is triggered within the `LlmAgent` and add assertions to verify its execution, which is a standard software development practice.
**Context:**
```python
  agent = LlmAgent(
      name='test_agent', before_model_callback=_before_model_callback
  )

  # TODO: add more logic assertions later.
  assert agent.before_model_callback is not None


def test_validate_generate_content_config_thinking_config_throw():
  with pytest.raises(ValueError):
    _ = LlmAgent(
        name='test_agent',
        generate_content_config=types.GenerateContentConfig(
```
---
**Title:** Remove manual polling for session creation in Vertex Express mode
**Description:** The code contains a workaround to manually poll for session creation in Vertex Express mode because LRO polling is not supported; this workaround should be removed when the feature becomes available.
**FilePath:** `src/google/adk/sessions/vertex_ai_session_service.py`
**LineNumber:** 119
**Confidence:** 3
**Rationale:** The resolution of this TODO is contingent upon an external dependency—the support for LRO polling in Vertex AI's Express mode. Without confirmation that this feature has been implemented in the Vertex AI service, any modification would be speculative and could break functionality for users of Express mode. The task requires external validation and is not self-contained within the codebase.
**Context:**
```python
    if _is_vertex_express_mode(self._project, self._location):
      # Express mode doesn't support LRO, so we need to poll
      # the session resource.
      # TODO: remove this once LRO polling is supported in Express mode.
      @retry(
          stop=stop_after_attempt(5),
          wait=wait_exponential(multiplier=1, min=1, max=3),
          retry=retry_if_result(lambda response: not response),
          reraise=True,
      )
      async def _poll_session_resource():
        try:
          return await self._get_session_api_response(
```
---
**Title:** Refactor State class to properly separate committed value from delta
**Description:** The `State` class's `__setitem__` and `update` methods should be modified to only update the `_delta`, leaving the `_value` unchanged until a commit operation is performed.
**FilePath:** `src/google/adk/sessions/state.py`
**LineNumber:** 42
**Confidence:** 1
**Rationale:** The TODO clearly describes a required refactoring of the `State` class logic. The issue is well-defined, and the surrounding code provides all necessary context. An engineer can implement this change by modifying the `__setitem__` and `update` methods and potentially adding a new `commit` method without needing any external information or dependencies.
**Context:**
```python
  def __setitem__(self, key: str, value: Any):
    """Sets the value of the state dict for the given key."""
    # TODO: make new change only store in delta, so that self._value is only
    #   updated at the storage commit time.
    self._value[key] = value
    self._delta[key] = value

  def __contains__(self, key: str) -> bool:
    """Whether the state dict contains the given key."""
    return key in self._value or key in self._delta

  def has_delta(self) -> bool:
```
---
**Title:** Refactor tool declaration aggregation in `LlmRequest`
**Description:** The current implementation aggregates multiple function declarations into a single `types.Tool` object; it should be refactored to add each tool as an individual `types.Tool` instance, with the merging logic possibly centralized in `google_llm.py`.
**FilePath:** `src/google/adk/tools/base_tool.py`
**LineNumber:** 129
**Confidence:** 2
**Rationale:** The TODO suggests a specific refactoring of the tool declaration logic. While the comment is somewhat ambiguous ("merge in google_llm.py"), the core idea of changing how tools are added to the request is understandable. An engineer would need to investigate `google_llm.py` to fully grasp the implications of this change and ensure the new implementation is correct. It is likely solvable but requires more investigation than a simple, self-contained fix.
**Context:**
```python
def _find_tool_with_function_declarations(
    llm_request: LlmRequest,
) -> Optional[types.Tool]:
  # TODO: add individual tool with declaration and merge in google_llm.py
  if not llm_request.config or not llm_request.config.tools:
    return None

  return next(
      (
          tool
          for tool in llm_request.config.tools
          if isinstance(tool, types.Tool) and tool.function_declarations
      ),
```
---
**Title:** Investigate non-standard schema requirement for `anyOf` in Google GenAI API
**Description:** The code includes a workaround to add a `type` field to a schema property that uses `anyOf` to prevent a `400 INVALID_ARGUMENT` error from the `google.genai` client; this needs investigation to understand the underlying API requirement.
**FilePath:** `src/google/adk/tools/_automatic_function_calling_util.py`
**LineNumber:** 177
**Confidence:** 3
**Rationale:** This TODO points to a potential undocumented or non-standard behavior in the external Google GenAI API. Resolving it requires deep investigation of the API's schema validation rules, which may involve consulting external documentation or performing exploratory API calls. It is not a self-contained code issue and depends on understanding the specifics of an external service, making it difficult to solve without that external context.
**Context:**
```python
      type_['type'] = _py_type_2_schema_type.get(
          type_['type'], 'TYPE_UNSPECIFIED'
      )
      # TODO: To investigate. Unclear why a Type is needed with 'anyOf' to
      # avoid google.genai.errors.ClientError: 400 INVALID_ARGUMENT.
      property_schema['type'] = type_['type']


def _map_pydantic_type_to_schema_type(schema: Dict):
  for _, property_schema in schema.get('properties', {}).items():
    _map_pydantic_type_to_property_schema(property_schema)


def _get_return_type(func: Callable) -> Any:
```
---
**Title:** Implement and register a service account credential exchanger
**Description:** A credential exchanger for service accounts needs to be implemented and registered in the `CredentialManager` to support exchanging service account credentials for other credential types, such as OAuth2 access tokens.
**FilePath:** `src/google/adk/auth/credential_manager.py`
**LineNumber:** 79
**Confidence:** 1
**Rationale:** This is a clear feature request to add a missing piece of functionality. The `CredentialManager` is already designed to support credential exchangers, and the TODO points to the exact place where the new exchanger should be registered. An engineer can create a new class that inherits from `BaseCredentialExchanger` and implement the required logic, which is a standard object-oriented programming task.
**Context:**
```python
    self._exchanger_registry = CredentialExchangerRegistry()
    self._refresher_registry = CredentialRefresherRegistry()

    # Register default exchangers and refreshers
    # TODO: support service account credential exchanger
    from .refresher.oauth2_credential_refresher import OAuth2CredentialRefresher

    oauth2_refresher = OAuth2CredentialRefresher()
    self._refresher_registry.register(
        AuthCredentialTypes.OAUTH2, oauth2_refresher
    )
    self._refresher_registry.register(
        AuthCredentialTypes.OPEN_ID_CONNECT, oauth2_refresher
    )
```
---
**Title:** Implement task cancellation in `A2aAgentExecutor`
**Description:** The `cancel` method in the `A2aAgentExecutor` is not implemented and should be updated to properly handle cancellation requests, which likely involves interrupting the `execute` method and gracefully terminating the agent's execution.
**FilePath:** `src/google/adk/a2a/executor/a2a_agent_executor.py`
**LineNumber:** 112
**Confidence:** 2
**Rationale:** Implementing cancellation for an asynchronous process is a non-trivial task. It requires a deep understanding of the `A2aAgentExecutor`'s execution flow and the cancellation mechanisms of the underlying ADK `Runner`. While the goal is clear, the implementation would require careful design to avoid race conditions and ensure graceful shutdown. It's solvable, but it's a complex piece of engineering, not a simple bug fix.
**Context:**
```python
  @override
  async def cancel(self, context: RequestContext, event_queue: EventQueue):
    """Cancel the execution."""
    # TODO: Implement proper cancellation logic if needed
    raise NotImplementedError('Cancellation is not supported')

  @override
  async def execute(
      self,
      context: RequestContext,
      event_queue: EventQueue,
  ):
```
---
**Title:** Improve error handling for memory search response processing
**Description:** The code for processing the `search_memory` API response should be made more robust by adding checks for the existence of expected fields and implementing better error handling for malformed memory entries.
**FilePath:** `src/google/adk/memory/vertex_ai_memory_bank_service.py`
**LineNumber:** 118
**Confidence:** 1
**Rationale:** This is a classic task of improving the robustness of code that processes external API responses. The TODO is clear, and the context points to the exact location where the improvements are needed. An engineer can add the necessary checks and logging without needing any external information.
**Context:**
```python
    memory_events = []
    for memory in api_response.get('retrievedMemories', []):
      # TODO: add more complex error handling
      memory_events.append(
          MemoryEntry(
              author='user',
              content=types.Content(
                  parts=[types.Part(text=memory.get('memory').get('fact'))],
                  role='user',
              ),
              timestamp=memory.get('updateTime'),
          )
      )
    return SearchMemoryResponse(memories=memory_events)
```
---
**Title:** Implement server-side filtering for memory search in Vertex AI RAG
**Description:** The memory search currently performs inefficient client-side filtering by `app_name` and `user_id`; this should be replaced with server-side filtering when the Vertex AI RAG service supports it.
**FilePath:** `src/google/adk/memory/vertex_ai_rag_memory_service.py`
**LineNumber:** 126
**Confidence:** 3
**Rationale:** This TODO points out an inefficiency where data is filtered on the client side instead of the server side. The fix is dependent on the external Vertex AI RAG service providing the capability to filter search results by metadata (like `app_name` and `user_id`). The existing code uses a workaround, which strongly implies this feature is not currently available. Therefore, this task cannot be completed without an update to the external service.
**Context:**
```python
    memory_results = []
    session_events_map = OrderedDict()
    for context in response.contexts.contexts:
      # filter out context that is not related
      # TODO: Add server side filtering by app_name and user_id.
      if not context.source_display_name.startswith(f"{app_name}.{user_id}."):
        continue
      session_id = context.source_display_name.split(".")[-1]
      events = []
      if context.text:
        lines = context.text.split("\n")

        for line in lines:
```
---
**Title:** Add support for non-text content in `send_history`
**Description:** The `send_history` method currently filters out non-text (e.g., audio) content from the history; this filter should be removed and replaced with logic to properly handle and stream all types of content.
**FilePath:** `src/google/adk/models/gemini_llm_connection.py`
**LineNumber:** 49
**Confidence:** 2
**Rationale:** The TODO describes a missing feature: the ability to handle non-text content in the conversation history. Implementing this requires knowledge of the Gemini streaming API and how different content types should be formatted and sent. While the goal is clear, the implementation details depend on the specifics of the `google.genai` library, which may require some research or experimentation. It is likely solvable but is more involved than a simple bug fix.
**Context:**
```python
    """

    # TODO: Remove this filter and translate unary contents to streaming
    # contents properly.

    # We ignore any audio from user during the agent transfer phase
    contents = [
        content
        for content in history
        if content.parts and content.parts[0].text
    ]

    if contents:
```
---
**Title:** Add dedicated support for `output_transcription` in `LlmResponse`
**Description:** The `LlmResponse` data structure and the surrounding logic should be updated to handle `output_transcription` as a distinct field, rather than treating it as regular text content.
**FilePath:** `src/google/adk/models/gemini_llm_connection.py`
**LineNumber:** 179
**Confidence:** 2
**Rationale:** This TODO proposes a significant refactoring of the `LlmResponse` data model to better represent different types of model output. While the change itself is straightforward (adding a field to a class), it has downstream consequences for any code that consumes `LlmResponse` objects. An engineer would need to trace all usages of `LlmResponse` and update them accordingly, which makes this a moderately complex task requiring careful planning and execution.
**Context:**
```python
        if (
            message.server_content.output_transcription
            and message.server_content.output_transcription.text
        ):
          # TODO: Right now, we just support output_transcription without
          # changing interface and data protocol. Later, we can consider to
          # support output_transcription as a separate field in LlmResponse.

          # Transcription is always considered as partial event
          # We rely on other control signals to determine when to yield the
          # full text response(turn_complete, interrupted, or tool_call).
          text += message.server_content.output_transcription.text
          parts = [
```
---
**Title:** Populate `finish_reason` in `LlmResponse` for Anthropic models
**Description:** The code to populate the `finish_reason` field in the `LlmResponse` object from the Anthropic message's `stop_reason` is currently commented out and should be re-enabled.
**FilePath:** `src/google/adk/models/anthropic_llm.py`
**LineNumber:** 194
**Confidence:** 1
**Rationale:** The task is to uncomment a single line of code that was likely disabled temporarily. The function to perform the necessary translation (`to_google_genai_finish_reason`) already exists. An engineer can re-enable this line and, after appropriate testing to ensure no regressions, the task would be complete. It's a simple, self-contained change.
**Context:**
```python
          prompt_token_count=message.usage.input_tokens,
          candidates_token_count=message.usage.output_tokens,
          total_token_count=(
              message.usage.input_tokens + message.usage.output_tokens
          ),
      ),
      # TODO: Deal with these later.
      # finish_reason=to_google_genai_finish_reason(message.stop_reason),
  )


def _update_type_string(value_dict: dict[str, Any]):
  """Updates 'type' field to expected JSON schema format."""
  if "type" in value_dict:
```
---
**Title:** Centralize tool processing logic in `_BasicLlmRequestProcessor`
**Description:** The logic for appending tool declarations to the `LlmRequest` should be moved from `BaseTool.process_llm_request` to the `_BasicLlmRequestProcessor`, which is responsible for building the request.
**FilePath:** `src/google/adk/flows/llm_flows/basic.py`
**LineNumber:** 78
**Confidence:** 2
**Rationale:** This TODO proposes a significant and beneficial architectural refactoring to centralize request-building logic. It is directly related to another TODO (in `base_tool.py`) and solving it would improve code organization. The task is complex because it involves changing the responsibility of multiple classes (`BaseTool`, `_BasicLlmRequestProcessor`) and requires a careful understanding of the entire request lifecycle. It is solvable but requires more than a trivial change.
**Context:**
```python
    llm_request.live_connect_config.proactivity = (
        invocation_context.run_config.proactivity
    )

    # TODO: handle tool append here, instead of in BaseTool.process_llm_request.

    return
    yield  # Generator requires yield statement in function body.


request_processor = _BasicLlmRequestProcessor()
```
---
**Title:** Remove Streamlit-specific timeout workaround
**Description:** The code contains a timeout in the `_send_to_model` method as a workaround for Streamlit's event loop behavior; this should be removed if the project migrates away from Streamlit.
**FilePath:** `src/google/adk/flows/llm_flows/base_llm_flow.py`
**LineNumber:** 176
**Confidence:** 3
**Rationale:** This TODO is tied to a specific deployment environment (Streamlit) and serves as a necessary workaround for its limitations. The task of removing it is contingent on a major architectural decision to migrate the application off of Streamlit. As such, it cannot be addressed without that larger, external change taking place.
**Context:**
```python
      try:
        # Streamlit's execution model doesn't preemptively yield to the event
        # loop. Therefore, we must explicitly introduce timeouts to allow the
        # event loop to process events.
        # TODO: revert back(remove timeout) once we move off streamlit.
        live_request = await asyncio.wait_for(
            live_request_queue.get(), timeout=0.25
        )
        # duplicate the live_request to all the active streams
        logger.debug(
            'Sending live request %s to active streams: %s',
            live_request,
            invocation_context.active_streaming_tools,
```
