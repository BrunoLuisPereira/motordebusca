from .strategy import SearchStrategy


class BruteForce(SearchStrategy):
    name = "brute_force"

    def _search(self, text, pattern):
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        for i in range(n - m + 1):
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(i)

        return positions
