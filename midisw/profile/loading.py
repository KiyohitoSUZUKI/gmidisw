import os
import shutil
import yaml
import logging

from midisw.envdefs import *
from midisw.util import *

from midisw.profile.profile_vars import *
from midisw.profile.build_startup import *
from midisw.profile.build_synth import *


logging.basicConfig(level=LOGGING_LEVEL)

#########################################    
#########################################
def cleanup_profile():
    if os.path.exists(PROFILE_BASE):
        shutil.rmtree(PROFILE_BASE)

def create_profile():
    shutil.copytree(TEMPLATE_PROFILE_BASE,
                    PROFILE_BASE,
                    dirs_exist_ok=True)


def load_profile(profile_category: str, profile_name: str):
    filename = os.path.join(PROFILE_BASE,profile_category,profile_name+'.yml')
    with open(filename,'r') as ldf:
        prof = {}
        #
        # apply DEFAULT(profile_category common)
        #
        prof.update(yaml.safe_load(PROFILE_DEFAULT[profile_category]))
        prof["category"] = profile_category
        prof["profile"] = profile_name
        prof["path"] = filename

        loaded_prof = yaml.safe_load(ldf)

        if not "type" in loaded_prof:
            loaded_prof["type"] = profile_category

        if not loaded_prof["type"] in PROFILE_DEFAULT:
            raise ValueError("unknown profile type dtected!"+loaded_prof["type"])
        
        #
        # apply DEFAULT(each subcategory)
        #
        prof.update(yaml.safe_load(PROFILE_DEFAULT[loaded_prof["type"]]))

        #
        # update  by loaded profile
        #
        prof.update(loaded_prof)

        #
        # update by builder
        #
        prof = PROFILE_BUILDER[profile_category](prof)

        return prof
        
