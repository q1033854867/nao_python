#coding utf-8
from Configure import VisualBasis
import vision_definitions as vd
import cv2
import numpy as np

class ColorDetection(VisualBasis):
    """
    derived from Visualbasics.used to recognize colers
    """

    def __init__(self, IP, PORT=9559, cameraId=vd.kBottomCamera, resolution=vd.kVGA, writeFrame=False):
        """
        initialization
        """
        super(ColorDetection, self).__init__(IP, PORT, cameraId,resolution)
        self.writeFrame = writeFrame

    def __getChannelAndBlur(self,color):
        """
        get the specified channel and blur the result.
        :param color: the color channel to split, only supports the color of red, geen and blue.   
        :return: the specified color channel or None (when the color is not supported).
        """
        try:
            channelB = self.frameArray[:, :, 0]
            channelG = self.frameArray[:, :, 1]
            channelR = self.frameArray[:, :, 2]
        except:
            print("do not get the image!")

        Hm = 6
        if color == "red":
            channelB = channelB * 0.1 * Hm
            channelG = channelG * 0.1 * Hm
            channelR = channelR - channelB - channelG
            channelR = 3 * channelR
            channelR = cv2.GaussianBlur(channelR, (9, 9), 1.5)
            channelR[channelR < 0] = 0
            channelR[channelR > 255] = 255
            return np.uint8(np.round(channelR))
        elif color == "blue":
            channelR = channelR * 0.1 * Hm
            channelG = channelG * 0.1 * Hm
            channelB = channelB - channelG - channelR
            channelB = 3 * channelB
            channelB = cv2.GaussianBlur(channelB, (9, 9), 1.5)
            channelB[channelB < 0] = 0
            channelB[channelB > 255] = 255
            return np.uint8(np.round(channelB))
        elif color == "green":
            channelB = channelB * 0.1 * Hm
            channelR = channelR * 0.1 * Hm
            channelG = channelG - channelB - channelR
            channelG = 3 * channelG
            channelG = cv2.GaussianBlur(channelG, (9, 9), 1.5)
            channelG[channelG < 0] = 0
            channelG[channelG > 255] = 255
            return np.uint8(np.round(channelG))
        else:
            print("can not recognize the color!")
            print("supported color:red, green and blue.")
            return None

    def __binImageHSV(self, minHSV1, maxHSV1, minHSV2, maxHSV2):
        """
        get binary image from the HSV image (transformed from BGR image)
        :param minHSV1: parameters [np.array] for the color.
        :param maxHSV1: parameters [np.array] for the color.
        :param minHSV2: parameters [np.array] for the color.
        :param maxHSV2: parameters [np.array] for the color.
        :return: binImage: binary image.
        """
        try:
            frameArray = self.frameArray.copy()
            imgHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
        except:
            print("no image detect!")
        else:
            frameBin1 = cv2.inRange(imgHSV, minHSV1, maxHSV1)
            frameBin2 = cv2.inRange(imgHSV, minHSV2, maxHSV2)
            frameBin = np.maximum(frameBin1, frameBin2)
            frameBin = cv2.GaussianBlur(frameBin, (9, 9), 1.5)
            return frameBin

