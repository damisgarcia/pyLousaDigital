import sys
#lol, gambiarra. Ver como muda isso pela configuracao depois.
#sys.path.insert(0, 'D:\\Workspace-Sublime\\pyLousaDigital\\src\\ffmpeg')


from lousadigital.ffmpeg import FFMpeg as ffmpeg
from lousadigital.ffmpeg.basic import *

camera = "USB Web-CAM       "
audio = "Microfone (USB Web-CAM       )"

args = ffmpeg.FFMpegArgs()


#Linux
#args.videoIn = ffmpeg.x11DesktopLinuxCamera('/dev/video0')
#args.audioIn = ffmpeg.pulseAudio()

#Windows
args.videoIn = ffmpeg.gdiDesktopDShowCamera(camera)
args.audioIn = ffmpeg.dshowAudio(audio)

#Codecs(Independente de plataforma)
#args.videoCodec = ffmpeg.libx264()
#args.audioCodec = ffmpeg.aac()


args.output = "out.mp4"

print args

ffmpegExec = ffmpeg.captureWebcamAndDesktop()
executing = Basic(ffmpegExec).start()

input  = None
while input != 's':
	input = raw_input("Aperte s para parar a gravacao")

ffmpegExec.stop()

#print ffmpeg.createThumbnail('out.mp4','thumbnail.png')

#print args
