
#-----------------------------------CONSTANTES---------------------------------------------------------------------------

FFMPEG_PATH = "ffmpeg-static/bin/"
#FFMPEG_EXEC = FFMPEG_PATH+"ffmpeg"
FFMPEG_EXEC = "ffmpeg"

#-----------------------------------ARGUMENTOS DO FFMPEG---------------------------------------------------------------------------
class FFMpegArgs(object):

	input = None

	initialArgs = ""

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

	initialArgs = '-thread_queue_size 128'
	#nome do dispositivo do ffmpeg(-f arg) que ira capturar a imagem de fundo
	bgDevice = "gdigrab"
	#nome do dispositivo de input para a imagem de fundo
	bgInput = "desktop"
	#tamanho do buffer para o dispositivo de fundo(nao tenho certeza se isso deveria ficar aqui)
	bgBufferSize = 1500
	
	#nome do dispositivo do ffmpeg(-f arg) para a imagem que ficara a frente
	fgDevice = None
	#argumento do dispositivo de input para imagem ficara a frente
	fgInput = None
	#tamanho do buffer para o dispositivo de frente
	fgBufferSize = 1500
	#par (x,y) que representa a distancia da janela de fg do canto inferior direito
	fgPadding = None
	#par (width, height) que representa o tamanho da janela de fg.
	fgArea = None

	@property
	def commandLine(self):
		command = ' %s -f %s -i %s -rtbufsize %dM ' % (self.initialArgs, self.bgDevice, self.bgInput, self.bgBufferSize)
		#command = ' %s -f %s -i %s ' % (self.initialArgs, self.bgDevice, self.bgInput )
		
		if self.fgDevice != None:
			command += ' %s -f %s -i %s -rtbufsize %dM' % (self.initialArgs, self.fgDevice, self.fgInput, self.fgBufferSize)
			#command += ' %s -f %s -i %s ' % (self.initialArgs, self.fgDevice, self.fgInput )

			command += ' -filter_complex "[0:v]setpts=PTS-STARTPTS[background];[1:v]setpts=PTS-STARTPTS,scale= %d:%d[foreground];[background][foreground]overlay=main_w-overlay_w-%d:main_h-overlay_h-%d"' % (self.fgArea[0],self.fgArea[1],self.fgPadding[0],self.fgPadding[1]);

			#command += ' -filter_complex "[0:v]setpts=PTS-STARTPTS[background];' 
			#+ '[1:v]setpts=PTS-STARTPTS,scale= %d:%d' + str(self.fgArea[0]) + ':' + str(self.fgArea[1]) + '[foreground];' 
			#+ '[background][foreground]overlay=main_w-overlay_w-' + str(self.fgPadding[0]) 
			#+ ':main_h-overlay_h-' + str(self.fgPadding[1]) + '"';

		
		return command+' ';

	def __repr__(self):
		return self.commandLine


#------------------------------ARGUMENTOS DO CODEC DE VIDEO-------------------------------------------------------------------------

class FFMpegVideoCodecArgs(object):

	initialArgs = ""
	videoCodec = "libvpx"
	"""
	  Indica a qualidade. Varia entre 4 e 63 no libvpx e entre 0 e 51 no
	  libx264. A intensidade do intervalo varia exponencialmente
	 """
	crf = 10
	videoBitrate = 512
	#TODO: numero de processadores em python como default
	numberThreads = 2


	@property
	def commandLine(self):
		command = " %s -codec:v %s -crf %d -b:v %dk -threads %d " % (self.initialArgs, self.videoCodec, self.crf, self.videoBitrate, self.numberThreads)

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
	


def _execute(ffmpegArgs):		

	processCode = subprocess.call(ffmpegArgs.commandLine, shell = True)

	#call retorna 0 para sucesso, e != 0 para processos mal sucedidos. Inverte isso para entrar no esquema de true(se o processo acabou) e false(caso contrario)
	return not(processCode)
	

#-------------------------------------FACTORIES--------------------------------------------------------------------------


#--------------------------CAPTURA(Windows)----------------------------------

def gdiDesktopDShowCamera(dshowDispositive):
	args = FFMpegCaptureArgs();
	initialArgs = '-thread_queue_size 128'
	args.bgDevice = "gdigrab";
	args.bgInput = "desktop";
	

	args.fgDevice = "dshow";
	args.fgInput = "video=\""+dshowDispositive+"\"";
	args.fgBufferSize = 2048

	args.fgPadding = (5,5);
	args.fgArea = (320, -1);

	return args

def dshowAudio(dshowAudioInput):
	args = FFMpegCaptureArgs();
	args.bgDevice = "dshow";
	args.bgInput = "audio=\""+dshowAudioInput+"\"";
	args.bufferSize = 2048

	return args

#--------------------------CAPTURA(Linux)----------------------------------

def x11DesktopLinuxCamera(linuxDispositive):
	args = FFMpegCaptureArgs();
	#initialArgs = '-thread_queue_size 64'
	args.bgDevice = "x11grab";
	args.bgInput = "0.0"; # a partir de que ponto comecar a capturar
		
	args.fgDevice = "vfl2";
	args.fgInput = linuxDispositive;
	
	args.fgPadding = (5,5);
	args.fgArea = (320, -1);

	return args

def pulseAudio():
	args = FFMpegCaptureArgs();
	args.bgDevice = "pulse";
	args.bgInput = "default"

	return args


#--------------------------CODEC VIDEO----------------------------------

def libvpx():
	args = FFMpegVideoCodecArgs()
	args.videoCodec = "libvpx"
	args.crf = 10
	args.videoBitrate = 512
	
	return args


def libx264():
	args = FFMpegVideoCodecArgs()

	args.videoCodec = "libx264"
	args.crf = 20
	args.videoBitrate = 512
	
	return args

#--------------------------CODEC AUDIO----------------------------------

def libvorbis():
	args = FFMpegAudioCodecArgs()
	
	args.audioCodec = "libvorbis"
	args.audioBitrate = 128

def aac():
	args = FFMpegAudioCodecArgs()

	args.initialArgs = "-strict -2"
	args.audioCodec = "aac"
	args.audioBitrate = 128

	return args
