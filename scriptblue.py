from random import randint
from random import choice

def CoordStr(x,y): # x,y<100
	if x<10:
		xs='0'+str(x)
	else:
		xs=str(x)
	if y<10:
		ys='0'+str(y)
	else:
		ys=str(y)
	return xs+ys

def VirusPolicy(robot,typ):
	viral=robot.GetVirus()
	up = robot.investigate_up()
	down = robot.investigate_down()
	left = robot.investigate_left()
	right = robot.investigate_right()
	ne = robot.investigate_ne()
	nw = robot.investigate_down()
	se = robot.investigate_left()
	sw = robot.investigate_right()
	locale=(up,down,left,right,ne,nw,se,sw)
	if 'enemy-base' in locale:
		if viral>4000:
			robot.DeployVirus(4000)
		else:
			robot.DeployVirus(viral/2) #alter
	elif 'enemy' in locale:
		numen=locale.count('enemy')
		if typ=='a'or typ=='m':
			if numen>2:
				robot.DeployVirus(800)	#alter the values
			else:
				robot.DeployVirus(320)	#alter the values
			
			

	
def FirstPhaseM(robot,typ):
	x_r,y_r=robot.GetPosition()
	#insert base finding code
	if robot.investigate_up()=='enemy-base': #rem--chk 
		robot.setSignal('b'+CoordStr(x_r,y_r-1))       
	elif robot.investigate_down()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r,y_r+1))       
	elif robot.investigate_left()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r-1,y_r))
	elif robot.investigate_right()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r+1,y_r))
	elif robot.investigate_ne()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r+1,y_r-1))
	elif robot.investigate_nw()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r-1,y_r-1))
	elif robot.investigate_se()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r+1,y_r+1))
	elif robot.investigate_sw()=='enemy-base':
		robot.setSignal('b'+CoordStr(x_r-1,y_r+1))
	
	#the movement defining code
	baes=robot.GetCurrentBaseSignal()
	x_r,y_r=robot.GetPosition()
	
	x_d=int(baes[1:3]) #destination estimation
	y_d=int(baes[3:5])
	x_b=int(baes[6:8]) #home
	y_b=int(baes[8:10])
	
	X = robot.GetDimensionX()
	Y = robot.GetDimensionY()

	pstring='1234' 
	if typ=='a': #direct scouts  
		if x_r<x_d:
			pstring+='2'*(x_d-x_r) 
		else:
			pstring+='4'*(x_r-x_d)
		if y_r>y_d:
			pstring+='1'*(y_r-y_d)
		else:
			pstring+='3'*(y_d-y_r)
		return int(choice(pstring))
	elif typ=='m': #scanners go on
		i=int(robot.GetInitialSignal()[1:])
		# 1 up, 2 right, 3 down, 4 left

		if i%2 == 0:    #Clockwise scanners
			i = i//2
			if (x_b<X//2 and y_b<Y//2):
				if (x_r==x_b and not(y_r==2+3*i)):
					if (y_r<2+3*i):
						return 1	#move up
					else:
						return 3	#move down
				elif (y_r==2+3*i and x_r<X+2-3*i):
					return 2     #move right
				elif (x_r==X+2-3*i):
					return 3	#move down
	
			elif (x_b>= X//2 and y_b<Y//2):
				if (y_r==x_b and not(x_r==X+2-3*i)):
					if (x_r<X+2-3*i):
						return 2	#move right
					else:
						return 4	#move left
				elif (x_r==X+2-3*i and y_r<Y+2-3*i):
					return 3     #move down
				elif (y_r==Y+2-3*i):
					return 4	#move left
			
			elif (x_b<X//2 and y_b>=Y//2):
				if (y_r==y_b and not(x_r==2+3*i)):
					if (x_r<2+3*i):
						return 2	#move right
					else:
						return 4	#move left
				elif (x_r==2+3*i and y_r<2+3*i):
					return 1     #move up
				elif (y_r==2+3*i):
					return 2	#move right
			
			elif (x_b>=X//2 and y_b>=Y//2):
				if (x_r==x_b and not(y_r==Y+2-3*i)):
					if (y_r<Y+2-3*i):
						return 3	#move down
					else:
						return 1	#move up
				elif (y_r==Y+2-3*i and x_r>2+3*i):
					return 4     #move left
				elif (x_r==2+3*i):
					return 1	#move up

		else:   #Anticlockwise scanners
			i=i//2
			if (x_b<X//2 and y_b<Y//2):
				if (y_r==y_b and not(x_r==2+3*i)):
					if (x_r<2+3*i):
						return 2	#move right
					else:
						 return 4	#move left
				elif (x_r==2+3*i and y_r<Y+2-3*i):
					return 3     #move down
				elif (y_r==Y+2-3*i):
					return 2	#move right
	
			elif (x_b>= X//2 and y_b<Y//2):
				if (x_r==x_b and not(y_r==2+3*i)):
					if (y_r<2+3*i):
						return 1	#move up
					else:
						 return 3	#move down
				elif (y_r==2+3*i and x_r>2+3*i):
					return 4     #move left
				elif (x_r==2+3*i):
					return 3	#move down
			
			elif (x_b<X//2 and y_b>=Y//2):
				if (x_r==x_b and not(y_r==Y+2-3*i)):
					if (y_r<Y+2-3*i):
						return 3	#move down
					else:
						 return 1	#move up
				elif (y_r==Y+2-3*i and x_r<X+2-3*i):
					return 2     #move right
				elif (x_r==X+2-3*i):
					return 1	#move up
			
			elif (x_b>=X//2 and y_b>=Y//2):
				if (y_r==y_b and not(x_r==X+2-3*i)):
					if (x_r<X+2-3*i):
						return 2	#move right
					else:
						 return 4	#move left
				elif (x_r==X+2-3*i and y_r>2+3*i):
					return 1     #move up
				elif (y_r==2+3*i):
					return 4	#move left


	else: #defence
		#if help condition either alter this or signal[0]
		if abs(x_r-x_b)+abs(y_r-y_b)<20-2*baes.count('h'):        
			return randint(1,4)
		else:
			if x_r<x_b:
				pstring+='2'*(x_b-x_r)
			else:
				pstring+='4'*(x_r-x_b)
			if y_r>y_b:
				pstring+='1'*(y_r-y_b)
			else:
				pstring+='3'*(y_b-y_r)
			return int(choice(pstring))


def ActRobot(robot):
	typ=robot.GetInitialSignal()[0]
	#investigation
	VirusPolicy(robot,typ)
	
	#movement    
	if robot.GetCurrentBaseSignal()[0]=='~':
		return FirstPhaseM(robot,typ) 
	#if robot.CurrentBaseSignal()[0]=='b':
		#return randint(1,4) #e boys
	else:
		return randint(1,4)


def ActBase(base):
	##initialisation step
	if base.GetYourSignal()=='':
		x_b,y_b=base.GetPosition()
		x_est=base.GetDimensionX()-x_b  # A good guess for expected location of opponent base,
		y_est=base.GetDimensionX()-y_b  # could help with finding enemy base quickly
		base.SetYourSignal('~'+CoordStr(x_est,y_est)+'O'+CoordStr(x_b,y_b))#optimise later
		#botcreation
		i=0
		#while base.GetElixir() > 500 and i<= 2*(base.GetDimensionX()//6):
			#base.create_robot('m'+str(i))  # scanner with signal of its path index
		while base.GetElixir() > 1000:
			base.create_robot('a')  # search directly
		while base.GetElixir() > 500:
			base.create_robot('d')  # defence capability ->more conservative with movement

	All=base.GetListOfSignals()
	for L in All:
		if len(L)>0 and L[0]=='b':
			base.SetYourSignal(L[:5]+base.GetYourSignal()[5:]) #checkforerrors

	def enemies_near(): #??
		return (base.investigate_up()=='enemy')+(base.investigate_down()=='enemy')+(base.investigate_left()=='enemy')+(base.investigate_right()=='enemy')+(base.investigate_ne()=='enemy')+(base.investigate_nw()=='enemy')+(base.investigate_se()=='enemy')+(base.investigate_sw()=='enemy')
	if enemies_near():
		base.DeployVirus(800) #100 per block
		base.SetYourSignal(base.GetYourSignal()+'h'*(enemies_near()))

	##put more logic in the base defense/attack mechn!!
	return
