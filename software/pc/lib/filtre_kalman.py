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
    
  def filtrer(self, Z, u = None):
    # Anthony : On ne peut pas utiliser self dans les arguments par défaut
    # donc u = numpy.zeros(self.x.shape[0])[:, numpy.newaxis] ne passait pas
    if u == None:
        u = numpy.zeros(self.x.shape[0])[:, numpy.newaxis]
    # prediction
    self.x = (self.F * self.x) + u
    self.P = self.F * self.P * self.F.transpose() + self.Q
    
    # measurement update
    y = Z - (self.H * self.x)
    S = self.H * self.P * self.H.transpose() + self.R
    
    K = self.P * self.H.transpose() * numpy.linalg.inv(S)
    print K
    self.x = self.x + (K * y)
    self.P = (numpy.identity(self.x.shape[0]) - (K * self.H)) * self.P