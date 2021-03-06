#Daniel D. Lee, Alex Kushleyev, Kelsey Saulnier, Nikolay Atanasov
import numpy as np
import bresenham2D
# INPUT
# im              the map
# x_im,y_im       physical x,y positions of the grid map cells
# vp(0:2,:)       occupied x,y positions from range sensor (in physical unit)
# xs,ys           physical x,y,positions you want to evaluate "correlation"
#
# OUTPUT
# c               sum of the cell values of all the positions hit by range sensor
def mapCorrelation(im, x_im, y_im, vp, xs, ys, theta=np.array([0])):
  nx = im.shape[0]
  ny = im.shape[1]
  xmin = x_im[0]
  xmax = x_im[-1]
  xresolution = (xmax-xmin)/(nx-1)
  ymin = y_im[0]
  ymax = y_im[-1]
  yresolution = (ymax-ymin)/(ny-1)
  nxs = xs.size
  nys = ys.size
  ntheta = theta.size
  cpr = np.zeros((ntheta, nxs, nys))
  for jtheta in range(0, ntheta):
    R = np.array([[np.cos(theta[jtheta]), -np.sin(theta[jtheta])], [np.sin(theta[jtheta]), np.cos(theta[jtheta])]])
    vs = np.dot(R, vp[0:2,:])
    for jy in range(0,nys):
      y1 = vs[1,:] + ys[jy] # 1 x 1076
      iy = np.int16(np.round((y1-ymin)/yresolution))
      for jx in range(0,nxs):
        x1 = vs[0,:] + xs[jx] # 1 x 1076
        ix = np.int16(np.round((x1-xmin)/xresolution))
        valid = np.logical_and( np.logical_and((iy >=0), (iy < ny)), \
                                                  np.logical_and((ix >=0), (ix < nx)))
        cpr[jtheta,jx,jy] = np.sum(im[ix[valid],iy[valid]])
  return cpr


#Bresenham's line algorithm
def getMapCellsFromRay(x0t,y0t,xis,yis):
    nPoints = np.size(xis)
    xyio = np.array([[],[]])
    for x1, y1 in zip(xis,yis):
        ox,oy = bresenham2D.bresenham2D(x0t,y0t,x1,y1)
        xyio = np.concatenate((xyio,np.array([ox,oy])),axis=1)

    return xyio