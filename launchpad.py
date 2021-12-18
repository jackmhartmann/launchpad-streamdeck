#!/bin/env python
from __future__ import print_function
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import sys
import random
import time
from pynput.keyboard import Key, Controller

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad.py")

keyboard = Controller()
muted = True
deafened = False
processes = []
lp = launchpad.Launchpad()
if lp.Open( 0 ):
	print("Launchpad Mk1")
	mode = "Mk1"
lp.Reset()

def cmdInput( prompt ):
	if sys.version_info.major == 2:
		inName = str(raw_input( prompt ))
	elif sys.version_info.major == 3:
		inName = str(input( prompt ))
	else:
		sys.exit(-1)

	return inName

def AdjustAudio(proc, level):
	global lp
	global processes
	sessions = AudioUtilities.GetAllSessions()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		if session.Process and session.Process.name() ==proc:
			new_level = level * (10/80)
			try:
				volume.SetMasterVolume(new_level, None)
				lv = int(8-level)
				if lv == 0:
					lv = 1
				if level == 0:
					for i in range(1,lv + 1):
						lp.LedCtrlXY(processes.index(proc),i,1,0)
				else:
					for i in range(lv,9):
						lp.LedCtrlXY(processes.index(proc),i,0,3)
					for i in range(1,lv):
						lp.LedCtrlXY(processes.index(proc),i,0,0)
			except:
				try:
					for i in range(1,9):
						lp.LedCtrlXY(processes.index(proc),i,1,1)
				except:
					pass

def ChangeDevice():
	keyboard.press(Key.alt)
	keyboard.press('a')
	keyboard.release(Key.alt)
	keyboard.release('a')

def muteDiscord():
	keyboard.press(Key.f15)
	keyboard.release(Key.f15)

def deafenDiscord():
	keyboard.press(Key.f16)
	keyboard.release(Key.f16)

def initAudio():
	global processes
	sessions = AudioUtilities.GetAllSessions()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		try:
			if session.Process.name() not in processes:
				processes.append(session.Process.name())
			AdjustAudio(session.Process.name(), volume.GetMasterVolume() * 8)
			#print(session.Process.name(), volume.GetMasterVolume())
		except:
			pass



def main():
	global lp
	global muted
	global deafened
	global processes
	processes = ["chrome.exe", "Discord.exe", "EscapeFromTarkov.exe", "Spotify.exe"]
	initAudio()

	print("Setup Audio Complete")
	lastBut = (-99,-99)
	lp.LedCtrlXY(8,1,3,3)
	lp.LedCtrlXY(8,8,3,0)
	lp.LedCtrlXY(8,7,3,0)
	print(processes)
	tStart = time.time()
	while True:

		initAudio()
		buts = lp.ButtonStateXY()

		if buts != []:
			print( buts[0], buts[1], buts[2] )
			if buts[0] < 8 and buts[1] > 0:
				try:
					AdjustAudio(processes[buts[0]], 8-buts[1])
					print("Audio Adjusted", processes[buts[0]], "=",8-buts[1] )
				except:
					pass
			elif buts[0] == 8 and buts[1] == 1 and buts[2] == True:
				ChangeDevice()
			elif buts[0] == 8 and buts[1] == 8 and buts[2] == True:
				muteDiscord()
				if muted and deafened:
					print("test1")
					muted = False
					deafened = False
					lp.LedCtrlXY(8,8,0,3)
					lp.LedCtrlXY(8,7,0,3)
				elif not muted:
					print("test2")
					muted = True
					lp.LedCtrlXY(8,8,3,0)
				elif muted:
					print("test3")
					muted = False
					lp.LedCtrlXY(8,8,0,3)
				print(muted, deafened)
			elif buts[0] == 8 and buts[1] == 7 and buts[2] == True:
				deafenDiscord()
				if deafened and not muted:
					print("test6")
					deafened = False
					lp.LedCtrlXY(8,7,0,3)
					lp.LedCtrlXY(8,8,0,3)
				elif deafened:
					print("test4")
					deafened = False
					lp.LedCtrlXY(8,7,0,3)
				elif not deafened and not muted:
					print("test5")
					deafened = True
					lp.LedCtrlXY(8,8,3,0)
					lp.LedCtrlXY(8,7,3,0)
				else:
					deafened = True
					lp.LedCtrlXY(8,7,3,0)
				print(muted, deafened)

			# quit?
			if buts[1] == 0 and buts[0] == 7 and buts[2] > 0:
				break



	print("bye ...")

	lp.Reset() # turn all LEDs off
	lp.Close() # close the Launchpad (will quit with an error

if __name__ == '__main__':
	main()
