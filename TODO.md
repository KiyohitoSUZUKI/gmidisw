# TODO

## TODO:libraries
- (passed)add tonelist loading, and store csv to sqllite, some util functions
- (passed)get tonelist from softsynth, like qsynth,zynaddsubfx, by dbus,OSC,config-file ... etc. => impremented by loading from config-file
- (passed)create new synth profile : qsynth,zynaddsubfx
     => qsynth will not be impremented, cause deploying soundfont is carla's matter, so startup-profile will not control qsynth, and we only need soundfont's tonename list.
   
- (passed)create port selector GUI
- (passed)create tone selector GUI
- (passed)create port definition /w GUI (create map of portname => synth profile)
- improve profile loading performance or add progressbar. 
- create mididing's scene creator GUI
- MIDINAM format support for synthprofile

- carla profile builder: load carla config and build synth profile
- open shell apps in **tab based** terminal
- fix bug: type==startup/oneshot fail startup process call => but has some error, can't use '(quote) in shell
- (planning)graduate from mididings, rebuild midi related module by rtmidi2
- (reserching) turn GUI toolkit GTK3+ to Qt5
- create midi-filter func /w threading
- GUI-mididdevice communication logic /w threading


