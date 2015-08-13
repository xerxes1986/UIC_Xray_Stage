from phidgets_stepper import *
stepper = phidgets_stepper()
## Moves the motor stage to a specific target
#
# This function is supposed to command the moror stage
# to move to a specific position. The posisitons of each 
# foil are prespecified. This function decides the most optimal 
# route to take (cw or ccw). Specificaly designed for UIC xray box.
def move(foil):
	target_position = [0]
	if foil == "Ag":
		target_position = [0]
	elif foil == "Mo":
		target_position = [2667]
	elif foil == "Cu":
		target_position = [5333]
	elif foil == "Tb":
		target_position = [8000]
	elif foil == "Sn":
		target_position = [10667]
	elif foil == "In":
		target_position = [13333]
	else:
		print("Valid arguments are Ag/In/Sn/Tb/Cu/Mo")
		return False
	stepper.move_absolute(target_position)
	return True

def zero():
	stepper.home()

while True:
    newtarget = raw_input("Enter Target Foil: ")
    print newtarget
    move(newtarget)

