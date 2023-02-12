# mtp-file-transfer
This script is useful for allowing a user to download picture, video, and audio files from their Android phone.
To do this, a simplistic text based interface was built that leverages the mtpy module.
Original mtpy module was modified in order for it to run on MacOS.

This has been tested with MacOS 10.13.x and a Consumer Cellular Link II Android based flip phone

## Setup steps:
1) Install libmtp. The mtpy module relies on this library.
2) Run mtpy-master/setup.py script with install parameter. This will require permissions to write to your Library files.

## Running:
Your phone should be on, plugged in, and set to MTP file transfer mode.

