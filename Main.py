import sys
#lol, gambiarra. Ver como muda isso pela configuracao depois.
sys.path.insert(0, 'D:\\Workspace-Sublime\\pyLousaDigital\\src\\ffmpeg')


import ffmpeg

camera = "USB Web-CAM       "
audio = "Microfone (USB Web-CAM       )"

args = ffmpeg.FFMpegArgs()


#Linux
args.videoIn = ffmpeg.x11DesktopLinuxCamera('/dev/video0')
args.audioIn = ffmpeg.pulseAudio()

#Windows
#args.videoIn = ffmpeg.gdiDesktopDShowCamera(camera)
#args.audioIn = ffmpeg.dshowAudio(audio)

#Codecs(Independente de plataforma)
args.videoCodec = ffmpeg.libx264()
args.audioCodec = ffmpeg.aac()


args.output = "out.mp4"

print args

<<<<<<< Updated upstream
#print ffmpeg.capture(args)

=======
print ffmpeg.capture(args)
>>>>>>> Stashed changes
