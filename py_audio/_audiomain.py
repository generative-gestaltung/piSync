#!/usr/bin/env python

import time
from audiothread import AudioThread
import func



if __name__ == '__main__':


    f = open("code.py", "r")
    codestr = f.read()
    f.close()

    audioT = AudioThread (0, "audio", 0, "wave")
    audioT.start()

    #audioT.cmd({"cmd":"COMPILE", "code":"pwm=math.sin(phase*0.0001)\nval=func.pulse(phase*0.01, pwm)"})
    #audioT.cmd({"cmd":"COMPILE", "code":"pwm=math.sin(phase*0.0001)\nval=func.saw(phase*0.01)"})
    audioT.cmd({"cmd":"COMPILE", "code":codestr})

    time.sleep(5)
    audioT.cmd({"cmd":"STOP"})

