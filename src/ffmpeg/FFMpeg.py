
FFMPEG_PATH = "ffmpeg-static/bin/"
#FFMPEG_EXEC = FFMPEG_PATH+"ffmpeg"
FFMPEG_EXEC = "ffmpeg"


class FFMpegArgs(object):

	input = None

	initialArgs = ""

	videoIn = None
	audioIn = None
	codecs = None

	output = None


	@property
	def commandLine(self):
		command = FFMPEG_EXEC + " " + self.initialArgs
		#command = " " + self.initialArgs

		if self.input != None:
			command += " -i " + self.input

		if self.videoIn != None:
			command += self.videoIn.commandLine

		if self.audioIn != None:
			command += self.audioIn.commandLine

		if self.codecs != None:
			command += self.codecs.commandLine

		command += " " + self.output


		return command

	def __repr__(self):
		return self.commandLine


class FFMpegCaptureArgs(object):

	initialArgs = '-thread_queue_size 64'
	#nome do dispositivo do ffmpeg(-f arg) que ira capturar a imagem de fundo
	bgDevice = "gdigrab"
	#nome do dispositivo de input para a imagem de fundo
	bgInput = "desktop"
	#nome do dispositivo do ffmpeg(-f arg) para a imagem que ficara a frente
	fgDevice = None
	#argumento do dispositivo de input para imagem ficara a frente
	fgInput = None
	#par (x,y) que representa a distancia da janela de fg do canto inferior direito
	fgPadding = None
	#par (width, height) que representa o tamanho da janela de fg.
	fgArea = None

	@property
	def commandLine(self):
		command = ' ' + self.initialArgs + ' -f ' + self.bgDevice + ' -i ' + self.bgInput;
		
		if self.fgDevice != None:
			command += ' ' + self.initialArgs + ' -f ' + self.fgDevice + ' -i ' + self.fgInput;

			command += ' -filter_complex "[0:v]setpts=PTS-STARTPTS[background];[1:v]setpts=PTS-STARTPTS,scale= %d:%d[foreground];[background][foreground]overlay=main_w-overlay_w-%d:main_h-overlay_h-%d"' % (self.fgArea[0],self.fgArea[1],self.fgPadding[0],self.fgPadding[1]);

			#command += ' -filter_complex "[0:v]setpts=PTS-STARTPTS[background];' 
			#+ '[1:v]setpts=PTS-STARTPTS,scale= %d:%d' + str(self.fgArea[0]) + ':' + str(self.fgArea[1]) + '[foreground];' 
			#+ '[background][foreground]overlay=main_w-overlay_w-' + str(self.fgPadding[0]) 
			#+ ':main_h-overlay_h-' + str(self.fgPadding[1]) + '"';

		
		return command+' ';

	def __repr__(self):
		return self.commandLine



class FFMpegCodecArgs(object):


	videoCodec = "libvpx"
	"""
	  Indica a qualidade. Varia entre 4 e 63 no libvpx e entre 0 e 51 no
	  libx264. A intensidade do intervalo varia exponencialmente
	 """
	crf = 10
	videoBitrate = 500
	
	audioCodec = "libvorbis"
	audioBitrate = 128	

	#TODO: numero de processadores em python como default
	numberThreads = 2


	@property
	def commandLine(self):
		command = " -codec:v %s -crf %d -b:v %dk -threads %d -codec:a %s -b:a %dk " % (self.videoCodec, self.crf, self.videoBitrate, self.numberThreads, self.audioCodec, self.audioBitrate)

		#command = " -codec:v " + self.videoCodec 
		#+ " -crf " + self.crf
		#+ " -b:v " + self.videoBitrate + "k"
		#+ " -threads " + self.numberThreads
		#+ " -codec:a " + self.audioCodec
		#+ " -b:a " + self.audioBirate + "k" + " "


		return command


	def __repr__(self):
		return self.commandLine


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
	



import os
import subprocess

def _execute(ffmpegArgs):		

	processCode = subprocess.call(ffmpegArgs.commandLine, shell = True)


	#call retorna 0 para sucesso, e != 0 para processos mal sucedidos. Inverte isso para entrar no esquema de true(se o processo acabou) e false(caso contrario)
	return not(processCode)
	


def gdiDesktopDShowCamera(dshowDispositive):
	args = FFMpegCaptureArgs();
	initialArgs = '-thread_queue_size 64'
	args.bgDevice = "gdigrab";
	args.bgInput = "desktop";
		
	args.fgDevice = "dshow";
	args.fgInput = "video=\""+dshowDispositive+"\"";
	
	args.fgPadding = (5,5);
	args.fgArea = (320, -1);

	return args

def dshowAudio(dshowAudioInput):
	args = FFMpegCaptureArgs();
	args.bgDevice = "dshow";
	args.bgInput = "audio=\""+dshowAudioInput+"\"";

	return args


def libvpx():
	args = FFMpegCodecArgs()
	args.videoCodec = "libvpx"
	args.crf = 10
	args.videoBitrate = 500
	
	args.audioCodec = "libvorbis"
	args.audioBitrate = 128
	return args


def libx264():
	args = FFMpegCodecArgs()
	args.videoCodec = "libx264"
	args.crf = 20
	args.videoBitrate = 500
	
	args.audioCodec = "libmp3lame"
	args.audioBitrate = 128

	return args