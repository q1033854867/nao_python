#coding utf-8

from naoqi import ALProxy
import vision_definitions as vd
import numpy as np
import time
import cv2
cv_version = cv2.__version__.split(".")[0]
if cv_version == "2":
        import cv2.cv as cv

class Configure(object):
    """
    a basic class for nao Proxy
    """
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
    """
    a basic class for visual task.
    """
    def __init__(self, IP, PORT = 9559, cameraId = vd.kBottomCamera, resolution = vd.kVGA):
        """
        initilization
        
        :param IP: NAO's IP
        :param PORT: NAO's PORT
        :param cameraId: bottom camera for 1 and top camera for 0
        :param resolution: kVGA, 640*480
        
        :return: none
        """
        super(VisualBasis, self).__init__(IP,PORT)
        self._IP = IP
        self._PORT = PORT
        self.cameraId = cameraId
        self.cameraName = "CameraBottom" if self.cameraId == vd.kBottomCamera else "CameraTop"
        self.resolution = resolution
        self.colorSpace = vd.kBGRColorSpace
        self.fps = 20
        self.frameHeight = 0
        self.frameWidth = 0
        self.frameChannels = 0
        self.frameArray = None
        self.cameraPitchRange = 47.64/180*np.pi
        self.cameraYawRange = 60.97/180*np.pi
        self.cameraProxy.setActiveCamera(self.cameraId)

    def updateFrame(self, client = "The host computer"):
        """
        get a new image from the specified camera and save it in self.frame
        
        :param client: client name
        
        :return: none
        """
        if self.cameraProxy.getActiveCamera() != self.cameraId:
            self.cameraProxy.setActiveCamera(self.cameraId)
            time.sleep(1)

        videoClient = self.cameraProxy.subscribe(client, self.resolution, self.colorSpace, self.fps)
        frame = self.cameraProxy.getImageRemote(videoClient)
        self.cameraProxy.unsubscribe(videoClient)
        try:
            self.frameWidth = frame[0]
            self.frameHeight = frame[1]
            self.frameChannels = frame[2]
            self.frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frame[1],frame[0],frame[2]])
        except IndexError:
            print("get image failed")

    def getFrameArray(self):
        """
        get current frame
        
        :return: current frame array
        """
        if self.frameArray is None:
            return np.array([])
        return self.frameArray

    def showFrame(self):
        """
        show current 
        """
        if self.frameArray is None:
            print("please get an image from Nao with the method updateFrame()")
        else:
            cv2.imshow("current frame", self.frameArray)

    def printFrameData(self):
        """
        print current frame date
        """
        print("frame height = ", self.frameHeight)
        print("frame width = ", self.frameWidth)
        print("frame channels = ", self.frameChannels)
        print("frame shape = ", self.frameArray.shape)

    def saveFrame(self, framePath):
        """
        save current frame to specified direction.
        
        :param framePath: image path
        """
        cv2.imwrite(framePath, self.frameArray)
        print("current frame image has been saved in ", framePath)

    def setParam(self, paramName=None, paramValue=None):
        raise NotImplementedError

    def setAllParamsToDefault(self):
        raise NotImplementedError






