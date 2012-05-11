# -*- coding: utf-8 -*-

import numpy

class FiltreKalman:
  
  def __init__(self,x,P,F,H,R,Q):
    self.x = x
    self.P = P
    self.F = F
    self.H = H
    self.R = R
    self.Q = Q
  
  def prediction(self, u = None):
    if u == None:
        u = numpy.zeros(self.x.shape[0])[:, numpy.newaxis]
    self.x = (self.F * self.x) + u
    self.P = self.F * self.P * self.F.transpose() + self.Q
  
  def measurement(self, Z):
    y = Z - (self.H * self.x)
    S = self.H * self.P * self.H.transpose() + self.R    
    K = self.P * self.H.transpose() * numpy.linalg.inv(S)
    self.x = self.x + (K * y)
    self.P = (numpy.identity(self.x.shape[0]) - (K * self.H)) * self.P
    
  def filtrer(self, Z, u = None):
    prediction(u)
    # measurement update
    measurement(Z)