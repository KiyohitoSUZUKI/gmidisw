
import sys
import subprocess
import threading
import time
import logging
import shlex

import midisw.envdefs
import midisw.util
import midisw.profile


_PORT_OBSERVE_INTERVAL=1

def wait_port_up(port_type, port_regex):
    while not midisw.util.is_port_active(port_type, port_regex):
        logging.debug(f"#@process:wait_port_up:waiting {port_type}/{port_regex}")
        time.sleep(_PORT_OBSERVE_INTERVAL)
    logging.debug(f"#@process:wait_port_up:found {port_type}/{port_regex}")

def wait_port_down(port_type, port_regex):
    while midisw.util.is_port_active(port_type, port_regex):
        logging.debug(f"#@process:wait_port:down:waiting {port_type}/{port_regex}")
        time.sleep(_PORT_OBSERVE_INTERVAL)
    logging.debug(f"#@process:port_down:downed {port_type}/{port_regex}")

##########################################################
# ProcessMonitoring Wrapper
##########################################################

class ProcessWrapper(object):
    def __init__(self, prof: dict, *args, **kwargs):
        super(ProcessWrapper, self).__init__(*args, **kwargs)
        self.prof = prof
        self.popen_h = None
        self.is_oneshot = self.prof['type'] == 'process/oneshot'
        self.observer_th = None
        self.req_observe_stop = False

    def observe(self):
        while True:
            if self.req_observe_stop:
                return

            is_process_active = (self.popen_h.poll() is None) or (self.is_oneshot is True)
            is_port_valid = True
            for port in self.prof['require']:
                is_port_valid &= midisw.util.is_port_active(port['type'],port['name'])
            if not is_process_active or not is_port_valid:
                self.stop()
                self.start()
            time.sleep(_PORT_OBSERVE_INTERVAL)

    def _wait_provides_down(self):
        logging.debug(f"#@process:ProcessWrapper:_wait_provides_down:waiting {self.prof['provides']}")
        for port in self.prof['provides']:
            wait_port_down(port['type'],port['name'])

        return self

    def _wait_provides_up(self):
        logging.debug(f"#@process:ProcessWrapper:_wait_provides_up:waiting {self.prof['provides']}")
        for port in self.prof['provides']:
            wait_port_up(port['type'],port['name'])

        return self


    def stop(self):
        self.req_observe_stop = True
        self.observer_th.join(timeout=_PORT_OBSERVE_INTERVAL)
        if not self.popen_h is None:
            self.popen_h.kill()
            self.popen_h.wait()
            logging.debug('#@process:ProcessWrapper:stop:killed, status= '+str(self.popen_h.poll()))
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
       logging.debug(f"#@process:ProcessWrapper:starting {cmdline}")
       self.popen_h = subprocess.Popen(cmdline,shell=True)

       if self.is_oneshot:
           self.popen_h.wait()
           time.sleep(_PORT_OBSERVE_INTERVAL*2)
       else:
           #
           # whien process process fail, restart and wait process again
           #
           while (not self.popen_h.poll() is None) and (self.is_oneshot is False): 
               logging.debug('.')
               time.sleep(_PORT_OBSERVE_INTERVAL)
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
