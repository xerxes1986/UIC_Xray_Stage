## @file
# Implements the class that defines the standard interface for motor stages
# @ingroup xrayClient
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper
from time import sleep
from motor_stage import motor_stage

## Motor stage implementation for Phidgets stepper
#
# This motor stage implementation is specifically made for the
# PhidgetStepper made by the company Phidgets. It assumes the "true 0" reading
# is indicated by digital input 1 
# @ingroup xrayClient
class phidgets_stepper(motor_stage):
	## Constructor 
	#
	def __init__(self):
                motor_stage.__init__(self, 1)
		self.Initialized = True
                try:
                        self.stepper = Stepper()
                except RuntimeError as e:
                        print("Runtime Exception: %s" % e.details)
                        self.Initialized = False
		try:
                        self.stepper.setOnAttachHandler(self.StepperAttached)
                        self.stepper.setOnDetachHandler(self.StepperDetached)
                        self.stepper.setOnErrorhandler(self.StepperError)
                        self.stepper.setOnCurrentChangeHandler(self.StepperCurrentChanged)
                        self.stepper.setOnInputChangeHandler(self.StepperInputChanged)
                        self.stepper.setOnPositionChangeHandler(self.StepperPositionChanged)
                        self.stepper.setOnVelocityChangeHandler(self.StepperVelocityChanged)
                except PhidgetException as e:
                        print("Phidget Exception %i: %s" % (e.code, e.details))
                        self.Initialized = False

                print("Opening phidget object....")

                try:
                        self.stepper.openPhidget()
                except PhidgetException as e:
                        print("Phidget Exception %i: %s" % (e.code, e.details))
                        self.Initialized = False


                print("Waiting for attach....")

                try:
                    self.stepper.waitForAttach(10000)
                except PhidgetException as e:
                        print("Phidget Exception %i: %s" % (e.code, e.details))
                        try:
                                self.stepper.closePhidget()
                        except PhidgetException as e:
                                print("Phidget Exception %i: %s" % (e.code, e.details))
                                self.Initialized = False
                        self.Initialized = False
                else:
                    self.DisplayDeviceInfo()

                try:
                        self.stepper.setAcceleration(0,4000)
                        self.stepper.setVelocityLimit(0, 900)
                        self.stepper.setCurrentLimit(0, 0.700)
			sleep(1)
                except PhidgetException as e:
                        print("Phidget Exception %i: %s" % (e.code, e.details))
                
                if(self.Initialized): self.home()

        def __del__(self):
                try:
                        self.stepper.setEngaged(0,False)
                        self.stepper.closePhidget()
                except PhidgetException as e:
                        print("Phidget Exception %i: %s" % (e.code, e.details))

        #Information Display Function
	def DisplayDeviceInfo(self):
	        print("|------------|----------------------------------|--------------|------------|")
                print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
                print("|------------|----------------------------------|--------------|------------|")
                print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (self.stepper.isAttached(), self.stepper.getDeviceName(), self.stepper.getSerialNum(), self.stepper.getDeviceVersion()))
                print("|------------|----------------------------------|--------------|------------|")
                print("Number of Motors: %i" % (self.stepper.getMotorCount()))

	#Event Handler Callback Functions
	def StepperAttached(self,e):
                attached = e.device
                print("Stepper %i Attached!" % (attached.getSerialNum()))

	def StepperDetached(self,e):
                detached = e.device
                print("Stepper %i Detached!" % (detached.getSerialNum()))

	def StepperError(self,e):
                try:
                        source = e.device
                        print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
                except PhidgetException as e:
                        print("Phidget Exception %i: %s" % (e.code, e.details))

	def StepperCurrentChanged(self,e):
                source = e.device
                #print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))

	def StepperInputChanged(self,e):
                source = e.device
                print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))

	def StepperPositionChanged(self,e):
                source = e.device
                print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))

	def StepperVelocityChanged(self,e):
                source = e.device
                print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))


	## Tests whether the device file of the motor stage is open or not
	#
	# @return Boolean, whether the device file is open or not
	def is_open(self):
                retvalue = False
                try:
		        retvalue = self.stepper.isAttached()
                except PhidgetException as e:
                        retvalue = False
                return (retvalue and self.Initialized)

	## Tests whether communication with the device is established
	#
	# @return Boolean, whether the device answers or not.
	def test_communication(self):
		return self.is_open()

	## Moves the motor stage to a specific coordinate
	#
	# This function is supposed to command the motor stage
	# to move to a specific point which is given in the argument.
	# The function should wait until the position is reached
	# until it returns. If the position cannot be reached, False
	# should be returned.
	# @param coordinates Tuple of floating point coordinates that
	# descripe the position where the motor stage is supposed to
	# move. The number of items in the tuple has to match the
	# number of dimensions of the motor stage.
	# @return Boolean, whether or not the position was reached or not
	def move_absolute(self, coordinates):
                if not self.is_open():
                        return None
		if type(coordinates) != list or len(coordinates) != self.dimensions:
			return 0
		self.stepper.setTargetPosition(0,coordinates[0])
                self.stepper.setEngaged(0,True)
		sleep(1)
                while self.stepper.getCurrentPosition(0) != coordinates[0]:
                        pass
		sleep(1)
                retvalue = self.stepper.getCurrentPosition(0) == coordinates[0]
		return retvalue

	## Moves the motor stage to a specific coordinate relative
	#  to the current one
	#
	# This function is supposed to command the motor stage
	# to move to a specific point relative to the current point
	# which is given in the argument.
	# The function should wait until the position is reached
	# until it returns. If the position cannot be reached, False
	# should be returned.
	# @param coordinates Tuple of floating point coordinates that
	# descripe the position relative to the current position
	# where the motor stage is supposed to move. The number of
	# items in the tuple has to match the number of dimensions
	# of the motor stage.
	# @return Boolean, whether or not the position was reached or not
	def move_relative(self, coordinates):
                if not self.is_open():
                        return None
		if type(coordinates) != list or len(coordinates) != self.dimensions:
			return 0
		absolute_cords = coordinates
                absolute_cords[0] += self.stepper.getCurrentPosition(0)
                return self.move_absolute(absolute_cords)

	## Sets the acceleration of the motor stage
	#
	# This function should communicate with the device
	# and set the acceleration of the stage. The devices
	# that do not support this should return False.
	# @param acceleration Value that the acceleration should
	# be set to
	# @return Boolean, whether the operation was successful
	# or not. If the stage does not support this, it should
	# return False.
	def set_acceleration(self, acceleration):
                if not self.is_open():
                        return None
		if( (acceleration >= self.stepper.getAccelerationMin()) and (acceleration <= self.stepper.getAccelerationMax()) ):
                        self.Acceleration = acceleration
                        try:
                                self.stepper.setAcceleration(0,self.Acceleration)
                        except PhidgetException as e:
                                print("Phidget Exception %i: %s" % (e.code, e.details))


        def home_switch(self):
                if not self.is_open():
                        return False
                return self.stepper.getInputState(0)

	## Moves the device to the home position
	#
	# This function is supposed to move the motor stage to
	# its home position to reset its coordinates. The function
	# should not return until the movement is complete.
	# @return Boolean, whether the position was reached or not
	def home(self):
                        #self.stepper.setAcceleration(0,4000)
                        #self.stepper.setVelocityLimit(0, 900)
                if not self.is_open():
                        return False
		if not self.move_absolute([0]):
                        return False
		if self.home_switch():
		        #self.stepper.setTargetPosition(0,-500)
                        self.stepper.setEngaged(0,True)
			#while self.stepper.getCurrentPosition(0) != -500:
			#	pass
			#sleep(1)
			self.stepper.setCurrentPosition(0,0)
			sleep(1)			
                if not self.home_switch():
		        self.stepper.setTargetPosition(0,17000)
                        self.stepper.setEngaged(0,True)
                     
			beggining_set=False
			home_beggining=0
			end_set=False
			home_end=0
                        while self.stepper.getCurrentPosition(0) != 16000:
                                if (self.stepper.getInputState(0) and not beggining_set):
                                        print "Found home beggining!"
					home_beggining = self.stepper.getCurrentPosition(0) 
					beggining_set = True
				elif (beggining_set  and not end_set and not self.stepper.getInputState(0)):
					print "Found home end!"
					home_end = self.stepper.getCurrentPosition(0)
					end_set = True
					self.stepper.setTargetPosition(0, home_end+100)
				elif (beggining_set and end_set and self.stepper.getCurrentPosition(0) != 
				      (home_end+100)):
                                        self.stepper.setTargetPosition(0, (home_beggining+home_end)/2-50)
					sleep(1)
                                        break

                        if not self.home_switch():
                                print("Cannot find home position!")
                                return False
                        else:
				print("position is zero")
                                self.stepper.setCurrentPosition(0,0)
				sleep(1)
				return True

	## Resets the device and reinitialises it
	#
	# This function is supposed to bring the device in a known
	# state from which other operations can be performed.
	# @return Boolean, whether the operation was successful or not
	def reset(self):
                return self.home()

        

