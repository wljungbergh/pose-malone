# pose-malone
HackTheCrisis20 Pose Estimator pose-malone.

This repo contains submodules. Be sure to run `git submodule update --init --recursive` after cloning. To run the GUI simply go in to the top folder and run `main.py`. In order to more clearly see the underlying algorithm, instead run `tuning.py`. This comes with rendering in OpenCv.

The Pose Estimator is made up of the following submodules.
### Frame Capture
OpenCv is used to access the video feed from the webcam
### Frame Process
OpenCv:s Deep Neural Network is used to make the facedetections
### Headpose Estimator
The FSA-Net (https://github.com/shamangary/FSA-Net) developed for CVPR19 is used to track the users head orientation
### Filter
A simple moving average is applied to the measurements to filter high-frequecy noise. 
### Decision Maker
The decision maker makes decision based how far away from a 'good' initial posture we are. Currently bases decisions on position and rotation of the head as well as the users distance from the screen.
### GUI
Impolementation of the GUI is made in PyQt5. 
