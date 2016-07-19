#!/bin/bash
for f in *.m4a; do ffmpeg -i ${f%.*}.m4a -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav ${f%.*}.wav;done
