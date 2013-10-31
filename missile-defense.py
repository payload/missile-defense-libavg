#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import random

import libavg as avg
from libavg import app



class Drug(object):
    def __init__(self, **kwargs):
        for k, w in kwargs.items():
            setattr(self, k, w)



def P(*args):
    for x in args:
        print x,
    print ""
    return args[-1:][0]



def sequentialAnim(anims, repeat = False, wait = 0):
    anims = list(anims)
    assert len(anims) > 0
    from itertools import chain, izip
    if wait > 0:
        waits = (avg.WaitAnim(wait) for _ in range(len(anims)))
        anims = list(chain(*izip(anims, waits)))
    for animA, animB in izip(anims, anims[1:]):
        _sequentialAnim(animA, animB)
    if repeat:
        _sequentialAnim(anims[-1:][0], anims[0])
    return anims[0]

def _sequentialAnim(animA, animB):
    animA.setStopCallback(lambda: animB.start())



def linearAnim(
        node, attrNames, duration, startValue, endValue, useInt=False,
        startCallback=None, stopCallback=None):
    if isinstance(attrNames, str):
        attrNames = map(str.strip, attrNames.split(","))
    assert len(attrNames) > 0
    anims = [
        avg.LinearAnim(node, attrName, duration, startValue, endValue, useInt)
        for attrName in attrNames]
    panim = avg.ParallelAnim(anims, startCallback, stopCallback, 10)
    anims[0].setStopCallback(lambda: panim.abort())
    return panim



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
        
        for child in self.children():
            onFrame = getattr(child, "onFrame", None)
            if onFrame:
                onFrame(dt)
        
        missiles = [m for m in self.children() if isinstance(m, Missile)]
        explosions = [e for e in self.children() if isinstance(e, Explosion)]
        for missile in missiles:
            for explosion in explosions:
                diff = explosion.pos - missile.pos2
                if diff.getNorm() < explosion.r:
                    missile.explode()
                    break
            
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
        pos2 = avg.Point2D(pos2)
        diff = pos2 - self.pos1
        vel = diff.getNormalized() * speed
        eta = diff.getNorm() / speed
        eta = int(eta * 1000)
        anim = avg.ParallelAnim([
            avg.ContinuousAnim(self, "pos2", self.pos1, vel),
            avg.WaitAnim(eta, stopCallback = self.explode)])
        anim.start()
        
    def explode(self):
        Explosion(
            parent = self.parent,
            pos = self.pos2)
        self.unlink(True)



class Explosion(avg.CircleNode):

    def __init__(self,
            r = 80,
            parent = None,
            **kwargs):
        super(Explosion, self).__init__(**kwargs)
        self.registerInstance(self, parent)
        self.fillcolor = "FFFFFF"
        anim = avg.ParallelAnim([
            avg.LinearAnim(self, "r", 600, 0.1*r, r),
            sequentialAnim([
                linearAnim(self, "fillopacity, opacity", 0, 1, 1),
                linearAnim(self, "fillopacity, opacity", 0, 0, 0)],
                repeat = True, wait = 100)
            ], None, lambda: self.unlink(True))
        anim.start()



def main():
    app.App().run(MyMainDiv())




if __name__ == "__main__":
    main()

