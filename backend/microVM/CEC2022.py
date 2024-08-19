# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 16:49:21 2022

@author: Abhishek Kumar
@email: abhishek.kumar.eee13@iitbhu.ac.in
"""
import numpy as np

INF = 1.0e99
EPS = 1.0e-14
E  = 2.7182818284590452353602874713526625
PI = 3.1415926535897932384626433832795029

class FuncCallsLimitReachedException(Exception):
    def __init__(self, message="Budget exhausted - limit of objective function calls reached."):
        self.message = message
        super().__init__(self.message)


class CECfunctions:
  def __init__(self) -> None:
    self.call_count = 0
    self.max_call_count = 200000
    self.function_to_call = 1
    self.nx = 10 # problem dimension
    self.mx = 50 # population size
    self.functions_dict = {
      1: 'zakharov_func',
      2: 'rosenbrock_func',
      3: 'schaffer_F7_func',
      4: 'step_rastrigin_func',
      5: 'levy_func',
      6: 'hf02',
      7: 'hf10',
      8: 'hf06',
      9: 'cf01',
      10: 'cf02',
      11: 'cf06',
      12: 'cf07'
    }
    self.fun_mins = [300, 400, 600, 800, 900, 1800, 2000, 2200, 2300, 2400, 2600, 2700]

    self.s_flag = 1
    self.r_flag = 1
    self.OShift = None 
    self.M = None 
    self.y = None
    self.z = None 
    self.x_bound = None 
    self.ini_flag = 0
    self.n_flag = None 
    self.func_flag = None
    self.SS = None
    self.cf_num = 10

  def set_function_to_call(self, fun):
    self.function_to_call = fun
  
  def reset_call_count(self):
    self.call_count = 0
  
  def set_problem_dim(self, nx):
    self.nx = nx
  
  def set_pop_size(self, mx):
    self.mx = mx
  
  def set_max_fes(self, max_fes):
    self.max_call_count = max_fes
  
  def get_function_min(self, fun_num):
    return self.fun_mins[fun_num-1]

  def get_calls_count(self):
    return self.call_count

  # @staticmethod
  def count_calls(func):
    def wrapper(self, *args, **kwargs):
        # print(f"Function {func.__name__} has been called {self.call_count} times.")
        if func.__name__ == self.functions_dict[self.function_to_call]:
          self.call_count += 1
          if self.call_count > self.max_call_count:
              raise FuncCallsLimitReachedException
        return func(self, *args, **kwargs)
    return wrapper

  def ellips_func(self, x, nx, Os, Mr, s_flag, r_flag):
    f = 0.0
    z = self.sr_func(x, nx, Os, Mr, 1.0, s_flag, r_flag)
    for i in range(nx):
      f += pow(10.0, 6.0*i/(nx-1))*z[i]*z[i]
    return f

  def bent_cigar_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    z = self.sr_func(x, nx, Os, Mr, 1.0, s_flag, r_flag)
    f = z[0]*z[0]
    for i in range(1, nx):
      f += pow(10.0, 6.0)*z[i]*z[i]
    return f

  def discus_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    z = self.sr_func(x, nx, Os, Mr, 1.0, s_flag, r_flag)
    f = pow(10.0,6.0)*z[0]*z[0]
    for i in range(1, nx):
      f += z[i]*z[i]
    return f

  @count_calls
  def rosenbrock_func(self, x, nx, Os, Mr, s_flag, r_flag):

    f = 0.0
    z = self.sr_func(x, nx, Os, Mr, 2.048/100.0, s_flag, r_flag)
    z[0] += 1.0
    for i in range(nx-1):
      z[i+1] += 1.0
      tmp1 = z[i]*z[i] - z[i+1]
      tmp2 = z[i] - 1.0
      f += 100.0*tmp1*tmp1 + tmp2*tmp2
    return f

  def ackley_func(self, x,  nx, Os, Mr, s_flag, r_flag):
    
    sum1, sum2 = 0, 0
    z = self.sr_func(x,  nx, Os, Mr, 1.0, s_flag, r_flag)
    for i in range(nx):
      sum1 += z[i]*z[i]
      sum2 += np.cos(2.0*PI*z[i])
    sum1 = -0.2*np.sqrt(sum1/nx)
    sum2 /= nx
    f =  E - 20.0*np.exp(sum1) - np.exp(sum2) + 20.0
    return f

  def griewank_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    s = 0.0
    p = 1.0

    z = self.sr_func (x, nx, Os, Mr, 600.0/100.0, s_flag, r_flag)
    for i in range(nx):
      s += z[i]*z[i]
      p *= np.cos(z[i]/np.sqrt(1.0+i))
    f = 1.0 + s/4000.0 - p
    return f

  def rastrigin_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    f = 0.0

    z = self.sr_func (x,  nx, Os, Mr, 5.12/100.0, s_flag, r_flag)
    for i in range(nx):
      f += (z[i]*z[i] - 10.0*np.cos(2.0*PI*z[i]) + 10.0)
    return f

  def schwefel_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    f = 0.0

    z = self.sr_func (x, nx, Os, Mr, 1000.0/100.0, s_flag, r_flag)

    for i in range(nx):
      z[i] += 4.209687462275036e+002
      if z[i]>500 :	
        f-=(500.0-np.fmod(z[i],500))*np.sin(pow(500.0-np.fmod(z[i],500),0.5))
        tmp=(z[i]-500.0)/100
        f+= tmp*tmp/nx
      elif (z[i]<-500):
        f-=(-500.0 + np.fmod(np.fabs(z[i]),500))*np.sin(pow(500.0-np.fmod(np.fabs(z[i]),500),0.5))
        tmp=(z[i]+500.0)/100
        f+= tmp*tmp/nx
      else:
        f-=z[i]*np.sin(pow(np.fabs(z[i]),0.5))
    f +=4.189828872724338e+002*nx
    return f


  def grie_rosen_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    f = 0.0

    z = self.sr_func (x, nx, Os, Mr, 5.0/100.0, s_flag, r_flag)

    z[0] += 1.0
    for i in range(nx-1):
      z[i+1] += 1.0
      tmp1 = z[i]*z[i]-z[i+1]
      tmp2 = z[i]-1.0
      temp = 100.0*tmp1*tmp1 + tmp2*tmp2
      f += (temp*temp)/4000.0 - np.cos(temp) + 1.0
      
    tmp1 = z[nx-1]*z[nx-1]-z[0]
    tmp2 = z[nx-1]-1.0
    temp = 100.0*tmp1*tmp1 + tmp2*tmp2
    f += (temp*temp)/4000.0 - np.cos(temp) + 1.0 
    return f

  def escaffer6_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    z = self.sr_func (x, nx, Os, Mr, 1.0, s_flag, r_flag)
    f = 0.0
    for i in range(nx - 1):
      temp1 = np.sin(np.sqrt(z[i]*z[i]+z[i+1]*z[i+1]))
      temp1 =temp1*temp1
      temp2 = 1.0 + 0.001*(z[i]*z[i]+z[i+1]*z[i+1])
      f += 0.5 + (temp1-0.5)/(temp2*temp2)
    temp1 = np.sin(np.sqrt(z[nx-1]*z[nx-1]+z[0]*z[0]))
    temp1 =temp1*temp1
    temp2 = 1.0 + 0.001*(z[nx-1]*z[nx-1]+z[0]*z[0])
    f += 0.5 + (temp1-0.5)/(temp2*temp2)
    return f

  def happycat_func(self, x, nx, Os, Mr, s_flag, r_flag):

    alpha=1.0/8.0
    z = self.sr_func (x,  nx, Os, Mr, 5.0/100.0, s_flag, r_flag)
    r2 = 0.0
    sum_z=0.0
    for i in range(nx):
      z[i]=z[i]-1.0
      r2 += z[i]*z[i]
      sum_z += z[i]
    f = pow(np.fabs(r2-nx),2*alpha) + (0.5*r2 + sum_z)/nx + 0.5
    return f

  def hgbat_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    alpha=1.0/4.0

    z = self.sr_func (x, nx, Os, Mr, 5.0/100.0, s_flag, r_flag)

    r2 = 0.0
    sum_z=0.0
    for i in range(nx):
      z[i]=z[i]-1.0
      r2 += z[i]*z[i]
      sum_z += z[i]
    
    f = pow(np.fabs(pow(r2,2.0)-pow(sum_z,2.0)),2*alpha) + (0.5*r2 + sum_z)/nx + 0.5
    return f

  @count_calls
  def schaffer_F7_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    f = 0.0
    z = self.sr_func (x, nx, Os, Mr, 1.0, s_flag, r_flag)
    for i in range(nx -1):
      z[i]=pow(y[i]*y[i]+y[i+1]*y[i+1],0.5)
      tmp=np.sin(50.0*pow(z[i],0.2))
      f += pow(z[i],0.5)+pow(z[i],0.5)*tmp*tmp 
    f = f*f/(nx-1)/(nx-1)
    return f

  @count_calls
  def step_rastrigin_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    f = 0.0
    for i in range(nx):
      if (np.fabs(y[i]-Os[i])>0.5):
        y[i]=Os[i]+np.floor(2*(y[i]-Os[i])+0.5)/2

    z = self.sr_func (x, nx, Os, Mr, 5.12/100.0, s_flag, r_flag)

    for i in range(nx):
      f += (z[i]*z[i] - 10.0*np.cos(2.0*PI*z[i]) + 10.0)
    return f

  @count_calls
  def levy_func(self, x, nx, Os, Mr, s_flag, r_flag):
    
    f = 0.0
    z = self.sr_func (x, nx, Os, Mr,1.0, s_flag, r_flag)

    w = [1]*nx

    sum1= 0.0
    for i in range(nx):
      w[i] = 1.0 + (z[i] - 0.0)/4.0

    term1 = pow((np.sin(PI*w[0])),2)
    term3 = pow((w[nx-1]-1),2) * (1+pow((np.sin(2*PI*w[nx-1])),2))

    Sum = 0.0

    for i in range(nx - 1):
      wi = w[i]
      newv = pow((wi-1),2) * (1+10*pow((np.sin(PI*wi+1)),2))
      Sum = Sum + newv
    f = term1 + Sum + term3
    del(w)
    return f

  @count_calls
  def zakharov_func(self, x, nx, Os, Mr, s_flag, r_flag):
    z = self.sr_func(x, nx, Os, Mr,1.0, s_flag, r_flag)
    f = 0.0
    sum1 = 0.0
    sum2 = 0.0
    for i in range(nx):
      xi = z[i]
      sum1 = sum1 + pow(xi,2)
      sum2 = sum2 + 0.5*(i+1)*xi

    f = sum1 + pow(sum2,2) + pow(sum2,4)
    return f

  def katsuura_func(self, x, nx, Os, Mr, s_flag, r_flag):
  
    f = 1.0
    tmp3=pow(1.0*nx,1.2)

    z = self.sr_func (x, nx, Os, Mr, 5.0/100.0, s_flag, r_flag)

    for i in range(nx):
      temp=0.0
      for j in range(1, 33):
        tmp1=pow(2.0,j)
        tmp2=tmp1*z[i]
        temp += np.fabs(tmp2-np.floor(tmp2+0.5))/tmp1
      f *= pow(1.0+(i+1)*temp,10.0/tmp3)
    tmp1=10.0/nx/nx
    f = f*tmp1-tmp1
    return f

  @count_calls
  def hf02(self, x, nx, Os, Mr, S, s_flag, r_flag):
    
    cf_num = 3
    fit = [None]*3
    G = [None]*3
    G_nx = [None]*3
    Gp = [0.4,0.4,0.2]

    tmp=0
    for i in range(cf_num-1):
      G_nx[i] = np.ceil(Gp[i]*nx)
      tmp += G_nx[i]
    G_nx[cf_num-1]=nx-tmp
    G_nx = np.int64(G_nx)
    G[0]=0
    for i in range(1, cf_num):
      G[i] = G[i-1]+G_nx[i-1]
  
    z = self.sr_func (x, nx, Os, Mr, 1.0, s_flag, r_flag)
    S = list(map(int, S))
    for i in range(nx):
      y[i]=z[S[i]-1]
    i=0
    fit[i] = self.bent_cigar_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=1
    fit[i] = self.hgbat_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=2
    fit[i] = self.rastrigin_func(y[G[i]:nx],G_nx[i],Os,Mr,0,0)

    f = 0.0
    for i in range(cf_num):
      f += fit[i]
    return f

  @count_calls
  def hf10(self, x, nx, Os, Mr, S, s_flag, r_flag):
    
    cf_num=6
    fit = [None]*6
    G = [None]*6
    G_nx = [None]*6
    Gp= [0.1,0.2,0.2,0.2,0.1,0.2]

    tmp=0
    for i in range(cf_num-1):
      G_nx[i] = np.ceil(Gp[i]*nx)
      tmp += G_nx[i]
    G_nx[cf_num-1]=nx-tmp
    G_nx = np.int64(G_nx)
    G[0]=0
    for i in range(1, cf_num):
      G[i] = G[i-1]+G_nx[i-1]

    z = self.sr_func (x, nx, Os, Mr, 1.0, s_flag, r_flag)
    S = list(map(int, S))
    for i in range(nx):
      y[i]=z[S[i]-1]

    i=0
    fit[i] = self.hgbat_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=1
    fit[i] = self.katsuura_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=2
    fit[i] = self.ackley_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=3
    fit[i] = self.rastrigin_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=4
    fit[i] = self.schwefel_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=5
    fit[i] = self.schaffer_F7_func(y[G[i]:nx],G_nx[i],Os,Mr,0,0)

    f = 0.0
    for i in range(cf_num):
      f += fit[i]
    return f

  @count_calls
  def hf06(self, x, nx, Os, Mr, S, s_flag, r_flag):
    
    cf_num=5
    fit = [None]*5
    G = [None]*5
    G_nx = [None]*5
    Gp = [0.3,0.2,0.2,0.1,0.2]

    tmp=0
    for i in range(cf_num-1):
      G_nx[i] = np.ceil(Gp[i]*nx)
      tmp += G_nx[i]
    G_nx[cf_num-1]=nx-tmp
    G_nx = np.int64(G_nx)
    G[0]=0
    for i in range(1, cf_num):
      G[i] = G[i-1]+G_nx[i-1]

    z = self.sr_func (x, nx, Os, Mr, 1.0, s_flag, r_flag)
    S = list(map(int, S))
    for i in range(nx):
      y[i]=z[S[i]-1]
    i=0
    fit[i] = self.katsuura_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=1
    fit[i] = self.happycat_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=2
    fit[i] = self.grie_rosen_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=3
    fit[i] = self.schwefel_func(y[G[i]:G[i+1]],G_nx[i],Os,Mr,0,0)
    i=4
    fit[i] = self.ackley_func(y[G[i]:nx],G_nx[i],Os,Mr,0,0)
    f = 0.0
    for i in range(cf_num):
      f += fit[i]
    return f

  @count_calls
  def cf01(self, x, nx, Os, Mr, s_flag, r_flag):
    cf_num=5
    fit = [None]*5
    delta = [10, 20, 30, 40, 50]
    bias = [0, 200, 300, 100, 400]

    i=0
    fit[i] = self.rosenbrock_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+4
    i=1
    fit[i] = self.ellips_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+10
    i=2
    fit[i] = self.bent_cigar_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+30
    i=3
    fit[i] = self.discus_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+10
    i=4
    fit[i] = self.ellips_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,0)
    fit[i]=10000*fit[i]/1e+10
    f = cf_cal(x, nx, Os, delta,bias,fit,cf_num)
    return f

  @count_calls
  def cf02(self, x, nx, Os, Mr, s_flag, r_flag):
    cf_num=3
    fit = [None]*3
    delta = [20,10,10]
    bias = [0, 200, 100]

    i=0
    fit[i] = self.schwefel_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,0)
    i=1
    fit[i] = self.rastrigin_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    i=2
    fit[i] = self.hgbat_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    f = cf_cal(x, nx, Os, delta,bias,fit,cf_num)
    return f

  @count_calls
  def cf06(self, x,  nx, Os, Mr, s_flag, r_flag):
    cf_num=5
    fit = [None]*5
    delta = [20,20,30,30,20]
    bias = [0, 200, 300, 400, 200]
    i=0
    fit[i] = self.escaffer6_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/2e+7
    i=1
    fit[i] = self.schwefel_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    i=2
    fit[i] = self.griewank_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=1000*fit[i]/100
    i=3
    fit[i] = self.rosenbrock_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    i=4
    fit[i] = self.rastrigin_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+3
    f = cf_cal(x,  nx, Os, delta,bias,fit,cf_num)
    return f

  @count_calls
  def cf07(self, x, nx, Os, Mr, s_flag, r_flag):
    cf_num=6
    fit = [None]*6
    delta = [10,20,30,40,50,60]
    bias = [0, 300, 500, 100, 400, 200]
    i=0
    fit[i] = self.hgbat_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1000
    i=1
    fit[i] = self.rastrigin_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+3
    i=2
    fit[i] = self.schwefel_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/4e+3
    i=3
    fit[i] = self.bent_cigar_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+30
    i=4
    fit[i] = self.ellips_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/1e+10
    i=5
    fit[i] = self.escaffer6_func(x,nx,Os[i*nx:(i+1)*nx],Mr[i*nx:(i+1)*nx,0:nx],1,r_flag)
    fit[i]=10000*fit[i]/2e+7
    f = cf_cal(x,  nx, Os, delta,bias,fit,cf_num)
    return f

  def shiftfunc(self, x,  nx, Os):
    xshift = np.zeros((nx,))
    for i in range(nx):
      xshift[i]=x[i] - Os[i]  
    return xshift

  def rotatefunc(self, x, nx, Mr):
    xrot = np.zeros((nx,))
    for i in range(nx):
      for j in range(nx):
        xrot[i]=xrot[i]+x[j]*Mr[i][j]
    return xrot

  def sr_func(self, x, nx, Os, Mr, sh_rate, s_flag, r_flag):
    global y
    sr_x = [None]*(nx)

    nx = int(nx)
    if (s_flag==1):
      if (r_flag==1):
        y = self.shiftfunc(x, nx, Os)
        for i in range(nx):
          y[i]=y[i]*sh_rate        
        
        sr_x = self.rotatefunc(y, nx, Mr)
      else:
        sr_x = self.shiftfunc(x, nx, Os)
        for i in range(nx):
          sr_x[i]=sr_x[i]*sh_rate
    else:
      if (r_flag==1):
        for i in range(nx):
          y[i]=x[i]*sh_rate
        sr_x = self.rotatefunc(y, nx, Mr)
      else:
        for i in range(nx):
          sr_x[i]=x[i]*sh_rate
    z = sr_x
    return z
  

  def asyfunc(self, x, xasy, nx, beta):
    for i in range(nx):
      if (x[i]>0):
        xasy[i]=pow(x[i],1.0+beta*i/(nx-1)*pow(x[i],0.5))

  def oszfunc(self, x, xosz, nx):
    
    for i in range(nx):
      if (i==0|i==nx-1):
        if (x[i]!=0):
          xx=np.log(np.fabs(x[i]))
        if (x[i]>0):
          c1=10
          c2=7.9
        else:
          c1=5.5
          c2=3.1
        if (x[i]>0):
          sx=1
        elif (x[i]==0):
          sx=0
        else:
          sx=-1
        xosz[i]=sx*np.exp(xx+0.049*(np.sin(c1*xx)+np.sin(c2*xx)))
      else:
        xosz[i]=x[i]

  def cf_cal(self, x, nx, Os, delta, bias, fit, cf_num):
    w_max=0
    w_sum=0
    w = [None]*cf_num
    for i in range(cf_num):
      fit[i]+=bias[i]
      w[i]=0
      for j in range(nx):
        w[i]+=pow(x[j]-Os[i*nx+j],2.0)
      if (w[i]!=0):
        w[i]=pow(1.0/w[i],0.5)*np.exp(-w[i]/2.0/nx/pow(delta[i],2.0))
      else:
        w[i]=INF
      if (w[i]>w_max):
        w_max=w[i]

    for i in range(cf_num):
      w_sum=w_sum+w[i]
    if(w_max==0):
      for i in range(cf_num):
        w[i]=1
      w_sum=cf_num
    f = 0.0
    for i in range(cf_num):
      f = f+w[i]/w_sum*fit[i]
    del(w)
    return f
  
  def config_cec_functions(self, nx, func_num):
    self.nx = nx
    self.function_to_call = func_num
    self.OShift = None 
    self.M = None 
    self.y = None
    self.z = None 
    self.x_bound = None 
    self.ini_flag = 0
    self.n_flag = None 
    self.func_flag = None
    self.SS = None
    self.cf_num = 10
    if (func_num < 1)|(func_num > 12):
      print('\nError: Test function %d is not defined.\n' %func_num)
    if self.ini_flag == 1:
      if (self.n_flag != nx)|(self.func_flag != func_num):
        self.ini_flag = 0

    if self.ini_flag == 0:
      del(self.M)
      del(self.OShift)
      del(self.y)
      del(self.z)
      del(self.x_bound)
      self.y = [0]*nx
      self.z = [None]*nx
      self.x_bound = [100.0]*nx

      if (nx!=2|nx!=10|nx!=20):
        print("\nError: Test functions are only defined for D=2,10,20.\n")

      if (nx==2)&(func_num==6 | func_num==7 | func_num==8):
        print("\nError:  NOT defined for D=2.\n")
        
      # Load M matrix
      FileName = "input_data/M_%d_D%d.txt"%(func_num, nx)
      try:
        self.M = np.loadtxt(FileName)
      except:
        print("\n Error: Cannot open M_%d_D%d.txt for reading \n" %(func_num,nx))
  #    if M==None:
  #      print("\nError: there is insufficient memory available!\n")
      del(FileName)
      
      # Shift data
      FileName = "input_data/shift_data_%d.txt" %func_num
      
      try:
        OShift_temp = np.loadtxt(FileName)
        del(FileName)
        if (func_num < 9):
            self.OShift = np.zeros((nx,))
            for i in range(nx):
                self.OShift[i] = OShift_temp[i]
        else:
            
            self.OShift = np.zeros((self.cf_num-1,nx))
            for i in range(self.cf_num-1):
                for j in range(nx):
                    self.OShift[i,j] = OShift_temp[i,j]
            self.OShift = np.reshape(self.OShift, (self.cf_num-1)*nx)
      except:
        print("\n Error: Cannot open shift_data_%d.txt for reading \n" %func_num)
  #    if OShift == None:
  #      print("\nError: there is insufficient memory available!\n")

      if (func_num >= 6) & (func_num <=8):
          FileName = "input_data/shuffle_data_%d_D%d.txt" %(func_num, nx)
          try:
            self.SS = np.loadtxt(FileName)
          except:
            print("\n Error: Cannot open shuffle_data_%d_D%d.txt for reading \n" %(func_num, nx))
    
          del(FileName)

      self.n_flag = nx
      self.func_flag = func_num
      self.ini_flag = 1

  def call_cec22_func(self, x):    
    # f = np.zeros((self.mx,))
    # for i in range(self.mx):
    ff = 0.0
    if self.function_to_call == 1:
      ff = self.zakharov_func(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 300.0
    elif self.function_to_call == 2:
      ff = self.rosenbrock_func(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 400.0
    elif self.function_to_call == 3:
      ff = self.schaffer_F7_func(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 600.0
    elif self.function_to_call == 4:
      ff = self.step_rastrigin_func(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 800.0
    elif self.function_to_call == 5:
      ff = self.levy_func(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 900.0
    elif self.function_to_call == 6:
      ff = self.hf02(x, self.nx, self.OShift, self.M, self.SS, 1, 1)
      ff = ff + 1800.0
    elif self.function_to_call == 7:
      ff = self.hf10(x, self.nx, self.OShift, self.M, self.SS, 1, 1)
      ff = ff + 2000.0
    elif self.function_to_call == 8:
      ff = self.hf06(x, self.nx, self.OShift, self.M, self.SS, 1, 1)
      ff = ff + 2200.0
    elif self.function_to_call == 9:
      ff = self.cf01(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 2300.0
    elif self.function_to_call == 10:
      ff = self.cf02(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 2400.0
    elif self.function_to_call == 11:
      ff = self.cf06(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 2600.0
    elif self.function_to_call == 12:
      ff = self.cf07(x, self.nx, self.OShift, self.M, 1, 1)
      ff = ff + 2700.0
    else:
      print("\nError: There are only 12 test functions in this test suite!\n")
      ff = 0.0
      # f[i] = 0.0
    
    # stopping algorithm execution when error reaches 10*(-8)
    if abs(ff - self.get_function_min(self.function_to_call)) < 1e-8:
      raise FuncCallsLimitReachedException
    return ff
    
# class cec2022_func():
  
#     def __init__(self, func_num):

#         self.func = func_num
        

#     def values(self, x):
        
#         nx, mx = np.shape(x)
#         ObjFunc = np.zeros((mx,))
#         for i in range(mx):
#             ObjFunc[i] = cec22_test_func(x[:,i], nx, 1, self.func)
#         self.ObjFunc = ObjFunc
        
        
#         return self