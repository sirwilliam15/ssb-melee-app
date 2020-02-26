import slippi
import sys

def main():
    g = game('Test1.slp')

    for _ in rang(0,10):
        data = frame.ports[0].leader # see also: port.follower (ICs)
        print(data.post.state) # character's post-frame action state