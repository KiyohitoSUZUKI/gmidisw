#
# dont'create .pyc cache for tests
#
export PYTHONDONTWRITEBYTECODE=1


#
# set PYTHONPATH for tests
#
export PYTHONPATH=`pwd`

#
# set rtmidi backend
#
#export RTMIDI_API=LINUX_ALSA
export RTMIDI_API=UNIX_JACK
export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/alsa-lib
