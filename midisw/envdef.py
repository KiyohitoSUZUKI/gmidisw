import os
import logging

LOGGING_LEVEL=logging.DEBUG

CONFIG_BASE = os.path.expanduser("~/.config/midisw")
PROFILE_BASE = os.path.join(CONFIG_BASE, "profile")

if __file__ == None:
    TEMPLATE_PROFILE_BASE = os.path.join(os.getcwd(),"profile")
else:
    TEMPLATE_PROFILE_BASE = os.path.join(os.path.dirname(__file__),"../profile")
