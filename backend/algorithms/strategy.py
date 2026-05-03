import time
from dataclasses import dataclass


@dataclass
class SearchResult:
    positions: list[int]
    time_ms: float
    n: int
    m: int
    algorithm: str

    @property
    def occurrences(self):
        return len(self.positions)

    @property
    def found(self):
        return bool(self.positions)


class SearchStrategy:
    name = "base"

    def search(self, text, pattern):
        start = time.perf_counter()
        positions = self._search(text, pattern)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return SearchResult(
            positions=positions,
            time_ms=round(elapsed_ms, 4),
            n=len(text),
            m=len(pattern),
            algorithm=self.name,
        )

    def _search(self, text, pattern):
        raise NotImplementedError
