from getted.tedtalk import TEDTalkWidget
from getted.window import *
from getted.tedlister import GetTEDTalks
import shutil
import os
from multiprocessing import Process

def load_ted_talks(twl):
    print("Worker: Loading thumbnails")
    tl = GetTEDTalks() # Gets list of TED Talks
    for t in tl: # Convert TED Talks to widgets
       twl.append(TEDTalkWidget(t))
       print("Worker: {0}/{1} done".format(tl.index(t)+1, len(tl)))
    print("Worker: Finished")

def do_quit (sender, e):
    print('Quitting / Delete temporary files...')
    shutil.rmtree('/tmp/getted')
    Gtk.main_quit(sender, e)

def do_onload (sender, e):
    print('Window ready, loading talks...')
    talkwlist = []
    p = Process(target=load_ted_talks, args=(talkwlist,))
    p.start()
    p.join()
    sender.populate_ted_talks(talkwlist)

if __name__ == '__main__':
    print('Welcome to GetTED.')
    getted_window = GetTEDWindow()
    if not os.path.exists('/tmp/getted'):
        print('Creating a directory for temporary files')
        os.makedirs('/tmp/getted') # Create a temp directory for thumbnail files
    
    getted_window.set_title("GetTED")
    getted_window.connect('delete-event', do_quit)
    getted_window.connect('ready', do_onload)
    print('Starting GetTED window...')
    getted_window.show_all()
    Gtk.main()
