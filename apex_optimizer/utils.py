from typing import Any

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


# Retry Decorator
def retry_with_backoff(func: Any) -> Any:
    return retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        retry=retry_if_exception_type(
            (requests.exceptions.RequestException, Exception)
        ),
        reraise=True,
    )(func)
