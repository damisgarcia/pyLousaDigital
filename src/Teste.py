import sys
#lol, gambiarra. Ver como muda isso pela configuracao depois.
#sys.path.insert(0, 'D:\\Workspace-Sublime\\pyLousaDigital\\src\\ffmpeg')


from lousadigital.ffmpeg.FFMpeg import *

camera = "USB Web-CAM       "
audio = "Microfone (USB Web-CAM       )"

#args = FFMpeg.FFMpegArgs()


#Linux
#args.videoIn = ffmpeg.x11DesktopLinuxCamera('/dev/video0')
#args.audioIn = ffmpeg.pulseAudio()

#Windows
#args.videoIn = ffmpeg.gdiDesktopDShowCamera(camera)
#args.audioIn = ffmpeg.dshowAudio(audio)

#Codecs(Independente de plataforma)
#args.videoCodec = ffmpeg.libx264()
#args.audioCodec = ffmpeg.aac()


#args.output = "out.mp4"

print createThumbnail('out.mp4','thumbnail.png')

#print args
