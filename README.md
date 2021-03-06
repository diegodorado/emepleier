# EMEPLEIER
Send OSC messages to MPlayer


## Requirements

Install Mplayer. 

On Debain based systems:

```bash
sudo apt install mplayer
```

On arch based systems:

```bash
sudo pacman -S mplayer
```



Install Python 3 and python-osc module.

```bash
pip install python-osc
```


To get the video in Atom with [hydra](https://github.com/ojack/atom-hydra), [v4l2loopback](https://github.com/umlaeute/v4l2loopback) is used to make loopback video devices.

To install it on Debian based systems:

```bash
sudo apt install v4l2loopback-dkms
```


To install it on arch based systems:

```bash
sudo pacman -S v4l2loopback-dkms
```


Now clone this repository: `git clone https://github.com/diegodorado/emepleier.git`

Finally, since `mplayer` cannot pipe video directly to v4l2 because a different video format is expected, it has to be piped to a converter program before.

You have to compile the converter `yuv4mpeg_to_v4l2.c` into this directory
```bash
gcc -o yuv4mpeg_to_v4l2 yuv4mpeg_to_v4l2.c
```

So the flow is: `mplayer` -> `tempPipe` -> `yuv4mpeg_to_v4l2` -> `virtualCamera`  
(Don't run this... it is here to explain what is happening inside `emepleier.py`)
```bash
./yuv4mpeg_to_v4l2 /dev/video1 < /tmp/vid0 & mplayer -vo yuv4mpeg:file=/tmp/vid0 vid.mp4
```


## Usage

First, enable the virtual camera/s. If you want only one, set `video_nr=10` . Notice that the device indexes start with 10 to avoid collision in the scripts which will start looking at `/dev/video10`

```bash
sudo modprobe v4l2loopback video_nr=10,11,12,13
```



In SuperDirt execute `emepleier.scd`

Start the python script, pointing to an initial mp4. This will also set the videos folder to be used later.

```bash
python emepleier.py ~/Videos/trump.mp4 
```


In tidal (1.x)

``` haskell
-- define seek and video
let seek = pF "seek"
    video = pS "video"
```

In tidal (0.9x)

``` haskell
let (seek, seek_p) = pF "seek" (Just 0.0)
    (video, video_p) = pS "video" (Just "0001.mp4")

d1 $ seek "0 0.5" # s "ino" #  video "hi.mp4"
```


