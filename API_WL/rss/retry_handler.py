import time
import functools
import logging
from icecream import ic
from rss.settings import BACKOFF_RETRY, NUMBER_OF_RETRIES, BACKOFF_BASE_DELAY

logger = logging.getLogger(__name__)


def with_backoff(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        retries = NUMBER_OF_RETRIES if BACKOFF_RETRY else 1
        for attempt in range(1, retries + 1):
            # ic(f"attempt: {attempt}")
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"[{func.__name__}] Attempt {attempt} failed: {e}")
                if attempt == retries:
                    logger.error(f"[{func.__name__}] All {retries} attempts failed.")
                    raise
                time.sleep(BACKOFF_BASE_DELAY * attempt)
    return wrapper
