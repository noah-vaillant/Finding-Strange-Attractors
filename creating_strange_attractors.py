#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:06:03 2024

@author: noahvaillant
"""
# =============================================================================
# This code uses methodology decribed in Automatic Generation of Strange Attractors
# By J. C. Sprott to randomly create strange attractors using a simple formula
# =============================================================================


import random as r
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mat

#Formula for n + 1
def nplus1(x: float, y: float, a: list[float], b: list[float]) -> (float, float):
    '''
    This simple formula takes random coefficents and an input x,y to spit out
    the next iteration of x,y
    
    Parameters
    ----------
    x - Input x value (x_n)
    y - Input y value (y_n)
    a - Randomly generated coefficents between -1.2 and 1.2
    b - Randomly generated coefficents between -1.2 and 1.2

    Returns
    -------
    x_n+1, y_n+1 - outputted x and y values

    '''
    return (a[0] + a[1]*x*y + a[2]*x**2 + a[3]*y + a[4]*y**2 +a[5]*x, 
            b[0] + b[1]*x*y +b[2]*x**2 + b[3]*y +b[4]*y**2 + b[5]*x)

def lya(x0, y0, w0, z0, x1, y1, w1, z1) -> float:
    '''
    This formula uses the lyapunov exponent formula of ln(d_n+1/d_n) for the d
    values as distances between points that started from simular initial conditons
    
    
    Parameters
    ----------
    x0, y0 - x-n, y_n
    w0, z0 - nth iterations of w,z which started nearby x,y
    x1, y1 - x_n+1, y_n+1
    w0, z0 - w_n+1, z_n+1

    Returns
    -------
    Lyapunov exponent around x_n, y_n
    '''
    return np.log(np.sqrt((((x0-w0)**2+(y0-z0)**2) + 10**-9)/((x1-w1)**2+ (y1-z1)**2 + 10**-9)))
    

#Coefficent range for a,b 
min = -12
max = 12


n = 70000

for j in range(10000):
   
    
    # Initial conditions, adding a very close togther point to check lyapunov exponent
    x = 0.05
    y = 0.05
    w = 10**-6 + x
    z = y

    xns = []
    yns = []
    wns = []
    zns = []
    
    # Random coeffiencents
    
    a = [0,0,0,0,0,0]
    b = [0,0,0,0,0,0]
    
    for num in range(6):
        a[num] = 0.1 * (int(25 * r.random()) - 12)
        b[num] = 0.1 * (int(25 * r.random()) - 12)
    
    lya_check = False
    

    for i in range(n):
            
        xns.append(x)
        yns.append(y)
        wns.append(w)
        zns.append(z)
        
        # Check Divergence
        if abs(x) > 10**10 or abs(y) > 10**10:
            break
        
        # Check repition using lya exponent
        if i > 2000 and not(lya_check):
            l = sum(lya(xns[d], yns[d], wns[d], zns[d], xns[d-1], yns[d-1], wns[d-1], zns[d-1]) for d in range(0, i))
            avg_l = l / (i - 1)
            if avg_l < 0:
                break
            lya_check = True
           
        # Check Divergence for w,z and not carrying on with them if they do
        # If w,z diverge but x,y dont keep going
        if abs(w) > 10**6 and abs(z) > 10**6:
            if i < 100 and (abs(x) > 10**6 or abs(y) > 10**6):
                break
            else:
                lya_check = False
        else:
            w, z  = nplus1(w,z,a,b)
          
        # Next iteration
        x, y  = nplus1(x,y,a,b)
        i = i + 1
    # Going through all n iteratons wihtout tripping means that a strange 
    # Attractor has been found    
    if len (xns) == n:
        break
   
    

print ('a =', a)
print ('b = ', b)

#Pyplot code
mat.rcParams['agg.path.chunksize'] = 100000

plt.title('Strange Attractor')
plt.plot(xns[int(len(xns)//5):], yns[int(len(yns)//5):], 'r:', alpha=0.6, lw=0.01 )
plt.axis('off')
plt.savefig('strange_attractor.png', dpi=300, bbox_inches='tight')
# plt.show()

plt.title('Strange Attractor')
plt.scatter(xns[int(len(xns)//5)::], yns[int(len(yns)//5)::], c='red', alpha=0.6, s=0.01)
plt.axis('off')
plt.savefig('strange_attractor.png', dpi=300, bbox_inches='tight')
# plt.show()

#Interesting a,b values

#Splits into Four
# a = [-0.8, 0.6000000000000001, 0.5, 0.7000000000000001, 1.1, 0.8]
# b =  [-0.7000000000000001, 0.5, 0.8, 0.1, 0.5, -0.4]

#Triangle
#a = [0.1, 0.8, -1.0, 0.9, -0.30000000000000004, -0.4]
#b =  [-0.5, 0.7000000000000001, -0.2, -0.9, 0.8, -0.8]

# Three Leaves 
# a = [-0.9, -0.30000000000000004, 0.1, 1.1, -0.2, 0.0]
# b =  [-0.2, 1.1, 1.1, -0.5, 0.6000000000000001, 0.30000000000000004]

# Two Closed Rings
# a = [0.6000000000000001, 0.9, -1.2000000000000002, -0.4, -0.6000000000000001, -0.7000000000000001]
# b =  [0.2, 1.2000000000000002, 0.0, -1.0, 0.8, -0.5]

# Big Stupid Oval
# a = [-0.6000000000000001, -0.1, 0.8, 0.2, 0.7000000000000001, 1.2000000000000002]
# b =  [1.1, 0.5, -1.1, 0.7000000000000001, -1.1, -0.9]



