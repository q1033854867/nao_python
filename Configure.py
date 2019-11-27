#coding utf-8

from naoqi import ALProxy
import vision_definitions as vd

class Configure(object):
    def __init__(self, IP, PORT = 9559):
        self._IP = IP
        self._PORT = PORT
        self.cameraProxy = ALProxy("ALVideoDevice", self._IP, self._PORT)
        self.motionProxy = ALProxy("ALMotion", self._IP, self._PORT)
        self.postureProxy = ALProxy("ALRobotPosture", self._IP, self._PORT)
        self.tts = ALProxy("ALTextToSpeech", self._IP, self._PORT)
        self.memoryProxy = ALProxy("ALMemory", self._IP, self._PORT)
        self.audioProxy = ALProxy("ALAudioDevice", self._IP, self._PORT)



class VisualBasis(Configure):
    def __init__(self, IP, PORT = 9559, cameraId = vd.kBottomCamera, resolution = vd.kVGA):
        self._IP = IP
        self._PORT = PORT
        self.cameraId = cameraId
        self.cameraName = "CameraBottom" if self.cameraId == vd.kBottomCamera else "CameraTop"
        self.resolution = resolution
        self.colorSpace = vd.kBGRColorSpace
