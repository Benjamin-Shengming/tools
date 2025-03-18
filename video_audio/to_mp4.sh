#!/usr/bin/env bash


mkdir -p output
for i in *.mkv *.avi *.mov *.flv *.mp4; do
    ffmpeg -i "$i" -fps_mode cfr -r 30  -c:v libx264 -c:a aac "./output/${i%.*}.mp4"
done