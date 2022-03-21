import yaml
import subprocess
import time
import os
import signal
import argparse
import datetime
from datetime import date
import threading
from os import fork
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
#Recorder Info
Recorder_Path=str(cfg["Recorder"]["Path"])
Recorder={}
firstrun=True
# Change to correct directory
os.chdir(Recorder_Path)
def run():
    global checkthis
    checkthis=False
    start_recording()

def return_filename():
    # Creates a filename with the start time
    # of recording in its name
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    fl = current_time.replace(' ', '_')
    fl = fl.replace(':', '-')
    return fl

def chunk_timer(camera,full_path,Camera_Name,proc):
    global checkthis
    global client
    print('Send termination signal')
    proc.send_signal(signal.SIGHUP)
    os.kill(proc.pid, signal.SIGTERM)
    print(camera+' Killed')
    Recorder[camera] = False
    start_recording()

def start_recording():
    global checkthis
    global firstrun
    global Recorder
    if firstrun == True:
        for camera in cfg["cameras"]:
            Recorder[camera]=False
        firstrun = False
    if firstrun == False:
        for camera in cfg["cameras"]:
            if Recorder[camera] == False:
                Recorder[camera] = True
                #Camera Info
                Camera_Name=str(cfg["cameras"][camera]["Name"])
                Camera_IP=str(cfg["cameras"][camera]["IP"])
                Camera_Port=str(cfg["cameras"][camera]["Port"])
                Camera_Path=str(cfg["cameras"][camera]["Path"])
                Camera_User=str(cfg["cameras"][camera]["User"])
                Camera_Password=str(cfg["cameras"][camera]["Password"])
                rtsp_url='rtsp://'+Camera_User+':'+Camera_Password+'@'+Camera_IP+':'+Camera_Port+Camera_Path
                filename = return_filename()
                now = datetime.datetime.now()
                currentyear = datetime.datetime.today().year
                currentmonth = datetime.datetime.today().month
                currentday = datetime.datetime.today().day
                current_path = os.getcwd()
                outdir = '%s/%s/%s/%s' % (Camera_Name, currentyear, currentmonth, currentday)
                print(outdir)
                isdir =  os.path.isdir('./%s' % (outdir))
                full_path = current_path + '/%s/%s.mp4' % (outdir, filename)
                print(full_path)
                if isdir == False:
                    os.system('mkdir -p %s' % outdir)                
                outfile = './%s/%s.mp4' % (outdir, filename)
                # cmd = 'ffmpeg -i %s -c:a aac -c:v copy -map 0 -f segment -strftime 1 -segment_time %d -segment_format mp4 -reset_timestamps 1 \"%s/%s.mp4\"' % (rtsp_url,Recorder_Chunks,outdir,filename)
                cmd = 'mencoder -nocache -rtsp-stream-over-tcp %s -oac copy -ovc copy -endpos 00:10:00 -o %s'%(rtsp_url,full_path)  
                print(cmd)
                cmd = cmd.split(' ')
                cmd = [ix for ix in cmd if ix != '']
                st = time.time()
                with open(outfile,"wb") as outp:
                  proc = subprocess.Popen(cmd, shell=False,stdin=None, stdout=outp, stderr=None, close_fds=True)
                  time.sleep(1)
                  print(Camera_Name+' Recording started!')
                  threading.Timer(600, chunk_timer,[camera,full_path,Camera_Name,proc]).start()

run()
