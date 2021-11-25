import os
import re
import shutil
import yaml

from midisw.envdefs import *
from midisw.util import *

from midisw.profile.modulevars import *
import midisw.profile.util
from midisw.profile.process_builder import *
from midisw.profile.synth_builder import *

import logging

#########################################    
#########################################
def cleanup():
    if os.path.exists(PROFILE_BASE):
        shutil.rmtree(PROFILE_BASE)

def create():
    shutil.copytree(TEMPLATE_PROFILE_BASE,
                    PROFILE_BASE,
                    dirs_exist_ok=True)

#==========================

def apply_default(profile_name: str, profile: dict):
    profile_name = re.sub("/$","", profile_name)

    if profile_name in PROFILE_DEFAULT:
        parent_profile=apply_default(os.path.dirname(profile_name), profile)
        profile.update(parent_profile)
        profile.update(yaml.safe_load(PROFILE_DEFAULT[profile_name]))    

    return midisw.profile.util.remove_null_conf(profile)

#==========================    

def load(profile_category: str, profile_name: str):
    filename = os.path.join(PROFILE_BASE,profile_category,profile_name+'.yml')
    logging.debug("#loading profile %s:%s"%(profile_category,profile_name))
    with open(filename,'r') as ldf:
        prof = {}
        #
        # apply DEFAULT(profile_category common)
        #
        prof["path"] = filename

        loaded_prof = yaml.safe_load(ldf)

        if not "type" in loaded_prof:
            prof["type"] = profile_category
        else:
            prof["type"] = loaded_prof["type"]

        if not prof["type"] in PROFILE_DEFAULT:
            raise ValueError("unknown profile type dtected!"+loaded_prof["type"])
        #
        # apply class defaults
        #
        prof.update(apply_default(prof["type"],prof))

        #
        # update  by loaded profile
        #
        prof.update(loaded_prof)

        #
        # update by builder
        #
        prof = PROFILE_BUILDER[profile_category](prof)

        return prof
        
#==========================    
