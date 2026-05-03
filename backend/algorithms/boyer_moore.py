from .strategy import SearchStrategy


class BoyerMoore(SearchStrategy):
    name = "boyer_moore"

    def _build_bad_char(self, pattern):
        table = {}
        for i, char in enumerate(pattern):
            table[char] = i
        return table

    def _search(self, text, pattern):
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        bad_char = self._build_bad_char(pattern)
        shift = 0

        while shift <= n - m:
            j = m - 1

            while j >= 0 and pattern[j] == text[shift + j]:
                j -= 1

            if j < 0:
                positions.append(shift)
                next_char_index = shift + m
                next_char_last_pos = bad_char.get(text[next_char_index], -1) if next_char_index < n else -1
                shift += max(1, m - next_char_last_pos)
            else:
                shift += max(1, j - bad_char.get(text[shift + j], -1))

        return positions
