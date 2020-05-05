
cut out part
	fmpeg -ss 00:01:30 -i GH010393.MP4 -to 00:05:00 -c copy GH010393_slice.MP4

Reduce framerate
	ffmpeg -i GH010393_slice.MP4 -r 25 -filter:v "setpts=0.1*PTS" GH010393_speed.MP4


