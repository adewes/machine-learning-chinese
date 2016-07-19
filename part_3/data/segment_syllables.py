import pygame
import wave
import sys
import time
import tty
import termios

if __name__ == '__main__':
    pygame.mixer.init(16000,-16,1,4096*100)
    filename = sys.argv[1]
    wv = wave.open(filename)
    frames = wv.readframes(wv.getnframes())
    start = 0.0
    stop = 3.0
    framerate = 16000
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    windows = []
    di = 0.1
    snd = None
    try:
        while True:
            print "Playing..."
            print start,stop
            if snd is not None:
                snd.stop()
            snd = pygame.mixer.Sound(buffer(frames[(int(start*framerate)//2)*2:(int(stop*framerate)//2)*2]))
            snd.play()
            sys.stdin.flush()
            while True:
                key = sys.stdin.read(1)
                if ord(key) == 68:
                    print "Left!"
                    start-=di
                elif ord(key) == 67:
                    print "Right!"
                    start+=di
                elif ord(key) == 66:
                    print "Down!"
                    stop-=di
                elif ord(key) == 65:
                    print "Up!"
                    stop+=di
                elif ord(key) == 10:
                    windows.append((start,stop))
                    start = stop
                    stop = start+di*2.0
                    print "Enter!"
                else:
                    continue
                print "Braking"
                if start < 0:
                    start = 0
                if stop <= start:
                    stop = start+di
                break
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
