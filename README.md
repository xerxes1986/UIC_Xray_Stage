# UIC_Xray_Stage

Files:
  motor_stage.py - elComondante base class for x-ray motor stages.
  phidgets_stepper.py - elComandante-compatible implementation of the x-ray rotary stage.
  UIC_stepper.py - Stand-alone wrapper for phidgets_stepper.py that allows 'manual' control of the rotary stage and targets.
  
The "0" position of the stage is found via a magnetic switch embeded in the rotation wheel during the initialization of the phidgets_stepper class. Then a position for the stepper motor (in units of 1/16 of a "step", 200 "steps" per revolution, 5-to-1 gear reduction --> 16000 positions per revolution) is sent to the controller and it goes to that location. This can be done via elComandante configuration files, or the provided UIC_stepper.py class which has the target locations programmed in it. 
