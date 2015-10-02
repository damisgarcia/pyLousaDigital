
#-----------------------------------CONSTANTES---------------------------------------------------------------------------

FFMPEG_PATH = "ffmpeg-static/bin/"
#FFMPEG_EXEC = FFMPEG_PATH+"ffmpeg"
FFMPEG_EXEC = "ffmpeg"

import gtk

from lousadigital.so.client import *

SCREEN_WIDTH =  1920
SCREEN_HEIGHT = 1080

#-----------------------------------ARGUMENTOS DO FFMPEG---------------------------------------------------------------------------
class FFMpegArgs(object):

	input = None

	initialArgs = '-y'

	videoIn = None
	audioIn = None
	videoCodec = None
	audioCodec = None

	output = None


	@property
	def commandLine(self):
		command = FFMPEG_EXEC + " " + self.initialArgs

		if self.input != None:
			command += " -i " + self.input

		if self.videoIn != None:
			command += self.videoIn.commandLine

		if self.audioIn != None:
			command += self.audioIn.commandLine

		if self.videoCodec != None:
			command += self.videoCodec.commandLine

		if self.audioCodec != None:
			command += self.audioCodec.commandLine

		command += " " + self.output


		return command

	def __repr__(self):
		return self.commandLine

#-----------------------------------ARGUMENTOS DE CAPTURA---------------------------------------------------------------------------

class FFMpegCaptureArgs(object):

	initialArgs = ''#'-thread_queue_size 192'
	#nome do dispositivo do ffmpeg(-f arg) que ira capturar a imagem de fundo
	bgDevice = "gdigrab"
	#nome do dispositivo de input para a imagem de fundo
	bgInput = "desktop"
	#largura de captura do input, no caso de video
	bgWidth = None
	#altura de captura do input, no caso de video
	bgHeight = None
	#nome do dispositivo do ffmpeg(-f arg) para a imagem que ficara a frente
	fgDevice = None
	#argumento do dispositivo de input para imagem ficara a frente
	fgInput = None
	#largura de captura do input, no caso de video
	fgWidth = None
	#altura de captura do input, no caso de video
	fgHeight = None
	#par (x,y) que representa a distancia da janela de fg do canto inferior direito
	fgPadding = None
	#par (width, height) que representa o tamanho da janela de fg.
	fgArea = None

	@property
	def commandLine(self):
		command = ' %s -f %s'  % (self.initialArgs, self.bgDevice)
		if self.bgWidth != None and self.bgHeight != None:
			command += ' -video_size %dX%d' % (self.bgWidth, self.bgHeight)

		command += ' -i %s ' % (self.bgInput)
		#command = ' %s -f %s -i %s ' % (self.initialArgs, self.bgDevice, self.bgInput )

		if self.fgDevice != None:
			command += ' %s -f %s -rtbufsize 1500M' % (self.initialArgs, self.fgDevice)

			if self.fgWidth != None and self.fgHeight != None:
				command += ' -video_size %dX%d' % (self.fgWidth, self.fgHeight)

			command += ' -i %s ' % (self.fgInput)
			#command += ' %s -f %s -i %s ' % (self.initialArgs, self.fgDevice, self.fgInput )

			command += ' -filter_complex "[0:v]setpts=PTS-STARTPTS[background];[1:v]setpts=PTS-STARTPTS,scale= %d:%d[foreground];[background][foreground]overlay=main_w-overlay_w-%d:main_h-overlay_h-%d"' % (self.fgArea[0],self.fgArea[1],self.fgPadding[0],self.fgPadding[1]);

			#command += ' -filter_complex "[0:v]setpts=PTS-STARTPTS[background];'
			#+ '[1:v]setpts=PTS-STARTPTS,scale= %d:%d' + str(self.fgArea[0]) + ':' + str(self.fgArea[1]) + '[foreground];'
			#+ '[background][foreground]overlay=main_w-overlay_w-' + str(self.fgPadding[0])
			#+ ':main_h-overlay_h-' + str(self.fgPadding[1]) + '"';


		return command + ' '

	def __repr__(self):
		return self.commandLine


#------------------------------ARGUMENTOS DO CODEC DE VIDEO-------------------------------------------------------------------------
import multiprocessing

class FFMpegVideoCodecArgs(object):

	initialArgs = ""
	videoCodec = None
	"""
	  Indica a qualidade. Varia entre 4 e 63 no libvpx e entre 0 e 51 no
	  libx264. A intensidade do intervalo varia exponencialmente
	 """
	crf = None
	videoBitrate = 512
	videoWidth = None
	videoHeight = None
	#TODO: numero de processadores em python como default
	numberThreads = multiprocessing.cpu_count()


	@property
	def commandLine(self):
		command = ' ' + self.initialArgs
		if(self.videoCodec != None):
			command += ' -codec:v %s -crf %d -b:v %dk -threads %d ' % (self.initialArgs, self.videoCodec, self.crf, self.videoBitrate, self.numberThreads)
		if self.videoWidth != None and self.videoHeight != None:
			command += '-s %dx%d' % (self.videoWidth, self.videoHeight)


		return command

	def __repr__(self):
		return self.commandLine

#----------------------------------ARGUMENTOS DO CODEC DE AUDIO------------------------------------------------------------------------

class FFMpegAudioCodecArgs(object):

	initialArgs = ""
	audioCodec = "libvorbis"
	audioBitrate = 128

	@property
	def commandLine(self):
		command = " %s -codec:a %s -b:a %dk " % (self.initialArgs, self.audioCodec, self.audioBitrate)

		return command

	def __repr__(self):
		return self.commandLine

#-------------------------------METODOS PARA CHAMADAS EXTERNAS--------------------------------------------------------------------------------------
import os
import subprocess
import signal

def capture(ffmpegArgs):
	if os.path.isfile(ffmpegArgs.output):
		os.remove(ffmpegArgs.output)

	return _execute(ffmpegArgs)


def convert(ffmpegArgs):
	if os.path.isfile(ffmpegArgs.output):
		os.remove(ffmpegArgs.output)

	if(os.path.isfile(ffmpegArgs.input)):
		return _execute(ffmpegArgs)

	return False

class FFMpegExecutor(object):

	process = None
	args = None

	def __init__(self, ffmpegArgs):
		self.args = ffmpegArgs

	def execute(self):
		
		self.process = subprocess.Popen(self.args.commandLine, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		return self.process.wait()

	def stop(self):
		if self.process != None:
			self.process.send_signal(signal.SIGTERM)


#-------------------------------------FACTORIES--------------------------------------------------------------------------


#--------------------------CAPTURA(Windows)----------------------------------

def gdiDesktopDShowCamera(dshowDispositive):
	args = FFMpegCaptureArgs();
	initialArgs = '-thread_queue_size 128'
	args.bgDevice = "gdigrab"
	args.bgInput = "desktop"

	args.fgDevice = "dshow"

	args.fgWidth = 320
	args.fgHeight = 240

	args.fgInput = "video=\""+dshowDispositive+"\""
	args.fgBufferSize = 2048

	args.fgPadding = (5,5)
	args.fgArea = (320, -1)

	return args

def gdiDesktop():
	args = FFMpegCaptureArgs();
	initialArgs = '-thread_queue_size 128'
	args.bgDevice = "gdigrab"
	args.bgInput = "desktop"

	return args


def dshowCamera(dshowDispositive):
	args = FFMpegCaptureArgs();
	#initialArgs = '-thread_queue_size 128'
	args.bgDevice = "dshow"
	args.bgInput = "video=\""+dshowDispositive+"\""

	return args


def dshowAudio(dshowAudioInput):
	args = FFMpegCaptureArgs();
	args.bgDevice = "dshow";
	args.bgInput = "audio=\""+dshowAudioInput+"\"";
	args.bufferSize = 2048

	return args

#--------------------------CAPTURA(Linux)----------------------------------

def x11DesktopLinuxCamera(linuxDispositive):
	args = FFMpegCaptureArgs()
	args.bgDevice = "x11grab"
	args.bgInput = ":0.0+100,200" # a partir de que ponto comecar a capturar

	args.fgDevice = "v4l2"
	args.fgInput = linuxDispositive

	args.fgWidth = 320
	args.fgHeight = 240

	args.fgPadding = (5,5)
	args.fgArea = (320, -1)

	return args


def x11Desktop():
	args = FFMpegCaptureArgs()
	args.bgDevice = "x11grab"
	args.bgInput = ":0.0+100,200" # a partir de que ponto comecar a capturar

	return args


def video4linuxCamera(linuxDispositive):
	args = FFMpegCaptureArgs()
	args.bgDevice = "v4l2"
	args.bgInput = linuxDispositive

	return args

#pode ser melhorado
def pulseAudio():
	args = FFMpegCaptureArgs();
	args.bgDevice = "pulse"
	args.bgInput = "default"

	return args


#--------------------------CODEC VIDEO----------------------------------

def libvpx():
	args = FFMpegVideoCodecArgs()

	args.videoCodec = "libvpx"
	args.crf = 20
	args.videoBitrate = 256

	scaleRatio = 1.5
	newWidth = SCREEN_WIDTH/scaleRatio
	newHeight = SCREEN_HEIGHT/scaleRatio
	args.videoWidth =  int( newWidth if newWidth % 2 == 0 else newWidth - 1 )
	args.videoHeight = int( newHeight if newHeight % 2 == 0 else newHeight - 1)

	return args


def libx264():

	args = FFMpegVideoCodecArgs()

	args.videoCodec = "libx264"
	args.crf = 30
	args.videoBitrate = 256

	scaleRatio = 1.5
	newWidth = SCREEN_WIDTH/scaleRatio
	newHeight = SCREEN_HEIGHT/scaleRatio
	args.videoWidth =  int( newWidth if newWidth % 2 == 0 else newWidth - 1 )
	args.videoHeight = int( newHeight if newHeight % 2 == 0 else newHeight - 1)

	return args

#--------------------------CODEC AUDIO----------------------------------

def libvorbis():
	args = FFMpegAudioCodecArgs()

	args.audioCodec = "libvorbis"
	args.audioBitrate = 64


def aac():
	args = FFMpegAudioCodecArgs()

	args.initialArgs = "-strict -2"
	args.audioCodec = "aac"
	args.audioBitrate = 64

	return args


#-------------------------------------PRESETS--------------------------------------------------------------------------

def createThumbnail(videoIn, thumbnailName):
	args = FFMpegArgs()
	args.input = videoIn

	args.videoCodec = FFMpegVideoCodecArgs()
	args.videoCodec.initialArgs = '-vframes 1 -ss 1 -an'

	args.output = thumbnailName

	return FFMpegExecutor(args)


def captureAudioOnly(outputFile = "out.mp4", audioInput = "Microfone (USB Web-CAM       )"):

	args = FFMpegArgs()
	if isWindows():
		args.audioIn = dshowAudio(audioInput)
		args.audioCodec = aac()

	elif isLinux():
		args.audioIn = pulseAudio()
		args.audioCodec = aac()

	args.output = outputFile

	return FFMpegExecutor(args)


def captureWebcam(outputFile = "out.mp4", videoInput = "USB Web-CAM       ", audioInput = "Microfone (USB Web-CAM       )"):
	args = FFMpegArgs()
	if isWindows():
		args.videoIn = dshowCamera(videoInput)
		args.audioIn = dshowAudio(audioInput)
		args.audioCodec = aac()

	elif isLinux():
		args.videoIn = video4linuxCamera(videoInput)
		args.audioIn = pulseAudio()
		args.audioCodec = aac()

	args.output = outputFile

	return FFMpegExecutor(args)


def captureDesktop(outputFile = "out.mp4", audioInput = "Microfone (USB Web-CAM       )"):
	args = FFMpegArgs()
	if isWindows():
		args.videoIn = gdiDesktop()
		args.audioIn = dshowAudio(audioInput)
		args.audioCodec = aac()

	elif isLinux():
		args.videoIn = x11Desktop()
		args.audioIn = pulseAudio()
		args.audioCodec = aac()

	args.output = outputFile

	return FFMpegExecutor(args)


def captureWebcamAndDesktop(outputFile = "out.mp4", videoInput = "USB Web-CAM       ", audioInput = "Microfone (USB Web-CAM       )"):
	args = FFMpegArgs()
	if isWindows():
		args.videoIn = gdiDesktopDShowCamera(videoInput)
		args.audioIn = dshowAudio(audioInput)
		args.audioCodec = aac()

	elif isLinux():
		args.videoIn = x11DesktopLinuxCamera(videoInput)
		args.audioIn = pulseAudio()
		args.audioCodec = aac()

	args.output = outputFile

	return FFMpegExecutor(args)
