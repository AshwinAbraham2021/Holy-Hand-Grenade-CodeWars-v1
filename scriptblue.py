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
        if numen>2 and robot.GetVirus()>1000:
            robot.DeployVirus(800)	#alter the values
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
    elif abs(x_d-x_r)+abs(y_d-y_r)<=2 and robot.GetYourSignal=='': #reached near destination but do not see base yet
        robot.setSignal('0')#counter updated if no base
    else:
        try:
            if int(robot.GetYourSignal())==8:
                robot.setSignal('!'+robot.GetYourSignal())
            else :
                robot.setSignal(str(int(robot.GetYourSignal())+1))
        except ValueError:
            pass   
    #the movement defining code
   
    x_h=int(baes[6:8]) #home
    y_h=int(baes[8:10])
    

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
    
    elif typ=='d': #defence
        #if help condition either alter this or signal[0]
        if abs(x_r-x_h)+abs(y_r-y_h)<=max(2,3*id-2*baes.count('h')):        
            return randint(1,4)
        else:
            if x_r<x_h:
                pstring+='2'*(x_h-x_r)
            else:
                pstring+='4'*(x_r-x_h)
            if y_r>y_h:
                pstring+='1'*(y_r-y_h)
            else:
                pstring+='3'*(y_h-y_r)
            return int(choice(pstring))

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
    
    pstring='1234'
    if typ=='a': #direct scouts
        
        return int(choice(pstring))
    
    elif typ=='d': #defence
        #if help condition either alter this or signal[0]
        if abs(x_r-x_h)+abs(y_r-y_h)<=max(2,3*id-2*baes.count('h')):        
            return randint(1,4)
        else:
            if x_r<x_h:
                pstring+='2'*(x_h-x_r)
            else:
                pstring+='4'*(x_r-x_h)
            if y_r>y_h:
                pstring+='1'*(y_r-y_h)
            else:
                pstring+='3'*(y_h-y_r)
            return int(choice(pstring))

def EndPhase(robot,typ):
    x_r,y_r=robot.GetPosition()
    baes=robot.GetCurrentBaseSignal()  
    x_d=int(baes[1:3]) #destination
    y_d=int(baes[3:5])
    x_h=int(baes[6:8]) #home
    y_h=int(baes[8:10])
    pstring=''

    if typ=='a'or typ=='m':
        if abs(x_r-x_d)+abs(y_r-y_d)==1:
            if x_r==x_d:
                return choice((2,4))
            else:
                return choice((1,3))
        else :
            if x_r<x_d:
                pstring+='2'*(x_d-x_r)
            else:
                pstring+='4'*(x_r-x_d)
            if y_r>y_d:
                pstring+='1'*(y_r-y_d)
            else:
                pstring+='3'*(y_d-y_r)
            return int(choice(pstring))
    elif typ=='d': #defence
        #if help condition either alter this or signal[0]
        if abs(x_r-x_h)+abs(y_r-y_h)<10-2*baes.count('h'):        
            return randint(1,4)
        else:
            pstring+='1234'
            if x_r<x_h:
                pstring+='2'*(x_h-x_r)
            else:
                pstring+='4'*(x_r-x_h)
            if y_r>y_h:
                pstring+='1'*(y_r-y_h)
            else:
                pstring+='3'*(y_h-y_r)
            return int(choice(pstring))

def ActRobot(robot):
    typ=robot.GetInitialSignal()[0]
    id=int(robot.GetInitialSignal()[1:])
    #investigation
    VirusPolicy(robot,typ)
    
    #movement    
    if robot.GetCurrentBaseSignal()[0]=='~':
        return FirstPhaseM(robot,typ,id)
    if robot.GetCurrentBaseSignal()[0]=='!':
        return SecondPhaseM(robot,typ,id) 
    elif robot.GetCurrentBaseSignal()[0]=='b':
        return EndPhase(robot,typ) #e boys
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
        
        j=0
        k=0
        
        while base.GetElixir() > 1200:
            base.create_robot('a'+str(j))  # search directly
            j+=1
        while base.GetElixir() > 500:
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

    def enemies_near(): #??
        return (base.investigate_up()=='enemy')+(base.investigate_down()=='enemy')+(base.investigate_left()=='enemy')+(base.investigate_right()=='enemy')+(base.investigate_ne()=='enemy')+(base.investigate_nw()=='enemy')+(base.investigate_se()=='enemy')+(base.investigate_sw()=='enemy')
    if enemies_near():
        base.DeployVirus(800) #100 per block
        base.SetYourSignal(base.GetYourSignal()+'h'*(enemies_near()))

    ##put more logic in the base defense/attack mechn!!
    return
