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

def randmoves(robot):
    rosig=robot.GetYourSignal()
    M=[1,2,3,4]
    if robot.investigate_up()=='wall':
        M.remove(1)
    elif robot.investigate_down()=='wall':
        M.remove(3)
    if robot.investigate_left()=='wall':
        M.remove(4)
    elif robot.investigate_right()=='wall':
        M.remove(2)
    if 'm' in rosig:
        ind=rosig.index('m')+1
        x=int(rosig[ind])+2
        if x>4: x=x-4
        if x in M:
            M.remove(x)
        move=choice(M)
        robot.setSignal(rosig[:ind]+str(move)+rosig[ind+1:])

    else:
        move=choice(M)
        robot.setSignal(rosig+'m'+str(move))

    return move

def WalkTo(x_r,y_r,x_d,y_d,randomiser):
    pstring='0'+'1234'*randomiser
    if x_r<x_d:
        pstring+='2'*(x_d-x_r) 
    else:
        pstring+='4'*(x_r-x_d)
    if y_r>y_d:
        pstring+='1'*(y_r-y_d)
    else:
        pstring+='3'*(y_d-y_r)
    return int(choice(pstring))





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
        if numen>2 and robot.GetVirus()>1000:
            robot.DeployVirus(800)	#alter the values
        elif robot.GetVirus()>5000:
            robot.DeployVirus(800)
        else:
            robot.DeployVirus(200)	#alter the values
        
            
            

    
def FirstPhaseM(robot,typ,id): #~
    x_r,y_r=robot.GetPosition()
    baes=robot.GetCurrentBaseSignal()
    x_d=int(baes[1:3]) #destination estimation
    y_d=int(baes[3:5])
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
    #el and robot.GetYourSignal=='': #reached near destination but do not see base yet
        #counter updated if no base
    else:
        rosig=robot.GetYourSignal()
        try:
            if rosig[0]=='t':            
                if int(rosig[1])>=8:
                    robot.setSignal('!'+rosig)
                else :
                    robot.setSignal('t'+str((int(rosig[1])+1)%10)+rosig[2:])
        except IndexError:
            if abs(x_d-x_r)+abs(y_d-y_r)<2:
                robot.setSignal('t0')
    #the movement defining code
   
    x_h=int(baes[6:8]) #home
    y_h=int(baes[8:10])
    

    if typ=='a': #direct scouts  
        return WalkTo(x_r,y_r,x_d,y_d)        
    elif typ=='m':
        return randmoves(robot)
    elif typ=='d': #defence
        #if help condition either alter this or signal[0]
        if abs(x_r-x_h)+abs(y_r-y_h)<=max(2,4*id-2*baes.count('h')):        
            return randmoves(robot)
        else:
            return WalkTo(x_r,y_r,x_h,y_h,0)

def SecondPhaseM(robot,typ,id): #!
    x_r,y_r=robot.GetPosition()
    #insert base finding code
    if robot.investigate_up()=='enemy-base': #rem--chk 
        robot.setSignal('b'+CoordStr(x_r,y_r-1))
        return choice((2,4))     
    elif robot.investigate_down()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r,y_r+1))
        return choice((2,4))       
    elif robot.investigate_left()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r-1,y_r))
        return choice((1,3)) 
    elif robot.investigate_right()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r+1,y_r))
        return choice((1,3)) 
    elif robot.investigate_ne()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r+1,y_r-1))
        return choice((1,2))
    elif robot.investigate_nw()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r-1,y_r-1))
        return choice((1,4))
    elif robot.investigate_se()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r+1,y_r+1))
        return choice((3,2))
    elif robot.investigate_sw()=='enemy-base':
        robot.setSignal('b'+CoordStr(x_r-1,y_r+1))
        return choice((3,4))
       
    #the movement defining code
    baes=robot.GetCurrentBaseSignal()
    
    x_d=int(baes[1:3]) #destination estimation
    y_d=int(baes[3:5])
    x_h=int(baes[6:8]) #home
    y_h=int(baes[8:10])
    
    
    if typ=='a'or typ=='m': #direct scouts
        
        return randmoves(robot)
    
    elif typ=='d': #defence
        #if help condition either alter this or signal[0]
        if abs(x_r-x_h)+abs(y_r-y_h)<=max(2,3*id-2*baes.count('h')):        
            return randmoves(robot)
        else:
            return WalkTo(x_r,y_r,x_h,y_h)

def EndPhase(robot,typ,id):
    x_r,y_r=robot.GetPosition()
    baes=robot.GetCurrentBaseSignal()  
    x_d=int(baes[1:3]) #destination
    y_d=int(baes[3:5])
    x_h=int(baes[6:8]) #home
    y_h=int(baes[8:10])

    if typ=='a'or typ=='m':
        if abs(x_r-x_d)+abs(y_r-y_d)==1:
            if x_r==x_d:
                return choice((2,4))
            else:
                return choice((1,3))
        else :
            return WalkTo(x_r,y_r,x_d,y_d,)
    elif typ=='d': #defence
        #if help condition either alter this or signal[0]
        if abs(x_r-x_h)+abs(y_r-y_h)<max(2,4*id-2*baes.count('h')):        
            return randmoves(robot)
        else:
            return WalkTo(x_r,y_r,x_h,y_h,0)

def ActRobot(robot):
    typ=robot.GetInitialSignal()[0]
    id=int(robot.GetInitialSignal()[1:])
    phase=robot.GetCurrentBaseSignal()[0]
    #investigation
    VirusPolicy(robot,typ)
    
    #movement    
    if phase=='~':
        return FirstPhaseM(robot,typ,id)
    elif phase=='!':
        return SecondPhaseM(robot,typ,id) 
    elif phase=='b':
        return EndPhase(robot,typ,id) #e boys
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
        j=0
        k=0
        
        while base.GetElixir() > 1200: #1200 tha
            base.create_robot('a'+str(j))  # search directly
            j+=1
        while base.GetElixir() > 900: #900 tha
            base.create_robot('m'+str(i))
        while base.GetElixir() > 500: #500 tha
            base.create_robot('d'+str(k))  # defence capability ->more conservative with movement
            k+=1
            
    All=base.GetListOfSignals()
    for L in All:
        if len(L)>0:
            if L[0]=='b':
                base.SetYourSignal(L[:5]+base.GetYourSignal()[5:]) #checkforerrors
                break
            elif L[0]=='!':
                base.SetYourSignal('!'+base.GetYourSignal()[1:])
                #base.create_robot('f0')
                

    def enemies_near(): #??
        return (base.investigate_up()=='enemy')+(base.investigate_down()=='enemy')+(base.investigate_left()=='enemy')+(base.investigate_right()=='enemy')+(base.investigate_ne()=='enemy')+(base.investigate_nw()=='enemy')+(base.investigate_se()=='enemy')+(base.investigate_sw()=='enemy')
    if enemies_near():
        base.DeployVirus(800) #100 per block
        base.SetYourSignal(base.GetYourSignal()+'h'*(enemies_near()))

    ##put more logic in the base defense/attack mechn!!
    return
