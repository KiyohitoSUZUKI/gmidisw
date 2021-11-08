
import sys
import subprocess
import threading
import time
import logging
import shlex

import midisw.envdef as ENVDEF
import midisw.profile

logging.basicConfig(level=ENVDEF.LOGGING_LEVEL)

PORT_TYPES = ['jack/audio','jack/midi','alsa/audio','alsa/midi']
PORT_OBSERVE_INTERVAL=1

##########################################################
# checkfunc for  jackd-audio/alsa-audio,midi port
##########################################################

def is_port_active(port_type, port_regex):
    if port_type == 'jack/audio' or port_type == 'jack/midi':
        cmd = 'jack_lsp | grep -i "' + port_regex + '" | wc -l'
    elif port_type == 'alsa/audio':
        cmd = f"(export LANG=C; aplay -l | grep -v '^ ' | grep -i  '{port_regex}' | wc -l)"
    elif port_type == 'alsa/midi':
#        cmd = f"cat /proc/asound/seq/clients | grep ^Client | grep : | sed 's/^Client *//g' |   grep -i '{port_regex}' | wc -l"
        cmd = f"cat /proc/asound/seq/clients | grep 'Port' | sed 's/^ *Port *[0-9] : //g' |  grep -i '{port_regex}' | wc -l"
    else:
        logging.error(f"startup:is_port_active:bad port type:{port_type}/{port_regex}")
        return False

    #logging.debug(f"startup:is_port_active:port checking:{port_type}/{port_regex}")

    rslt = subprocess.check_output(cmd,shell=True, universal_newlines=True)

    #logging.debug(f"startup:is_port_active:port check rslt={rslt}")

    return int(rslt) > 0

def wait_port_up(port_type, port_regex):
    while not is_port_active(port_type, port_regex):
        logging.debug(f"startup:wait_port_up:waiting {port_type}/{port_regex}")
        time.sleep(PORT_OBSERVE_INTERVAL)
    logging.debug(f"startup:wait_port_up:found {port_type}/{port_regex}")

def wait_port_down(port_type, port_regex):
    while is_port_active(port_type, port_regex):
        logging.debug(f"startup:wait_port:down:waiting {port_type}/{port_regex}")
        time.sleep(PORT_OBSERVE_INTERVAL)
    logging.debug(f"startup:port_down:downed {port_type}/{port_regex}")

##########################################################
# ProcessMonitoring Wrapper
##########################################################

class ProcessWrapper(object):
    def __init__(self, prof: dict, *args, **kwargs):
        super(ProcessWrapper, self).__init__(*args, **kwargs)
        self.prof = prof
        self.popen_h = None
        self.is_oneshot = self.prof['type'] == 'startup/oneshot'
        self.observer_th = None
        self.req_observe_stop = False

    def observe(self):
        while True:
            if self.req_observe_stop:
                return

            is_process_active = (self.popen_h.poll() is None) or (self.is_oneshot is True)
            is_port_valid = True
            for port in self.prof['require']:
                is_port_valid &= is_port_active(port['type'],port['name'])
            if not is_process_active or not is_port_valid:
                self.stop()
                self.start()
            time.sleep(PORT_OBSERVE_INTERVAL)

    def _wait_provides_down(self):
        logging.debug(f"startup:ProcessWrapper:_wait_provides_down:waiting {self.prof['provides']}")
        for port in self.prof['provides']:
            wait_port_down(port['type'],port['name'])

        return self

    def _wait_provides_up(self):
        logging.debug(f"startup:ProcessWrapper:_wait_provides_up:waiting {self.prof['provides']}")
        for port in self.prof['provides']:
            wait_port_up(port['type'],port['name'])

        return self


    def stop(self):
        self.req_observe_stop = True
        self.observer_th.join(timeout=PORT_OBSERVE_INTERVAL)
        if not self.popen_h is None:
            self.popen_h.kill()
            self.popen_h.wait()
            logging.debug('startup:ProcessWrapper:stop:killed, status= '+str(self.popen_h.poll()))
            self._wait_provides_down()

        self.popen_h = None
        return self

    def is_active(self):
        if self.is_oneshot:
            return not self.req_observe_stop
        else:
            return (not self.popen_h is None) and (self.popen_h.poll() is None)

    def start(self):
       #
       # wait required port
       #
       for port in self.prof['require']:
           wait_port_up(port['type'],port['name'])
       #
       # start process
       #
       #  pid = subprocess.Popen("xterm +sb -e 'ethstatus -i wlp2s0'",shell=True).pid
       #  subprocess.call('export LANG=C; ' + cmd + ' &',shell=True)
       #
       cmdline = 'exec ' + self.prof['command']
       logging.debug(f"startup:ProcessWrapper:starting {cmdline}")
       self.popen_h = subprocess.Popen(cmdline,shell=True)

       if self.is_oneshot:
           self.popen_h.wait()
           time.sleep(PORT_OBSERVE_INTERVAL*2)
       else:
           #
           # whien process startup fail, restart and wait process again
           #
           while (not self.popen_h.poll() is None) and (self.is_oneshot is False): 
               logging.debug('.')
               time.sleep(PORT_OBSERVE_INTERVAL)
               self.popen_h = subprocess.Popen(cmdline,shell=True)
            #
            # wait provided port
            #
           self._wait_provides_up()

        # 
        # start observer
        #
       self.req_observe_stop = False
       self.observer_th = threading.Thread(target=self.observe)
       self.observer_th.start()

       return self
