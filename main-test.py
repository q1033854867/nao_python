#coding utf-8

from Configure import VisualBasis
import vision_definitions as vd

IP = "169.254.51.241"


visualBasic = VisualBasis(IP, cameraId=0, resolution=vd.kVGA)

visualBasic.updateFrame()
