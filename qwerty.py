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

# hello


import numpy as np


import requests
import io
import time, re
from multiprocessing import Pool
import pygame
import bs4
from functools import lru_cache


import wrapt

@wrapt.decorator
def timer(wrapped, instance, args, kwargs, offset_length=25):
    start = dt.datetime.now()
    rv = wrapped(*args, **kwargs)
    end = dt.datetime.now()
    diff = end-start
    print('{.__name__}:{} {:10.4f}s'.format(wrapped,' '*(offset_length-wrapped.__name__.__len__()),diff.total_seconds()))
    return rv


#@lru_cache()
def get_sound(search_term):
    print(search_term)

    url = f'https://sproget.dk/lookup?SearchableText={search_term}'
    response = requests.get(url)
#    pattern = re.compile(r'\.mp3')
#    matches = pattern.finditer(str(response.content))
#    for match in matches:
#        print(match)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    sounds = soup.find_all('audio')
    name, mp3 = None, None
    names = []
    while mp3 is None:
        for i,sound in enumerate(sounds):
            elements = list(sound.previous_elements)[:6]
            for elem in elements:
                if elem.__str__().startswith('<span class="k">'):
                    name = elem.contents[0]
                    if name == search_term:
                        mp3 = sound['src']
                        break;break;break#;continue
#                    else:
#                        names.append(name)
        break

    name = name if name is not None else search_term
    if mp3 is None:
        # Fall-back
        try:
            mp3 = sounds[0]['src']
#        mp3 = str(response.content)[str(response.content).find('.mp3')-100+55:str(response.content).find('.mp3')+4]

        except IndexError:
            print('No sounds found!')
            return name, b''

    bts = io.BytesIO(requests.get(mp3).content)
    return [name, bts]






#p = Pool(3)
#res = p.map(get_sound, ['jeg', 'telefon'])
#stoip
#if __name__ == '__main__':
#    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
#    p = Pool(processes = 4)
#    print(p.apply_async( get_sound, ['jeg', 'telefon']   ))


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
        self.legebdlegend = ttk.Entry(self.frame, textvariable = self.legend_var, font=LARGER_FONT).grid(row=10,columnspan=100)#(row=0,column=0)#, command=lambda: self._set_date_db(time='start')))

        self.build_keyboard()
        self.sounds = {}
        pygame.mixer.init()


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
            self.legend_var.set( self.legend_var.get())# + key.char )
        self.last_press = now
#        self.parent.update_idletasks()
        print(f'key = {key}')

    @timer
    def play(self, *args, **kwargs):
        text = self.legend_var.get()
        play_sounds = {}
        words = text.split()



        for word in text.split():
#            if word not in self.sounds.keys():
#                word, sound = get_sound(word)
#                self.sounds[word] = sound
#            play_sounds.append(self.sounds[word])
            key, sound = get_sound(word)
            play_sounds[key] = sound

        self.legend_var.set('')
#        self.update_idletasks()
        self.update()
        for key,sound in play_sounds.items():
            try:
                sound.seek(0)
                audio = pygame.mixer.music.load(sound)
                play  = pygame.mixer.music.play()
                self.legend_var.set(f'{self.legend_var.get()} {key}'.strip())
#                self.update_idletasks()
                self.update()
                while pygame.mixer.music.get_busy():
#                    print('waiting...')
                    time.sleep(0.05)
            except:
                pass




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