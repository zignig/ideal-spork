# Spork templated file
# Created on Thu May  7 11:54:02 2020
# Bare board

from nmigen import *
from nmigen_boards.icebreaker import ICEBreakerPlatform


class icebreaker_unsnapped(ICEBreakerPlatform):
    __sporked__ = True
    resources = ICEBreakerPlatform.resources + ICEBreakerPlatform.break_off_pmod
