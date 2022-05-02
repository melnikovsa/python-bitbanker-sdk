from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Dict
from typing import Optional


class HttpResponseMock:
    def __init__(self, status_code: int, json: Optional[Dict[str, Any]] = None, text: str = '') -> None:
        self.status_code = status_code
        self._json = json or {}
        self.text = text

    def json(self) -> Dict[str, Any]:
        return self._json


def exception(exception: Exception) -> Callable[[], None]:
    def wrapper() -> None:
        raise exception

    return wrapper


def async_mock(return_value: Any) -> Callable[[], Coroutine[Any, None, None]]:
    async def wrapper() -> Any:
        if isinstance(return_value, Exception):
            raise return_value

        return return_value

    return wrapper
