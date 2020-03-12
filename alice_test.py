import aiml
import os

os.chdir('./alice')
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond('LOAD ALICE')

if __name__ == '__main__':
    while True:
        text = input('我说：')
        res = alice.respond(text)
        print('ALICE说：' + res)
