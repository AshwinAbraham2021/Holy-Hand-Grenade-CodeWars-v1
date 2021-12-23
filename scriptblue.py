from random import randint
def CoordStr(x,y): #assumes x,y<100
    if x<10:
        xs='0'+str(x)
    else:
        xs=str(x)
    if y<10:
        ys='0'+str(y)
    else:
        ys=str(y)
    return xs+ys

def ActRobot(robot):

    ## if base is found, return as b + x_be +| y_be + .
        if robot.GetVirus() > 1000:
                robot.DeployVirus(200)
        
        return randint(1,4)


def ActBase(base):

    if base.GetYourSignal()=='':
        x_b,y_b=base.GetPosition()
        x_est=base.GetDimensionX()-x_b  # A good guess for expected location of opponent base
        y_est=base.GetDimensionX()-y_b  # Could help with finding enemy base quickly
        base.SetYourSignal('~'+CoordStr(x_est,y_est))#optimise later

    #count of classes???

    bel = base.GetElixir()
    while bel > 600:
        if bel > 1500:
            base.create_robot('m')  # mixed capability ->depends
        elif bel > 1000:
            base.create_robot('a')  # attack capability ->more freedom of movement and attack
        else:
            base.create_robot('d')  # defence capability ->more conservative with movement

    All=base.GetListOfSignals()
    for L in All:
        if L[0]=='b':
            base.SetYourSignal(L[:5]+base.GetYourSignal()[5:]) #checkforerrors

    enemies_near=(base.investigate_up()=='enemy')or(base.investigate_down()=='enemy')or(base.investigate_left()=='enemy')or(base.investigate_right()=='enemy')or(base.investigate_ne()=='enemy')or(base.investigate_nw()=='enemy')or(base.investigate_se()=='enemy')or(base.investigate_sw()=='enemy')
    if enemies_near:
        base.DeployVirus(500)
        base.SetYourSignal(base.GetYourSignal()+'h')

    ##add the defense/attack mechn!!
    return
