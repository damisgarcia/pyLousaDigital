import sys
#lol, gambiarra. Ver como muda isso pela configuracao depois.
sys.path.insert(0, 'D:\\Workspace-Sublime\\pyLousaDigital\\src\\ffmpeg')


import ffmpeg

camera = "USB Web-CAM       "
audio = "Microfone (USB Web-CAM       )"

args = ffmpeg.FFMpegArgs()

#TODO: -thread_queue_size e um argumento do input, colocar ele junto com os inputs.
args.videoIn = ffmpeg.gdiDesktopDShowCamera(camera)
args.audioIn = ffmpeg.dshowAudio(audio)
args.codecs = ffmpeg.libx264()

args.output = "out.avi"

print args

print ffmpeg.capture(args)

