#/usr/bin/env python
'''
    Mutually Inhibitory Toggle Switch with protein burst.
    X ---| Y; Y ---| X
    DEs for the toggle switch system:


    The equivalent chemical system: 
    R1:  
    R2: 
    R3:  
    R4: 
    
    System variables: X, Y, Px, and Py
    Dummy variable: phi
    System parameters: gX, gY, kX, kY 
'''
import sys
import random
from collections import OrderedDict
import auxiliary_functions as aux

#-----------------------------------------------------------------------------#
def defineSystem():
    '''
    Create variables to store the parameters and status of the system. 
    '''
    #set parameters:
    pars = OrderedDict() 
    pars = aux.parameter_burst_1()
    #set initial conditions for the system variables: 
    vars=OrderedDict()
    vars['X'] = 100 
    #vars['X'] = 0 
    vars['Y'] = 100
    #vars['Y'] = 0

    vars['Px'] = 0 
    vars['Py'] = 1
    #set simulation time: 
    tmax=1.0e+6
    return (pars,vars,tmax)

#-----------------------------------------------------------------------------#
def calculate_propensities(pars, vars):
    '''
    This method calculates the propensitites for all reactions happening at the 
    current state. Each subsystem can be in two states: promoter is ON or OFF. 
    The status of the promoter of two subsystems are stored in variables Px and
    Py, respectively.
    Therefore, the whole system of the two subsystems can be at any of FOUR 
    states:
    Px  Py 
    ON  ON 
    ON  OFF 
    OFF ON 
    OFF OFF  
    Here, the propensitites of the two subsystems at any of the FOUR states are 
    calculated.
    '''
    #availalbe reactions (initially make all six of them available):
    availableReactions = [1]*6
    #propensities are stored in pros:
    pros = list()

    if (vars.get('Px') and vars.get('Py')):
        #reactions of X system: promoter P is ON
        #R1:
        pros.append(pars.get('KoffX'))
        #R2:
        pros.append(pars.get('gXon'))
        #R3:
        pros.append(pars.get('kX')*vars.get('X'))

        #reactions of Y system: promoter P is ON
        #R1:
        pros.append(pars.get('KoffY'))
        #R2:
        pros.append(pars.get('gYon'))
        #R3:
        pros.append(pars.get('kY')*vars.get('Y'))
    elif (vars.get('Px') and not vars.get('Py')):
        #reactions of X system: promoter P is ON
        #R1:
        pros.append(pars.get('KoffX'))
        #R2:
        pros.append(pars.get('gXon'))
        #R3:
        pros.append(pars.get('kX')*vars.get('X'))

        #reactions Y system: promoter P is OFF
        #R1:
        if (vars.get('X')>=pars.get('nX')):
            pros.append(pars.get('KonY')*(vars.get('X')**pars.get('nX')))
        else: 
            pros.append(0.0)
            availableReactions[3]=0
        #R2:
        pros.append(pars.get('gYoff'))
        #R3:
        pros.append(pars.get('kY')*vars.get('Y'))

    elif (not vars.get('Px') and vars.get('Py')):
        #reactions of X system: promoter P is OFF
        #R1:
        if (vars.get('Y')>=pars.get('nY')): #R1 IS Available
            pros.append(pars.get('KonX')*(vars.get('Y')**pars.get('nY')))
        else: #R1 is NOT Available
            pros.append(0.0)
            availableReactions[0]=0
        #R2:
        pros.append(pars.get('gXoff'))
        #R3:
        pros.append(pars.get('kX')*vars.get('X'))

        #reactions of Y system: promoter P is ON
        #R1:
        pros.append(pars.get('KoffY'))
        #R2:
        pros.append(pars.get('gYon'))
        #R3:
        pros.append(pars.get('kY')*vars.get('Y'))

    elif (not vars.get('Px') and not vars.get('Py')):
        #reactions of X system: promoter P is OFF
        #R1:
        if (vars.get('Y')>=pars.get('nY')):
            pros.append(pars.get('KonX')*(vars.get('Y')**pars.get('nY')))
        else: #R1 is not Available
            pros.append(0.0)
            availableReactions[0]=0
        #R2:
        pros.append(pars.get('gXoff'))
        #R3:
        pros.append(pars.get('kX')*vars.get('X'))

        #reactions of Y system: promoter P is OFF
        #R1:
        if (vars.get('X')>=pars.get('nX')):
            pros.append(pars.get('KonY')*(vars.get('X')**pars.get('nX')))
        else:
            pros.append(0.0)
            availableReactions[3]=0
        #R2:
        pros.append(pars.get('gYoff'))
        #R3:
        pros.append(pars.get('kY')*vars.get('Y'))

    return (availableReactions, pros)

#-----------------------------------------------------------------------------#
def updateSystem_xPon_yPon(pars, vars, pros):
    '''
    This method updates the system when both X and Y promoters are ON.
    '''
    #probability of each reaction: 
    ptotal = sum(pros)
    pr=[x/ptotal for x in pros]
    #cumulative probabilities: 
    prAc=[]
    for k in range(len(pr)):
        if not k:
            prAc.append(pr[k])
            continue
        prAc.append(prAc[k-1]+pr[k])
    
    #update system by randomly selecting a reaction:    
    rn=random.uniform(0,1)
    #(options 0 to 2 for X system, 3 to 5 for Y system)
    if rn<prAc[0]:
        vars['Y']+=pars['nY']
        vars['Px']=0 #X promoter switches to OFF state
    elif rn<prAc[1]:
        vars['X']+=1
    elif rn<prAc[2]: 
        vars['X']-=1
    elif rn<prAc[3]: 
        vars['X']+=pars['nX']
        vars['Py']=0 #Y promoter switches to OFF state
    elif rn<prAc[4]:
        vars['Y']+=1
    else:
        vars['Y']-=1

    return (ptotal, vars)

#-----------------------------------------------------------------------------#
def updateSystem_xPon_yPoff(pars, vars, pros):
    '''
    This method updates the system when X promoter is ON and Y promoter is OFF.
    '''
    #probability of each reaction:
    ptotal = sum(pros)
    pr=[x/ptotal for x in pros]
    #cumulative probabilities:
    prAc=[]
    for k in range(len(pr)):
        if not k:
            prAc.append(pr[k])
            continue
        prAc.append(prAc[k-1]+pr[k])

    #update system by randomly selecting a reaction:    
    rn=random.uniform(0,1)
    #(options 0 to 2 for X system, 3 to 5 for Y system)
    if rn<prAc[0]:
        vars['Y']+=pars['nY']
        vars['Px']=0 #X promoter switches to OFF state
    elif rn<prAc[1]:
        vars['X']+=1
    elif rn<prAc[2]:
        vars['X']-=1
    elif rn<prAc[3]: # and vars.get('X')>=pars.get('nX'):
        #Critical Point 1
        vars['X']-=pars['nX']
        vars['Py']=1 #Y promoter switches to ON state
    elif rn<prAc[4]:
        vars['Y']+=1
    else:
        vars['Y']-=1

    return (ptotal, vars)

#-----------------------------------------------------------------------------#
def updateSystem_xPoff_yPon(pars, vars, pros):
    '''
    This method updates the system when X promoter is OFF and Y promoter is ON.
    '''
    
    #probability of each reaction: 
    ptotal = sum(pros)
    pr=[x/ptotal for x in pros]
    #cumulative probabilities:
    prAc=[]
    for k in range(len(pr)):
        if not k:
            prAc.append(pr[k])
            continue
        prAc.append(prAc[k-1]+pr[k])

    #update system by randomly selecting a reaction:    
    rn=random.uniform(0,1)
    #(options 0 to 2 for X system, 3 to 5 for Y system)

    if rn<prAc[0]: #and vars.get('Y')>=pars.get('nY'):
        #Critical Point 2
        vars['Y']-=pars['nY']
        vars['Px']=1 # X promoter switches to ON state
    elif rn <prAc[1]:   
        vars['X']+=1
    elif rn <prAc[2]:   
        vars['X']-=1
    elif rn<prAc[3]: 
        vars['X']+=pars['nX']
        vars['Py']=0 #Y promoter switches to OFF state
    elif rn<prAc[4]: 
        vars['Y']+=1
    else:   
        vars['Y']-=1

    return (ptotal, vars)

#-----------------------------------------------------------------------------#
def updateSystem_xPoff_yPoff(pars, vars, pros):
    '''
    This method updates the system when both X and Y promoters are OFF.
    '''
    #probability of each reaction: 
    ptotal = sum(pros)
    pr=[x/ptotal for x in pros]
    #cumulative probabilities: 
    prAc=[]
    for k in range(len(pr)):
        if not k:
            prAc.append(pr[k])
            continue
        prAc.append(prAc[k-1]+pr[k])

    #update system by randomly selecting a reaction:    
    rn=random.uniform(0,1)
    #(options 0 to 2 for X system, 3 to 5 for Y system)
    if rn<prAc[0]: #and vars.get('Y')>=pars.get('nY'):
        #Critical Point 3 => Critical Point 2
        vars['Y']-=pars['nY']
        vars['Px']=1 #X promoter switches to ON state
    elif rn <prAc[1]:
        vars['X']+=1
    elif rn <prAc[2]:
        vars['X']-=1
    elif rn<prAc[3]: # and vars.get('X')>=pars.get('nX'): 
        #Critical Point 4 => Critical Point 1
        vars['X']-=pars['nX']
        vars['Py']=1 #Y promoter switches to ON state
    elif rn<prAc[4]:
        vars['Y']+=1
    else:
        vars['Y']-=1

    return (ptotal, vars)

#-----------------------------------------------------------------------------#
def updateSystem(pars, vars):
    '''
    This method updates the system variables by performing specific 
    reaction(s) at each time step.
    '''
    #calculate propensities:
    (availableReactions,pros) = calculate_propensities(pars, vars)

    if vars.get('Px') and vars.get('Py'): #both promoters ON
        (ptotal,vars) = updateSystem_xPon_yPon(pars, vars, pros)
    elif vars.get('Px') and not vars.get('Py'): #X promoter ON, Y promoter OFF
        (ptotal,vars) = updateSystem_xPon_yPoff(pars, vars, pros)
    elif not vars.get('Px') and vars.get('Py'): #X promoter OFF, Y promoter ON
        (ptotal,vars) = updateSystem_xPoff_yPon(pars, vars, pros)
    else: #elif not vars.get('Px') and not vars.get('Py'): #both promoters OFF
        (ptotal,vars) = updateSystem_xPoff_yPoff(pars, vars, pros)

    return (ptotal,vars)

#-----------------------------------------------------------------------------#
def run_simulation(pars, vars, tmax):
    '''
    This method repeatedly performs the following tasks: 
    (1) Calculates propensities for each reaction as a function of the current
        state of the system.
    (2) Stochastically selects the next reaction to occur and update the 
        system after the reaction is performed.
    (3) Stochastically chooses the wait time (dt) for the next reaction to 
        occur.
    '''
    import numpy as np

    #initialize current time:
    tc=0
    #iteration counter:
    factor=1000
    count = 0
    print('tc', '\t', 'X', '\t', 'Y', '\t', 'Px', '\t', 'Py')
    while(tc<tmax):
        #save configuration at multiple of 'factor' timesteps:
        if (not (count%factor)):
            print(tc, '\t', vars.get('X'), '\t', vars.get('Y'), 
                      '\t', vars.get('Px'), '\t', vars.get('Py'))
        #print(tc, '\t', vars.get('X'), '\t', vars.get('Y'), 
        #          '\t', vars.get('Px'), '\t', vars.get('Py'))

        #perform specific reaction based on propensity values:
        (ptotal, vars) = updateSystem(pars, vars)

        if(vars.get('X')<0 or vars.get('Y')<0):
            print('system variable X or Y is below 0')
            print(tc, '\t', vars.get('X'), '\t', vars.get('Y'), 
                      '\t', vars.get('Px'), '\t', vars.get('Py'))
            return None
 
        if(not ptotal):
            print('ptotal became zero')
            sys.exit(0) 
        #obtain wait time dt from exponential distribution:
        lambd=ptotal # lambd = 1/mean where mean = 1/ptotal
        dt=random.expovariate(lambd)
        tc+=dt
        count+=1
    #print(count)
    return None

#-----------------------------------------------------------------------------#
if __name__=="__main__":
    import time
    (pars,vars,tmax)=defineSystem()
    t_start=time.time()
    run_simulation(pars,vars,tmax)
    t_end=time.time()
    print('simulation time: ',t_end-t_start)
    sys.exit(0)
