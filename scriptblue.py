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

def FirstPhaseM(robot):
    x_r,y_r=robot.GetPosition()
    #insert base finding code
    if robot.investigate_up()=='enemy-base':
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
    typ=robot.GetInitialSignal()[0]
    x_r,y_r=robot.GetPosition()
    
    x_d=int(baes[1:3])
    y_d=int(baes[3:5])
    x_b=int(baes[6:8])
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
    elif typ=='m': #scanners go on..dw
        i=int(robot.GetInitialSignal()[1:]) #because each bot covers a strip of width 3 and quadrant has size X/2, hence i_max for vertical branch = X/6
        if i <= X//6: #enter the last index for the vertical going bots
            if y_r == y_b and not(x_r ==(2+3*i)):
                if x_r < (2+3*i):
                    return 2
                elif x_r > (2+3*i):
                    return 4
            elif x_r == (2+3*i) and y_r >= y_b and y_r < X-1:
                return 1
            elif y_r == Y-1 and x_r < X:
                return 2
        else:
            if x_r == x_b and y_r !=(2+3*i):
                if y_r < (2+3*i):
                    return 1
                elif y_r > (2+3*i):
                    return 3
            elif y_r == (2+3*i) and x_r >= x_b and x_r < X-1:
                return 2
            elif x_r == X-1 and y_r < Y:
                return 1
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
    #investigation
    #if robot.GetVirus() > 1000:##change
        #robot.DeployVirus(200)
    #movement    
    if robot.GetCurrentBaseSignal()[0]=='~':
        return FirstPhaseM(robot) 
    #if robot.CurrentBaseSignal()[0]=='b':
        #return randint(1,4)#endgame boys


def ActBase(base):
    ##initialisation step
    if base.GetYourSignal()=='':
        x_b,y_b=base.GetPosition()
        x_est=base.GetDimensionX()-x_b  # A good guess for expected location of opponent base,
        y_est=base.GetDimensionX()-y_b  # could help with finding enemy base quickly
        base.SetYourSignal('~'+CoordStr(x_est,y_est)+'O'+CoordStr(x_b,y_b))#optimise later
        #botcreation
        i=0
        while base.GetElixir() > 1200 and i< base.GetDimensionX()//3:
            base.create_robot('m'+str(i))  # scanner with signal of its path index
            i+=1
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
        base.SetYourSignal(base.GetYourSignal()+'h'+str(enemies_near))

    ##add the base defense/attack mechn!!
    return
