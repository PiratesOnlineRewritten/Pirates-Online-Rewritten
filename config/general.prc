# Window:
window-title Pirates Online Rewritten
icon-filename phase_3/etc/Pirates_Adds.ico
win-size 800 600
win-origin -2 -2
fullscreen #f

# Text:
text-encoding utf8
direct-wtext #f
text-never-break-before 1

# Models:
model-path ../resources
model-path ../resources/phase_2
model-path ../resources/phase_3
model-path ../resources/phase_4
model-path ../resources/phase_5
default-model-extension .bam

# Display Pipeline:
load-display pandagl
aux-display pandagl
aux-display pandadx9
aux-display tinydisplay

# Audio:
audio-output-rate 44100
audio-library-name p3fmod_audio

# Graphics:
allow-live-flatten 1
stencil-bits 8
textures-power-2 down
framebuffer-alpha 1
alpha-bits 8
prefer-parasite-buffer 1
force-parasite-buffer 1
retransform-sprites 1

# DClass (reverse order...):
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Cache:
model-cache-max-kbytes 262144
want-disk-cache 1

# Font:
text-default-font models/fonts/BardiT_outline.bam

# Server:
server-version pirates-dev
game-server 127.0.0.1

# SSL:
want-ssl-scheme #f

# Loading Screen:
fancy-loading-screen #t

# Antialiasing:
framebuffer-multisample 1
multisamples 2

# LOD:
default-lod-type fade
make-grid-lod true
verify-lods false

# Sticky Keys:
disable-sticky-keys 1

# Other:
want-logout #f
skip-tutorial #f

# Clock:
clock-mode limited
clock-frame-rate 120

# Options Gui:
enable-pipe-selector #f
enable-stereo-display #t
want-gameoptions-hdr #t
enable-frame-rate-counter #t

# Screenshot Viewer:
want-screenshot-viewer #t
model-path ./screenshots