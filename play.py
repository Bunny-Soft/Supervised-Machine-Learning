
from utils import resize_image, XboxController, Screenshot
from termcolor import cprint
from PIL import ImageTk, Image
import mss
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.io import imread
import subprocess
from training import create_model
import numpy as np
import keyboard
sct = mss.mss()
from time import sleep

# Play
class Actor(object):

	def __init__(self):
		# Load in model from train.py and load in the trained weights
		self.model = create_model(keep_prob=1) # no dropout
		self.model.load_weights('model_weights.h5')

		# Init contoller for manual override
		self.real_controller = XboxController()

	def get_action(self, obs):

		### determine manual override
		manual_override = self.real_controller.LeftBumper == 1

		if not manual_override:
			## Look
			vec = resize_image(obs)
			vec = np.expand_dims(vec, axis=0) # expand dimensions for predict, it wants (1,66,200,3) not (66, 200, 3)
			## Think
			joystick = self.model.predict(vec, batch_size=1)[0]

		else:
			joystick = self.real_controller.read()
			joystick[1] *= -1 # flip y (this is in the config when it runs normally)


		## Act

		### calibration
		output = [
			int(joystick[0] * 80),
			int(joystick[1] * 80),
			int(round(joystick[2])),
			int(round(joystick[3])),
			int(round(joystick[4])),
		]
		pressed = ''
		if output[0] > 30:
			keyboard.press('right')
			pressed += 'right '
		if output[0] < -30:
			keyboard.press('left')
			pressed += 'left '
		if output[1] > 30:
			keyboard.press('up')
			pressed += 'up '
		if output[1] < -30:
			keyboard.press('down')
			pressed += 'down '
		if output[2] > 0.5:
			keyboard.press('z')
			pressed += 'z '
		if output[3] > 0.5:
			keyboard.press('z')
			pressed += 'z '

		### print to console
		if manual_override:
			print("Manual: " + str(output)+ "Pressed: " + pressed)
		else:
			print("AI: " + str(output)+ "Pressed: " + pressed)
		return output

def take_screenshot():
	# Get raw pixels from the screen
	sct_img = sct.grab({"top": Screenshot.OFFSET_Y,"left": Screenshot.OFFSET_X,"width": Screenshot.SRC_W,"height": Screenshot.SRC_H})

	# Create the Image
	return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

if __name__ == '__main__':
	subprocess.Popen(['C:\\Program Files\\BizHawk\\EmuHawk.exe'])
	actor = Actor()
	end_episode = False
	while not end_episode:
		temp = take_screenshot()
		temp.save("temp.png")
		image = imread("temp.png")
		action = actor.get_action(image)
		sleep(.05)
		keyboard.release('right')
		keyboard.release('left')
		keyboard.release('up')
		keyboard.release('down')
		keyboard.release('z')
