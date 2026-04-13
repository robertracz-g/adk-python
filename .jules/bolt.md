## 2024-05-18 - Set construction micro-optimization
**Learning:** Found instances where lists were created just to be passed to `set()`. While the environment lacks some dependencies blocking full test execution, the syntax change is extremely safe.
**Action:** Used `python3 -m py_compile` to verify syntax when standard test runners failed due to environment issues.
