
Extract single frame:
	ffmpeg -ss 01:23:45 -i input -vframes 1 -q:v 2 output.jpg


cut out part
	fmpeg -ss 00:01:30 -i GH010393.MP4 -to 00:05:00 -c copy GH010393_slice.MP4

Reduce framerate by dropping 10% frames
	ffmpeg -i GH010393_slice.MP4 -filter:v "setpts=0.1*PTS" GH010393_speed_all.MP4
