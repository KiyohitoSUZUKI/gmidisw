import os
import re
import subprocess

PORT_LIST_CMD = {}
PORT_LIST_CMD["jack"] = "jack_lsp -tp | awk '(NR-1)%3 == 0 { nm = $0 } (NR-1)%3 == 1 { prop = $0 } (NR-1)%3 == 2 { printf(\"%s%s%s\\n\",nm, prop, $0) }' "

PORT_LIST_CMD["jack/audio"]        = PORT_LIST_CMD["jack"] + " | grep 'audio$' "
PORT_LIST_CMD["jack/audio/input"]  = PORT_LIST_CMD["jack/audio"] + " | grep 'properties: input' "
PORT_LIST_CMD["jack/audio/in"]     = PORT_LIST_CMD["jack/audio/input"] 
PORT_LIST_CMD["jack/audio/output"] = PORT_LIST_CMD["jack/audio"] + " | grep 'properties: output' "
PORT_LIST_CMD["jack/audio/out"]    = PORT_LIST_CMD["jack/audio/output"] 
PORT_LIST_CMD["jack/midi"]         = PORT_LIST_CMD["jack"] + " | grep 'midi$' "
PORT_LIST_CMD["jack/midi/input"]   = PORT_LIST_CMD["jack/midi"] + " | grep 'properties: input' "
PORT_LIST_CMD["jack/midi/in"]      = PORT_LIST_CMD["jack/midi/input"]
PORT_LIST_CMD["jack/midi/output"]  = PORT_LIST_CMD["jack/midi"] + " | grep 'properties: output' "
PORT_LIST_CMD["jack/midi/out"]     = PORT_LIST_CMD["jack/midi/output"] 
PORT_LIST_CMD["alsa/audio"] = "(export LANG=C; aplay -l)| grep '^card' | sed 's/^.*: //g'"
#PORT_LIST_CMD["alsa/midi"]  = "cat /proc/asound/seq/clients | grep 'Port' | sed 's/^ *Port *[0-9] : //g' | sed 's/......)$//g' | sed 's/\"//g' "
PORT_LIST_CMD["alsa/midi"]  = "aplaymidi -l | sed '1d'"

##########################################################
#
##########################################################
def sfpath2sfname(sfpath: str):
    return os.path.splitext(os.path.basename(sfpath))[0]

##########################################################
# checkfunc for  jackd-audio/alsa-audio,midi port
##########################################################

def _lsport_by_cmd(port_type: str):
    rslts = subprocess.check_output(PORT_LIST_CMD[port_type] + "| cat - ",
                                   shell=True,
                                   universal_newlines=True,
                                   stderr=subprocess.DEVNULL)
    rslt = [a for a in rslts.split("\n") if a!= ""]

    if "jack" in port_type:
        rslt2 = []
        for e in rslt:
            rslt2.append(re.sub(r'\t.*$','',e))
        return rslt2
    else:
        return rslt

#=============================================
def lsport(port_type = "jack"):
    rslt = _lsport_by_cmd(port_type)

    return rslt

#=============================================
def is_port_active(port_type, port_regex):
    if not port_type in PORT_LIST_CMD:
        logging.error(f"#@startup:is_port_active:bad port type:{port_type}/{port_regex}")
        return False
    cmd = "%s | grep -i '%s' | wc -l "%(PORT_LIST_CMD[port_type], port_regex)
#    logging.debug("#@ cmd=%s"%cmd)
    rslt = subprocess.check_output(cmd,
                                   shell=True,
                                   universal_newlines=True,
                                   stderr=subprocess.DEVNULL)
#    logging.debug(f"#@ startup:is_port_active:port check rslt={rslt}")

    return int(rslt) > 0

##########################################################
#
##########################################################
def is_jack_active():
    return len(lsport()) > 0
