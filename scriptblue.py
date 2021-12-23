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

#def ()
def ActRobot(robot):

    ## if base is found, return as b + Coordstr .
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


    if base.GetElixir()> 600:
        while base.GetElixir() > 1500:
            base.create_robot('m')  # mixed capability ->depends
        while base.GetElixir() > 1000:
            base.create_robot('a')  # attack capability ->more freedom of movement and attack
        while base.GetElixir() > 600:
            base.create_robot('d')  # defence capability ->more conservative with movement

    All=base.GetListOfSignals()
    for L in All:
        if len(L)>0 and L[0]=='b':
            base.SetYourSignal(L[:5]+base.GetYourSignal()[5:]) #checkforerrors

    def enemies_near():
        return (base.investigate_up()=='enemy')+(base.investigate_down()=='enemy')+(base.investigate_left()=='enemy')+(base.investigate_right()=='enemy')+(base.investigate_ne()=='enemy')+(base.investigate_nw()=='enemy')+(base.investigate_se()=='enemy')+(base.investigate_sw()=='enemy')
    if enemies_near():
        base.DeployVirus(800)
        base.SetYourSignal(base.GetYourSignal()+'h'+str(enemies_near))

    ##add the defense/attack mechn!!
    return
