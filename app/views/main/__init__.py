from .genres import api as genres_ns
from .directors import api as directors_ns
from .movies import api as movies_ns
from .favourites import api as favourites_ns

__all__ = [
    "genres_ns",
    "directors_ns",
    "movies_ns",
    "favourites_ns",
]
