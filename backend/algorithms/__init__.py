from .boyer_moore import BoyerMoore
from .brute_force import BruteForce
from .kmp import KMP
from .rabin_karp import RabinKarp

ALGORITMOS = {
    "brute_force": BruteForce(),
    "rabin_karp": RabinKarp(),
    "kmp": KMP(),
    "boyer_moore": BoyerMoore(),
}
