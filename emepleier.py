#!/usr/bin/python3
import subprocess
import argparse
from pythonosc import dispatcher,osc_server
from pathlib import Path
import os
LINE_BUFFERED = 1


class Vid:
  def __init__(self,proc,path):
    self.proc = proc
    self.path = path

def main(args):
    def send_command(command, orbit):
        print(command, flush=True, file=vids[orbit].proc.stdin)

    def osc_seek(unused_addr, args, seek,orbit):
        send_command('seek {} 1'.format(seek*100), orbit)

    def osc_speed(unused_addr, args, speed,orbit):
        send_command('speed_set {}'.format(speed), orbit)

    def osc_loadfile(unused_addr, args, name, orbit):
        path = '{}/{}'.format(cwd,name)
        if path != vids[orbit].path:
            vids[orbit].path = path
            send_command('loadfile {}'.format(path), orbit)

    dis = dispatcher.Dispatcher()
    dis.map("/seek", osc_seek, "Seek")
    dis.map("/speed", osc_speed, "Speed")
    dis.map("/loadfile", osc_loadfile, "Loadfile")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dis)
    print("Serving on {}".format(server.server_address))

    vids = []
    cwd = str(Path(args.filename).parents[0])
    for i in range(args.instances):
        #delete old pipes
        subprocess.run(['rm', '-f','/tmp/vid{0}'.format(i)], stdout=subprocess.PIPE)
        # create new pipes
        subprocess.run(['mkfifo', '/tmp/vid{0}'.format(i)], stdout=subprocess.PIPE)
        #convert pipe to v4l2
        os.system('./yuv4mpeg_to_v4l2 /dev/video1{0} < /tmp/vid{0} &'.format(i))
        # start subprocess
        proc = subprocess.Popen('mplayer -slave -nolirc -noaspect  -quiet -fps 30 -osdlevel 0 -ao jack:noconnect:name=emepleier{0}  -loop 0 -vf scale=480:-2,crop=480:208 -fixed-vo -vo yuv4mpeg:interlaced:file=/tmp/vid{0}'.format(i).split()+[args.filename] , stdin=subprocess.PIPE, universal_newlines=True, bufsize=LINE_BUFFERED, cwd=cwd)
        # append to collection
        vids.append(Vid(proc,args.filename))


    server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='filename', help='filename')
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    parser.add_argument("--instances",
                        type=int, default=1, choices=[1,2,3,4], help="The number of video intances to create")

    # todo: check v4l2 instances
    # todo: validate osc messages
    args = parser.parse_args()
    main(args)
