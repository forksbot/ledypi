# Usage
LedyPi is a project about LEDs and RasperryPi.
The scope of this project is to have an easy way to implement custom patterns on a led script in Python which can then be controlled trough the ssh or on the android app.

Here's a video tutorial showing how the app works on my strip.

[![Tutorial](http://img.youtube.com/vi/k1sSvwABXCE/0.jpg)](http://www.youtube.com/watch?v=k1sSvwABXCE )

# Installation 
For the installation check out the related [README](INSTALL.md).

# Patterns

## Logic fixed
There are more than 10 _standard_ pattern to choose from with a steady logic, that is a fixed behavior.

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
- index: the position of the ledstrip can also be used

For example the following patters is given with:
- red = _cos(t)_
- green = _sin(t)_
- blue = _idx_

[![equation demo](Resources/equation_demo.gif)]


# Testing
If you get a `ModuleNotFoundError` try to set the python path as follows in your terminal window:
```shell script
export PYTHONPATH=./src   
```
Both the local and remote test relies on two processes to work, one of which is always the [gui](src/pc/gui.py).

### Local PC
To test first run the [gui](src/pc/gui.py) and then in a separate process run [patterns](./src/pc/test.py)
```shell script
python src/pc/gui.py
python src/pc/test.py
```

### Local RPI
If you wish to run a local test of the rapsberrypi you don't need the gui process, simply ssh into the rpi and execute the test

```shell script
python src/rpi/test.py
```

### Remote 

You can test the remote configuration running the [connect](src/firebase/connect.py) script which takes as **mandatory** inputs 
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
To run it on the raspberrypi.

#### Additional params
The [connect script](src/firebase/connect.py)  accepts two optional arguments:
- _databaseURL_ : the url of your database (default [value](https://ledypie.firebaseio.com/), more in the [firebase tutorial](https://rominirani.com/tutorial-mit-app-inventor-firebase-4be95051c325)
- _pixels_ : the number of pixels (default 300).

To connect to a custom databaseURL with 64 leds on the rpi you should run

```shell script
python src/firebase/connect.py credential.json rpi --databaseURL https://customURL.firebaseio.com/ --pixels 64
```
