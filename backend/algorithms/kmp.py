from .strategy import SearchStrategy


class KMP(SearchStrategy):
    name = "kmp"

    def _build_lps(self, pattern):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

        return lps

    def _search(self, text, pattern):
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        lps = self._build_lps(pattern)
        i = 0
        j = 0

        while i < n:
            if text[i] == pattern[j]:
                i += 1
                j += 1

            if j == m:
                positions.append(i - j)
                j = lps[j - 1]
            elif i < n and text[i] != pattern[j]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return positions
