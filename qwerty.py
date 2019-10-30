# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 19:59:13 2019

@author: nki
"""

import tkinter as Tk
from tkinter import ttk, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename

import matplotlib.pyplot as plt

LARGER_FONT= ("Arial", 16)
LARGE_FONT= ("Arial", 12)
import datetime as dt



import numpy as np


import requests
import io
import time
from multiprocessing import Pool


import wrapt

@wrapt.decorator
def timer(wrapped, instance, args, kwargs, offset_length=25):
    start = dt.datetime.now()
    rv = wrapped(*args, **kwargs)
    end = dt.datetime.now()
    diff = end-start
    print('{.__name__}:{} {:10.4f}s'.format(wrapped,' '*(offset_length-wrapped.__name__.__len__()),diff.total_seconds()))
    return rv



def get_sound(search_term):
    print(search_term)
    url = f'https://sproget.dk/lookup?SearchableText={search_term}'
    response = requests.get(url)

    mp3 = str(response.content)[str(response.content).find('.mp3')-100+55:str(response.content).find('.mp3')+4]
    bts = io.BytesIO(requests.get(mp3).content)
#    bts.seek(0)
    return bts#response.content




#def f(s):
#    return s*2
#p = Pool(3)
#res = p.map(get_sound, ['jeg', 'telefon'])
#if __name__ == '__main__':
#    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
#    p = Pool(processes = 4)
#    print(p.map( f, ['jeg', 'telefon']   ))
#    for r in ['jeg', 'er']:
#        print(f(r))









test = get_sound('er')
#mp3 = str(test)[str(test).find('.mp3')-100+55:str(test).find('.mp3')+4]
#sound = requests.get(mp3)
#with open('hest.mp3','rb') as fin:
#    sound2 = fin.read()


#import pygame
#pygame.mixer.init()
#pygame.mixer.music.load(test)
#pygame.mixer.music.rewind()
#pygame.mixer.music.play()


#pygame.init()
#pygame.mixer.init()
##sound = pygame.mixer.Sound(sound2)
#sound = pygame.mixer.Sound(buffer=sound2)
#stop
#class Page(Tk.Frame):                               ####################
#    def __init__(self, *args, **kwargs):            ##          KEEP  ##
#        Tk.Frame.__init__(self, *args, **kwargs)    ##    <---- PAGE  ##
#    def show(self):                                 ##          CLASS ##
#        self.lift()                                 ## AND KEEP       ##
                                                    ## "Page1" AS     ##
class Page1(Tk.Frame):                              ## <-- CLASS NAME ##
    def __init__(self, parent, *args, **kwargs):     ####################
        self.parent = parent # Parent == MainView(Tk.Tk)
        super().__init__(*args, **kwargs) # Initialize Page(frame)
        self.pagename = ttk.Label(self, text="This is page: %s"%__name__, font = LARGE_FONT) # Page name
        self.pagename.grid()#(row=0, column=0, fill=None, sticky='nw')                         # Location of page name

        ## YOUR CODE GOES HERE ...
        self.last_press = dt.datetime.now()

        ## PLOT INITIALIZATION ##
#        self.f = plt.Figure(figsize=(9.2,9.2),dpi=100) # figsize=(10.9,10.9),
#        self.plot_fit = {'pad':0.25,'w_pad':0.01,'h_pad':0.01, 'rect': (0,0,1,0.96)}  #{'pad':1.5,'h_pad':0.5, 'rect': (0,0,1,0.96)} # {'pad':0.25,'w_pad':0.01,'h_pad':0.01, 'rect': (0,0,1,0.96)}     {'w_pad':0.01, 'rect': (0,0,1,0.96)}
#        self.f.set_tight_layout(self.plot_fit)

        ## FRAME SETUP (incl. canvas area)
        self.frame   = Tk.Frame(self, background="#f0f0f0").grid()#id(sticky='nw')#, width=2, height=1080)
        self.buttonframe   = Tk.Frame(self.frame, background="#f0f0f0").grid(row=10)#id(sticky='nw')#, width=2, height=1080)
#        self.canvasPanel   = NewFrame(self.plotFrame, background="grey", loc=(0,0))#width=1, height=1)
#        self.canvasPanel.columnconfigure(0,weight=1)
#        self.canvasPanel.rowconfigure(0,weight=1)

        self.legend_var = Tk.StringVar(self, '')
        self.legebdlegend = ttk.Label(self.frame, textvariable = self.legend_var, font=LARGER_FONT).grid(row=10,columnspan=100)#(row=0,column=0)#, command=lambda: self._set_date_db(time='start')))

        self.build_keyboard()
        self.sounds = {}


    @staticmethod
    def f(key, s2):
        return key

    @timer
    def build_keyboard(self,capslock=False):
        self.buttons, self.buttonVars = {}, {}
        keys = ['qwertyuiop','asdfghjkl','zxcvbnm']
        keys = [l.upper() if capslock else l.lower() for l in keys]
        for i,row in enumerate(keys):
            for j,key in enumerate(row):
                self.buttonVars[key] = Tk.StringVar(0,key)
                self.buttons[key] = Tk.Button(self.buttonframe,textvariable = self.buttonVars[key],font=LARGER_FONT, command = lambda key=key: self.event_generate(f'<{key}>'))
                self.buttons[key].grid(row=i,column=j)
#                self.winfo_toplevel().bind(f'<{key.upper()}>', lambda key=key: self.callback(key))
#                self.winfo_toplevel().bind(f'<{key.lower()}>', lambda key=key: self.callback(key))
#        key = 'Aring'
        self.winfo_toplevel().bind('<Key>', lambda key: self.callback(key))

        self.button_play = Tk.Button(self.buttonframe, text = 'Play', command = self.play)
        self.button_play.grid(row=100,column=0)
#        self.winfo_toplevel().bind(f'<BackSpace>', lambda key: self.callback(key))

    @timer
    def callback(self,key, *args, **kwargs):
        print(key, self.legend_var.get())
        now = dt.datetime.now()
        if key.keysym.lower() == 'backspace':
            self.legend_var.set(  self.legend_var.get()[0:-1]  )
        elif (now-self.last_press).total_seconds() > 4:
            self.legend_var.set( key.char )
        else:
            self.legend_var.set( self.legend_var.get() + key.char )
        self.last_press = now
#        self.parent.update_idletasks()
        print(f'key = {key}')

    @timer
    def play(self, *args, **kwargs):
        text = self.legend_var.get()
        play_sounds = []
        for word in text.split():
            if word not in self.sounds.keys():
                self.sounds[word] = get_sound(word)
            play_sounds.append(self.sounds[word])

        for sound in play_sounds:
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
            time.sleep(1)



if __name__ == '__main__':
    root = Tk.Tk()                                             # root for mainloop
    p1 = Page1(root)#.pack(side="top", fill="both", expand=True)
    root.mainloop()





#        @timer
#    @classmethod
#    def __create_function_gui__(cls, *args, **kwargs):
#        cls = cls(**kwargs)
#
#        cls.label = Tk.Label(cls, text  = '')
#        cls.label.grid(row=10,column = 5)
#
#        cls.funcs = []
#
#        for func in args:
#            cls.row += 1
#            frame = Tk.Frame(cls)
#            frame.label = Tk.Label(frame, text = f'{[func.__qualname__,"No name"][func.__qualname__==None]}')
#            frame.label.grid(row=0)
#            frame.grid(row=cls.row,column=0)
#            func = cls.__entry_vars__(func,frame)
#            cls.funcs.append(func)