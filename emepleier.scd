(
// live audio input, with orbit offset
(
SynthDef(\ino, { |out, sustain = 1, pan, orbit|
	var sound;
	sound = SoundIn.ar([orbit*2,orbit*2+1]); // stereo in
	OffsetOut.ar(out,
		DirtPan.ar(sound, ~dirt.numChannels, pan)
	)
}).add
);


~oscaddr = NetAddr.new("127.0.0.1", 5005);
~dirt.receiveAction = { |e|
    var video, seek, speed, orbit;
    video = e['video'];
    seek = e['seek'];
    orbit = if (e['orbit']!=nil, { e['orbit'] },{ 0 });
    speed = if (e['speed']!=nil, { e['speed'] },{ 1 });

	if(video!=nil)
	{
        ~oscaddr.sendMsg("/loadfile",video,orbit);
	};

	if(seek!=nil)
	{
		SystemClock.sched(e.latency,{
			~oscaddr.sendMsg("/seek",seek,orbit);
		});
	};
	if(speed!=nil)
	{
		SystemClock.sched(e.latency,{
			~oscaddr.sendMsg("/speed",speed,orbit);
		});
	};
};
)
