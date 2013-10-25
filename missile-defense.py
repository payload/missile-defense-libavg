#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random

import libavg as avg
from libavg import app



class Drug(object):
    def __init__(self, **kwargs):
        for k, w in kwargs.items():
            setattr(self, k, w)



Color = Drug(
    ship = "666666"
)



class MyMainDiv(app.MainDiv):

    def onInit(self):
        self.subscribe(self.CURSOR_UP, self.onCursorUp)

    def onExit(self):
        pass

    def onFrame(self):
        dt = avg.player.getFrameDuration() / 1000
        for line in self.children():
            onFrame = getattr(line, "onFrame", None)
            if onFrame:
                onFrame(dt)
        if random.random() < 0.02:
            self.newMissile()

    def children(self):
        return [self.getChild(i) for i in range(self.getNumChildren())]

    def newMissile(self, x1 = None, y1 = 0, x2 = None, y2 = 480):
        if x1 == None:
            x1 = random.randint(0, 640)
        if x2 == None:
            x2 = random.randint(0, 640)
        return Missile(
            parent = self,
            pos1 = (x1, y1),
            pos2 = (x2, y2))
            
    def onCursorUp(self, ev):
        step = float(640 / 5)
        i = round(ev.x / step)
        i = min(4, max(i, 1))
        x_start = i * step
        y_start = 480
        self.newMissile(x_start, y_start, ev.x, ev.y)


class Missile(avg.LineNode):

    def __init__(self,
            pos2 = (0,0),
            speed = 100,
            parent = None,
            **kwargs):
        super(Missile, self).__init__(**kwargs)
        self.registerInstance(self, parent)
        self.__pos2 = avg.Point2D(pos2)
        self.pos2 = self.pos1
        
        speed = float(speed)
        diff = self.__diff = self.__pos2 - self.pos1
        self.timeToLive = diff.getNorm() / speed
        self.progress = 0
        
    def onFrame(self, dt):
        progress = self.progress = self.progress + dt / self.timeToLive
        self.pos2 = self.pos1 + self.__diff * progress
        if progress >= 1:
            self.unlink(True)



def main():
    app.App().run(MyMainDiv())




if __name__ == "__main__":
    main()

