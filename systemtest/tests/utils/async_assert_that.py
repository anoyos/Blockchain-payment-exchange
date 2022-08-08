import time

from assertpy import assert_that


class async_assert_that:
    def __init__(self, subject):
        self.subject = subject

    def is_equal_to(self, expected):
        assertion = assert_that(self.subject).is_equal_to
        self._run(assertion, expected)

    def is_length(self, length: int):
        assertion = assert_that(self.subject).is_length
        self._run(assertion, length)

    def _run(self, assertion, asserted):
        timer = time.perf_counter()
        while True:
            current = time.perf_counter()
            if (current - timer) > 2:
                assertion(asserted)
            try:
                assertion(asserted)
                return
            except Exception:
                pass