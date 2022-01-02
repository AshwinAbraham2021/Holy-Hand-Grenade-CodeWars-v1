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

def Refuel(robot, robsig , id):
    # will need base coordinates base_x,base_y and robot coordinates bot_x, bot_y
    base_x=int(robsig[:2])
    base_y=int(robsig[2:4])
    bot_x,bot_y=robot.GetPosition()
    elixir = robot.GetElixir()
    elixirmin = 60
    elixirmax = 150
    #elixir < elixirmin or elixir < elixirmax
    if elixir < elixirmin:	
        if (id%4 == 0): # Moving southeasterly
            return choice((2,3))
        elif (id%4 == 1): # Moving southwesterly
            return choice((3,4))
        elif (id%4 == 2): # Moving northwesterly
            return choice((1,4))
        else: # Moving northeasterly
            return choice((1,2))
    else:
        if abs(base_x - bot_x) + abs(base_y - bot_y) < 8:
            return(randint(1, 4))
        else:
            return WalkTo(base_x,base_y,bot_x,bot_y,0)

def Defence(robot,id):
    robsig=robot.GetYourSignal()
    basesig=robot.GetCurrentBaseSignal()
    if robsig=='': 
        robsig= basesig[3:7]
        robot.setSignal(robsig)
    if ('H' in basesig):
        x_r,y_r=robot.GetPosition()
        return WalkTo(x_r,y_r,int(robsig[:2]),int(robsig[2:4]),1)
    else:
        return Refuel(robot,robsig,id)
    #if abs(x_r-x_h)+abs(y_r-y_h)<max(2,4*id-2*baes.count('h')):        
        #return randmoves(robot)
    #else:
        #return WalkTo(x_r,y_r,x_h,y_h,0)


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
        
            
            

    
def FirstPhaseM(robot,robsig,id): #~
    x_r,y_r=robot.GetPosition()
    baes=robot.GetCurrentBaseSignal()
    
    if len(robsig)==1:
        x_h=int(baes[3:5]) #home
        y_h=int(baes[5:7])
        X=robot.GetDimensionX()
        Y=robot.GetDimensionY()
        if robsig[0]=='0': robsig+=CoordStr(X-x_h-1,Y-y_h-1)
        elif robsig[0]=='1': robsig+=CoordStr(X-x_h-1,y_h)
        elif robsig[0]=='2': robsig+=CoordStr(x_h,Y-y_h-1)
    
    x_d=int(robsig[1:3])
    y_d=int(robsig[3:5])
    
    if robot.investigate_up()=='enemy-base': #rem--chk 
        robsig='b'+CoordStr(x_r,y_r-1)   
    elif robot.investigate_down()=='enemy-base':
        robsig='b'+CoordStr(x_r,y_r+1)       
    elif robot.investigate_left()=='enemy-base':
        robsig='b'+CoordStr(x_r-1,y_r)
    elif robot.investigate_right()=='enemy-base':
        robsig='b'+CoordStr(x_r+1,y_r) 
    elif robot.investigate_ne()=='enemy-base':
        robsig='b'+CoordStr(x_r+1,y_r-1)
    elif robot.investigate_nw()=='enemy-base':
        robsig='b'+CoordStr(x_r-1,y_r-1)
    elif robot.investigate_se()=='enemy-base':
        robsig='b'+CoordStr(x_r+1,y_r+1)
    elif robot.investigate_sw()=='enemy-base':
        robsig='b'+CoordStr(x_r-1,y_r+1)
    #el and robot.GetYourSignal=='': #reached near destination but do not see base yet
        #counter updated if no base
    else:
        try:
            ind=robsig.index('t')+1
            time=int(robsig[ind])            
            if time>3:
                robsig+='!'
            else :
                robsig=robsig[:ind]+str((time+1)%5)+robsig[ind+1:]
                #print (robsig)
        except ValueError:
            if abs(x_d-x_r)+abs(y_d-y_r)<2:
                robsig+='t0'
                #print(robsig)
    #the movement defining code
    robot.setSignal(robsig)
    return WalkTo(x_r,y_r,x_d,y_d,1)


def SecondPhaseM(robot,robsig,id): #!
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
    #print(robsig +'\t'+ baes)
    try:
        if id%2==0:
            robsig=str(baes.index('~'))
        else:
            robsig=str(baes.rindex('~'))
    except: robsig='0'

    robot.setSignal(robsig)  
    return randint
    

def EndPhase(robot,typ,id):
    x_r,y_r=robot.GetPosition()
    baes=robot.GetCurrentBaseSignal()  
    x_d=int(baes[1:3]) #destination
    y_d=int(baes[3:5])
    

    if typ=='a':
        if abs(x_r-x_d)+abs(y_r-y_d)==1:
            if robot.GetVirus()>robot.GetElixir():
                if x_r==x_d:
                    return choice((2,4))
                else:
                    return choice((1,3))
            else:
                if x_r>x_d : return 4
                elif x_r<x_d : return 2
                else: 
                    if y_r>y_d : return 1
                    else: return 3
        else :
            return WalkTo(x_r,y_r,x_d,y_d,0)
    elif typ=='m':
        if robot.GetElixir()>100:
            if abs(x_r-x_d)+abs(y_r-y_d)==1:
                if x_r==x_d:
                    return choice((2,4))
                else:
                    return choice((1,3))
            else :
                return WalkTo(x_r,y_r,x_d,y_d,0)
        else:
            return randmoves(robot)


def ActRobot(robot):
    #return 0
    typ=robot.GetInitialSignal()[0]
    id=int(robot.GetInitialSignal()[1:])
    basesig=robot.GetCurrentBaseSignal()
    #investigation
    VirusPolicy(robot,typ)
    
    #movement    
    if typ=='d':
        return Defence(robot,id)
    elif basesig[0]=='b':
        return EndPhase(robot,typ,id) 
    elif basesig[:3]=='!!!': return randmoves(robot)
    elif typ=='a':
        robsig=robot.GetYourSignal()
        if robsig=='':robsig=str(id%3)
        if robsig[0]=='b': return randint(1,4)
        elif basesig[int(robsig[0])]=='~': return FirstPhaseM(robot,robsig,id)
        elif basesig[int(robsig[0])]=='!': return SecondPhaseM(robot,robsig,id)
    else:
        x_r,y_r=robot.GetPosition()
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
        else:  return randint(1,4)


def ActBase(base):
    ##initialisation step
    if base.GetYourSignal()=='':
        No_of_bots=(base.GetElixir()-500)//50
        x_b,y_b=base.GetPosition()
        base.SetYourSignal('~'*3+CoordStr(x_b,y_b))#optimise later
        #botcreation
        #i=0
        #j=0
        k=0        
        #while base.GetElixir() > 1200: #1200 tha
        #    base.create_robot('a'+str(i))  # search directly
        #    i+=1
        for i in range(No_of_bots//2):
            base.create_robot('a'+str(i))

        #while base.GetElixir() > 900: #900 tha
            #base.create_robot('m'+str(j))
        for j in range(No_of_bots//4):
            base.create_robot('m'+str(j))

        while base.GetElixir() > 500: #500 tha
            base.create_robot('d'+str(k))  # defence capability ->more conservative with movement
            k+=1
        
    basesig=base.GetYourSignal()        
    All=base.GetListOfSignals()
    #print(len(All),basesig)
    
    for L in All:
        if len(L)>0 and not(basesig[0]=='b'):
            if L[0]=='b':
                #print(basesig)
                base.SetYourSignal(L[:5]+basesig[7:]) #checkforerrors
                break
            elif L[-1]=='!':
                base.SetYourSignal(basesig[:int(L[0])]+'!'+basesig[int(L[0])+1:])
                #base.create_robot('f0')           

    enemies_near= (base.investigate_up()=='enemy')+(base.investigate_down()=='enemy')+(base.investigate_left()=='enemy')+(base.investigate_right()=='enemy')+(base.investigate_ne()=='enemy')+(base.investigate_nw()=='enemy')+(base.investigate_se()=='enemy')+(base.investigate_sw()=='enemy')
    
    if enemies_near:
        base.DeployVirus(1200) #100 per block
        if 'H' in basesig:
            ind=basesig.index('H')+1
            base.SetYourSignal(basesig[:ind]+str(max(9,2*enemies_near))+basesig[ind+1:])
        else:
            base.SetYourSignal(basesig+'H'+str(max(9,2*enemies_near)))
    else:
        if 'H0' in basesig:
            ind=basesig.index('H')
            base.SetYourSignal(basesig[:ind]+basesig[ind+2:])
        elif 'H' in basesig:
            ind=basesig.index('H')+1
            base.SetYourSignal(basesig[:ind]+str(int(basesig[ind])-1)+basesig[ind+1:])
        

    ##put more logic in the base defense/attack mechn!!
    return
