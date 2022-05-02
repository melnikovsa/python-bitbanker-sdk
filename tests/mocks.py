import asyncio
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional


class HttpResponseMock:
    def __init__(self, status_code: int, json: Optional[Dict[str, Any]] = None, text: str = '') -> None:
        self.status_code = status_code
        self._json = json or {}
        self.text = text

    def json(self) -> Dict[str, Any]:
        return self._json


class AsyncMock:
    def __new__(  # type: ignore
        cls, return_value: Optional[Any] = None, side_effect: Optional[Exception] = None
    ) -> Callable[[Any, Any], None]:
        f = lambda *args, **kwargs: None
        if return_value:

            f = lambda *args, **kwargs: return_value

        elif side_effect:

            def f(*args: Any, **kwargs: Dict[str, Any]) -> None:
                raise side_effect  # type: ignore

        return asyncio.coroutine(f)
