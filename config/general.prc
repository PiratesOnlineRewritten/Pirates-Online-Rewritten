# Window:
window-title Pirates Online Rewritten
icon-filename phase_3/etc/Pirates_Adds.ico

# Models:
model-path ../resources
model-path ../resources/phase_2
model-path ../resources/phase_3
model-path ../resources/phase_4
model-path ../resources/phase_5
default-model-extension .bam

# Audio:
audio-library-name p3openal_audio

# DClass (reverse order...):
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Server:
server-version pirates-dev
game-server 127.0.0.1

# SSL:
want-ssl-scheme #f

# Loading Screen:
fancy-loading-screen #t

# ANTIALIASING
framebuffer-multisample 1
multisamples 2

# STICKY KEYS
disable-sticky-keys 1