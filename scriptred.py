from random import randint




    
# 1-11 are defence bots
# 12-30 are attack bots


def ActRobot(robot):
	init = robot.GetInitialSignal()
	base_signal = robot.GetCurrentBaseSignal()
	arr = []
	for i in range(len(init)):
		if init[i] == ',':
			arr.append(i)
	id = int(init[0:arr[0]])
	bot_x, bot_y = robot.GetPosition()
	base_x = int(init[arr[0]+1:arr[1]])
	base_y = int(init[arr[1]+1:])
	up = robot.investigate_up()
	down = robot.investigate_down()
	left = robot.investigate_left()
	right = robot.investigate_right()
	nw = robot.investigate_nw()
	ne = robot.investigate_ne()
	sw = robot.investigate_sw()
	se = robot.investigate_se()
	if id <= 11:
		
		if up == 'enemy' or down == 'enemy' or left == 'enemy' or right == 'enemy' or ne == 'enemy' or nw == 'enemy' or se == 'enemy' or sw == 'enemy':
			robot.setSignal('alarm')
			if (id == 1 or id == 3 or id == 5 or id == 7) and ('alarm' in base_signal) and ('form' in base_signal):
				if robot.GetVirus() > 400:
					if id == 1 and (ne == 'enemy' or right == 'enemy' or down == 'enemy' or sw == 'enemy'):
						robot.DeployVirus(200)
					elif id == 3 and (nw == 'enemy' or left == 'enemy' or down == 'enemy' or se == 'enemy'):
						robot.DeployVirus(200)
					elif id == 5 and (up == 'enemy' or left == 'enemy' or ne == 'enemy' or sw == 'enemy'):
						robot.DeployVirus(200)
					elif id == 	7 and (up == 'enemy' or right == 'enemy' or nw == 'enemy' or se == 'enemy'):
						robot.DeployVirus(200)
					elif id == 1 and se == 'enemy':
						robot.DeployVirus(100)
					elif id == 3 and sw == 'enemy':
						robot.DeployVirus(100)
					elif id == 5 and nw == 'enemy':
						robot.DeployVirus(100)
					elif id == 7 and ne == 'enemy':
						robot.DeployVirus(100)
				else:
					robot.DeployVirus(robot.GetVirus())
			else:
				robot.DeployVirus(min(robot.GetVirus(), 400))									


		#if base_signal.find('base found'):
		#	spot = int(base_signal[-1:])   #the id of robot which found the base. also add the direction in which it found the base to know exact co-ordinates	
		if 'alarm' in base_signal:  #tell the base 'form' to confirm all are at corners
			if not ('form' in base_signal):
				if id == 1:
					robot.setSignal('alarm')    
				if id == 1 or id == 2:
					if bot_x == base_x-1 and bot_y == base_y-1:
						if id == 1:
							robot.setSignal('d')
						return 0
					if bot_x < base_x-1:
						return 2
					elif bot_x > base_x-1:
						return 4
					if bot_y < base_y-1:
						return 3
					elif bot_y > base_y-1:
						return 1
				elif id == 3 or id == 4:
					if bot_x == base_x+1 and bot_y == base_y-1:
						if id == 3:
							robot.setSignal('o')
						return 0
					if bot_x < base_x+1:
						return 2
					elif bot_x > base_x+1:
						return 4
					if bot_y < base_y-1:
						return 3
					elif bot_y > base_y-1:
						return 1
				elif id == 5 or id == 6:
					if bot_x == base_x+1 and bot_y == base_y+1:
						if id == 5:
							robot.setSignal('n')
						return 0
					if bot_x < base_x+1:
						return 2
					elif bot_x > base_x+1:
						return 4
					if bot_y < base_y+1:
						return 3
					elif bot_y > base_y+1:
						return 1
				elif id == 7 or id == 8:
					if bot_x == base_x-1 and bot_y == base_y+1:
						if id == 7:
							robot.setSignal('e')
						return 0
					if bot_x < base_x-1:
						return 2
					elif bot_x > base_x-1:
						return 4
					if bot_y < base_y+1:
						return 3
					elif bot_y > base_y+1:
						return 1
			elif 'form' in base_signal:
				robot.setSignal('alarmform') 	
				if id == 9 or id == 10 or id == 11:
					return randint(1, 4)			


		elif base_signal == ' ':
			if abs(base_x - bot_x) <= 3 and abs(base_y - bot_y) <= 3:
				return(randint(1, 4))
			if bot_x - base_x > 3:
				return 4
			elif bot_x - base_x < -3:
				return 2
			if bot_y - base_y > 3:
				return 1
			elif bot_y - base_y < -3:
				return 3

	#else:

	return 0

def ActBase(base):
	if base.GetElixir() > 500:
		for i in range(1, 31):
			base.create_robot(str(i) + ',' + str(base.GetPosition()[0]) + ',' + str(base.GetPosition()[1]))
		
	bot_signals = base.GetListOfSignals()
	signal = ' '
	done = [0, 0, 0, 0]
	for s in bot_signals:
		if 'alarm' in s and len(signal) <= 20:
			signal += 'alarm'
		if ('d' in s):    #make sure that these characters dont appear in s anywhere else
			done[0] = 1
		if ('o' in s):    #make sure that these characters dont appear in s anywhere else
			done[1] = 1
		if ('n' in s):    #make sure that these characters dont appear in s anywhere else
			done[2] = 1
		if ('e' in s):    #make sure that these characters dont appear in s anywhere else
			done[3] = 1
		if 'form' in s:
			signal += 'form'		
			
		#if s.find('base found'):
		#	signal += 'base found'
	if done[0] == 1 and done[1]	 == 1 and done[2] == 1 and done[3] == 1:
		signal += 'form'
	base.SetYourSignal(signal)			    

	return