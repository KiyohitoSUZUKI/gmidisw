import os
import glob
import logging

from functools import lru_cache

import configparser
import sqlite3

from midisw.envdefs import *
import midisw.profile
import midisw.util
import midisw.tonenamedb
import midisw.profile.util

#############################################################
#############################################################
class Synth(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profiles = []        
        self.profiles.append(midisw.profile.apply_default("synth", {}))
        self.load_from_profile()
        self.load_from_qsynth()
    #
    # scan from profile folder/and build eac hprofile
    #
    def load_from_profile(self):
        files = glob.glob(os.path.join(PROFILE_BASE,"synth")+"/**/*.yml")
        for f in files:
            bname = os.path.splitext(f.replace(PROFILE_BASE+"synth/",""))[0]
            self.profiles.append(midisw.profile.load("synth", bname))
        
    #
    # scan qsynth-conf and build profile
    #
    def load_from_qsynth(self, qconfig="~/.config/rncbc.org/Qsynth.conf"):
        confpath = os.path.expanduser(qconfig)
        conf = configparser.ConfigParser()
        conf.read(confpath, encoding="utf-8")
        ##=====================
        ## extract Qsynth.conf
        ##=====================
        tonedic_sf={}
        tonedic_names={}
        for k in conf["Engine"]:
            key = k
            value = conf["Engine"][k]
            ename,category,param = key.split("\\")
        
            if not ename in tonedic_sf:
                tonedic_sf[ename] = {}
        
            if category == "soundfonts":          ##all keys are lowercase
                for tgtp in ["bankoffset","soundfont"]:
                    if param.startswith(tgtp):
                        num = param.replace(tgtp,"")
                        if not num in tonedic_sf[ename]:
                            tonedic_sf[ename][num] = {}
                        tonedic_sf[ename][num][tgtp] = value
            elif category == "settings":
                if param == "jackname":
                    tonedic_names[ename] = value
        ## ====================
        ## extract from default
        ## ====================
        dname = conf["Settings"]["jackname"]
        tonedic_sf[dname] = {}
        tonedic_names[dname]=dname
        for k in conf["SoundFonts"]:
            param = k
            value = conf["SoundFonts"][k]
            for tgtp in ["bankoffset", "soundfont"]:
                if param.startswith(tgtp):
                    num = param.replace(tgtp,"")
                    if not num in tonedic_sf[dname]:
                        tonedic_sf[dname][num] = {}
                    tonedic_sf[dname][num][tgtp] = value

        ##=====================
        # gen tonenamedb, create synth/profile
        ##=====================
        for qc in tonedic_sf:
            addprof = midisw.profile.apply_default("synth/fluidsynth/qsynth",{})
            addprof = midisw.profile.util.remove_null_conf(addprof)
            addprof["name"] = tonedic_names[qc]
            addprof["type"] = "synth/fluidsynth/qsynth"
            addprof["jackname"] = tonedic_names[qc]
            addprof["tonenamedb"] = midisw.tonenamedb.Base()
            
            for sf in tonedic_sf[qc]:
                ofs=int(tonedic_sf[qc][sf]["bankoffset"])
                sfpath=tonedic_sf[qc][sf]["soundfont"]
                db = midisw.tonenamedb.SoundFont()
                db.load(sfpath)
                for rec in db.ls():
                    try:
                        addprof["tonenamedb"].create(rec[0]+ofs/128,
                                                     rec[1]+ofs%128,
                                                     rec[2],
                                                     rec[3],
                                                     rec[4])
                    except sqlite3.IntegrityError:
                        logging.error("key integrity error, some conf wrong in qsynth soundfont settings.")
                    finally:
                        pass
                    
            self.profiles.append(addprof)

    #
    # list writable profile
    #
    @lru_cache
    def ls_writable(self):
        retval=[]
        for prof in self.profiles:
            if "recv" in prof:
                retval.append(prof)

        return retval

    #
    # list readable profile
    #
    @lru_cache
    def ls_readable(self):
        retval=[]
        for prof in self.profiles:
            if "send" in prof:
                retval.append(prof)

        return retval
        
#############################################################
#############################################################

