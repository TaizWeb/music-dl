#!/bin/sh
for i in *; do ffmpeg -i "$i" "${i%.*}.$1";done
