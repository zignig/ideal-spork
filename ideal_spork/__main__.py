" Module level main"
from .logger import logger

log = logger(__name__)

from .builder.select_board import interactive

print("Ideal Spork")
interactive()
