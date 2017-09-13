# Window:
window-title Pirates Online Rewritten
icon-filename phase_3/etc/Pirates_Adds.ico
win-size 800 600
win-origin -2 -2
fullscreen #f
color-bits 0
framebuffer-depth #f

# Text:
text-encoding utf8
direct-wtext #f
text-never-break-before 1
text-flatten 0
text-dynamic-merge 1
text-minfilter linear
text-magfilter linear
text-page-size 512 512
text-rwap-mode WM_border_clor

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
audio-preload-threshold 1024
audio-library-name p3fmod_audio

# Graphics:
allow-live-flatten 1
framebuffer-alpha 1
alpha-bits 8
prefer-parasite-buffer 1
force-parasite-buffer 1
retransform-sprites 1

# Stenciles:
stencil-bits 8

# SRGB:
framebuffer-srgb #f

# DClass (reverse order...):
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Animations: 
even-animation #t
interpolate-frames #t
hardware-animated-vertices #t
restore-initial-pose #f

# Cache:
model-cache-max-kbytes 262144
want-disk-cache 1
state-cache #t
transform-cache #t
model-cache-textures #f

# Textures:
textures-power-2 none
#textures-power-2 down
texture-anisotropic-degree 16
texture-magfilter linear
texture-minfilter linear
texture-quality-level fastest


# NOTIFIER
notify-level-tiff error
notify-level-dxgsg warning
notify-level-gobj warning
notify-level-loader warning
notify-level-chan fatal
notify-level-pgraph error
notify-level-collide error
notify-level-abs error
notify-level-Actor error
notify-level-DisplayOptions debug

# Graphics Library:
gl-finish #f
gl-force-no-error #t
gl-check-errors #f
gl-force-no-flush #t
gl-force-no-scissor #t

uniquify-matrix #t
uniquify-transforms #t
uniquify-states #t
uniquify-attribs #f

# Shaders:
gl-validate-shaders #f
gl-skip-shader-recompilation-warnings #t

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

# V-Sync
sync-video #f