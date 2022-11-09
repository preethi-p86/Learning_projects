import cv2         #image processing
import easygui      #to open the filebox
import numpy as np
import imageio

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image')
top.configure(background='white')
label= Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
  ImagePath = easygui.fileopenbox()
  cartoonify(ImagePath)

def cartoonify(ImagePath):

  #read the image
  originalImage = cv2.imread(ImagePath)
  originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
  # print(image)

  # confirm that image is chosen
  if originalImage is None:
    print('Cannot find any image. Choose appropriate file')
    sys.exit()

  resized_1 = cv2.resize(originalImage, (960,540))
  # plt.imshow(resized_1, cmap='gray')

  #converting an image to grayscale
  grayscale = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
  resized_2 = cv2.resize(grayscale, (960,540))
  # plt.imshow(resized_2, cmap'gray')

  #applying median blur to smoothen an image
  smoothgrayscale = cv2.medianBlur(grayscale, 5)
  resized_3 = cv2.resize(smoothgrayscale, (960,540))
  # plt.imshow(resized_3, cmap='gray')

  #retrieving the edges for cartoon effect
  #by using threshold technique
  getedge = cv2.adaptiveThreshold(smoothgrayscale, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9 , 9)
  
  resized_4 = cv2.resize(getedge, (960,540))
  # plt.imshow(resized_4, cmap='gray') 

  #applying bilatera; filter to remove noise
  #and keep edge sharp as required
  colorimage = cv2.bilateralFilter(originalImage, 9,300,300)
  resized_5 = cv2.resize(colorimage, (960,540))
  # plt.imshow(resized_5,cmap='gray')

  #masking edged image with our "BEAUTIFY" image
  cartoonimage = cv2.bitwise_and(colorimage, colorimage, mask=getedge)
  resized_6 = cv2.resize(cartoonimage, (960,540))
  # plt.imshow(resized_6, cmap='gray')

  #plotting the whole transition
  images  = [resized_1, resized_2, resized_3, resized_4, resized_5, resized_6]
  #images = [original, grayscaled, graysmoothened, edged, colorsmoothened, cartoonified]

  fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw = {'xticks':[], 'yticks': []}, gridspec_kw=dict(hspace=0.1,wspace=0.1))
  for i,ax in enumerate(axes.flat):
    ax.imshow(images[i], cmap='gray')

  save1 = Button(top,text="Save cartoon image", command=lambda : save(resized_6, ImagePath), padx=30, pady=5)
  save1.configure(background='#364156', foreground='white', font=('calibri',10,'bold'))
  save1.pack(side=TOP, pady=50)

  plt.show()

def save(resized_6, ImagePath):

  #saving an image using imwrite()
  newname = "cartoonified_image"
  path1 = os.path.dirname(ImagePath)
  extension = os.path.splitext(ImagePath)[1]
  path = os.path.join(path1, newname + extension)
  cv2.imwrite(path, cv2.cvtColor(resized_6, cv2.COLOR_RGB2BGR))
  I = "Image saved by name " + newname + " at" + path
  tk.messagebox.showinfo(title=None, message=I)

upload = Button(top,text="Cartoonify an Image", command = upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri',10,'bold'))
upload.pack(side=TOP, pady=50)

top.mainloop()
