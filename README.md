# EMEPLEIER
Send OSC messages to MPlayer


## Requirements

Mplayer is needed. On Debain based systems:

`sudo apt install mplayer`

Python 3 and python-osc module should be installed.

`pip install python-osc`




## Usage

In SuperDirt

``` supercollider
(
~oscaddr = NetAddr.new("127.0.0.1", 5005);
~dirt.receiveAction = { |e|
	var video, pos, speed, orbit;

    video = e['video'];
    pos = e['pos'];
    orbit = if (e['orbit']!=nil, { e['orbit'] },{ 0 });
    

	if(video!=nil)
	{
        ~oscaddr.sendMsg("/loadfile",video,orbit);
	};

	if(pos!=nil)
	{
		SystemClock.sched(e.latency,{
			~oscaddr.sendMsg("/seek",pos,orbit);
		});
	}
};
)
```

In tidal

``` haskell
let (pos, pos_p) = pF "pos" (Just 0.0)
    (depth, depth_p) = pF "depth" (Just 0.0)
    (video, video_p) = pS "video" (Just "0001.mp4")
    
d1 $ n "0 1 2 1" # s "in" # depth 1.2 # pos "40 50" # video "0012.mp4" # gain 1.60
```

