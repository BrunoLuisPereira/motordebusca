from .strategy import SearchStrategy

BASE = 256
MOD = 1_000_000_007


class RabinKarp(SearchStrategy):
    name = "rabin_karp"

    def _search(self, text, pattern):
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        h = 1
        for _ in range(m - 1):
            h = (h * BASE) % MOD

        pattern_hash = 0
        window_hash = 0
        for i in range(m):
            pattern_hash = (BASE * pattern_hash + ord(pattern[i])) % MOD
            window_hash = (BASE * window_hash + ord(text[i])) % MOD

        for i in range(n - m + 1):
            if pattern_hash == window_hash and self._equals_at(text, pattern, i):
                positions.append(i)

            if i < n - m:
                window_hash = (
                    BASE * (window_hash - ord(text[i]) * h) + ord(text[i + m])
                ) % MOD

        return positions

    def _equals_at(self, text, pattern, start):
        for j in range(len(pattern)):
            if text[start + j] != pattern[j]:
                return False
        return True
