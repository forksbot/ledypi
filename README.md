<h1 align="center">
  <br>
    <img src="Resources/logo.png"  width="250"></a>
  <br>
  Ledypi
</h1>

<h4 align="center">Control you led strip with  RaspberryPi, Python and Android</a>.</h4>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://forthebadge.com/images/badges/made-with-python.svg"
         a>
  </a>
  <a href="https://forthebadge.com/images/badges/built-with-love.svg">
      <img src="https://forthebadge.com/images/badges/built-with-love.svg">
  </a>

</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#Patterns">Patterns</a> •
  <a href="#Installation">Installation</a> •
  <a href="#Testing">Testing</a> •
  <a href="#Contributing">Contributing</a>
</p>

<h4 align="center">
  Click video for tutorial 
</h4>

<p align="center" 
    href="https://youtu.be/c0NvfBiJOkw">
    <img src="Resources/ledyweb_tutorial.gif">
</p>


<br>
<br>


# Key Features
Choose from more than 10 pre-made patterns and implement your own.
The modular desing allows you to add the logic you wish by overriding a single method, then you can choose the pattern either trough ssh or on the android app.

- 14 pre-made patterns
- Customizable attributes for each one
- [Music reactive](#music-reactive-click-gif-for-video) 
- [Android app](AppInventor) for control 
- Firebase database
- Debug mode available 

On [develop branch](https://github.com/nicofirst1/ledypi/tree/develop):
- [LedyWeb](https://github.com/nicofirst1/ledyweb) online controller 
- Dynamic android app

# Patterns
Each pattern inherits from a [base class](src/patterns/default.py) with its own logic. This allows anyone to implement his own pattern simply by overriding a method (see more on the [readme](patterns/README.md)).

Moreover each pattern can be customized by changing the values of its attributes, more ahead.

## Fixed logic
There are more than 10 _standard_ pattern to choose from with a steady logic, that is a fixed behavior.

<h3 >Water</h3>

Bring the ocean home with the ocean pattern. You can choose the deepness with the parameters

![water demo](Resources/water_demo.gif)

<h3 >Fire</h3>

If you're cold then try the fire pattern.

![water demo](Resources/fire_demo.gif)

<h3 >Game of Life</h3>

Watch how life evolves with the famous [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) algorithm.

![gof demo](Resources/gof_demo.gif)



## Interactive
On top of these fixed patters there are two interactive patters whose behavior can completely change based on the user input"

### Music Reactive (click gif for video)
[![audio demo](Resources/audio_demo2.gif)](https://youtu.be/7PXDBr3uZmA) 

This pattern uses a microphone to visualize the music on your led strip. There are three different type of visualization:
- Spectrum: split the strip on subsequent frequency bands and visualize the amplitude as a mix of rgb values
- Energy: use an energy function to plot the sound on the leds
- Scroll: record the audio amplitude on a scrolling timeline.

### Equation
You can input a custom equation for the rgb values. Such equation can depend on:
- time: a time-step is kept so to evolve the function through time
- index: the position of the led-strip can also be used

For example the following patters is given with:
- red = _cos(t)_
- green = _sin(t)_
- blue = _idx_

![equation demo](Resources/equation_demo.gif)

# Installation 
For the installation check out the related [INSTALL markdown/](markdowns/INSTALL.md).

# Testing
If you get a `ModuleNotFoundError` source the python path with
```shell script
source scripts/app.sh  
```
Both the local and remote test relies on two processes to work, one of which is always the [gui](src/pc/gui.py).

### Local PC
To test first run the [gui](src/pc/gui.py) and then in a separate process run [patterns](./src/pc/test.py)
```shell script
python src/pc/gui.py
python src/pc/test.py
```

### Local RPI
If you wish to run a local test of the RaspberryPi you don't need the gui process, simply ssh into the rpi and execute the test

```shell script
python src/rpi/test.py PatternName 
```

### Remote 

You can test the remote configuration running the [connect](src/firebase/control.py) script which takes as **mandatory** inputs 
the credential json file and the mode (either 'pc' or 'rpi') which specify where the script is being run.

An example might be
```shell script
python src/gui.py
python src/firebase/connect.py credential.json pc
```
To run the remote app on your pc together with the gui, or 

```shell script
python src/firebase/connect.py credential.json rpi
```
To run it on the RaspberryPi.

#### Additional params
The [connect script](src/firebase/control.py)  accepts two optional arguments:
- _databaseURL_ : the url of your database (default [value](https://ledypie.firebaseio.com/), more in the [firebase tutorial](https://rominirani.com/tutorial-mit-app-inventor-firebase-4be95051c325)
- _pixels_ : the number of pixels (default 300).

To connect to a custom databaseURL with 64 leds on the rpi you should run

```shell script
python src/firebase/connect.py credential.json rpi --databaseURL https://customURL.firebaseio.com/ --pixels 64
```

# Contributing
If you wish to support this project just fork it and add your pattern following the [readme](src/patterns/README.md).

<a href="https://paypal.me/dizzi17">
  <img src="https://img.shields.io/badge/-donate-0079C1.svg?style=for-the-badge&logo=paypal">
</a>
&nbsp;&nbsp
<a href="https://www.linkedin.com/in/nicol%C3%B2-brandizzi-04091b153/">
  <img src="https://img.shields.io/badge/-LinkedIn-2867b2.svg?style=for-the-badge&logo=linkedin">
</a>