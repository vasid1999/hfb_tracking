import numpy as np
import cv2
from matplotlib import pyplot as plt
import urllib.request as ur
import time

url='http://192.168.43.56:8080/shot.jpg'
print("entered loop")


#rec=cv2.VideoCapture(0)

while(1):
    print("in loop")
    # Use urllib to get the image from the IP camera
    imgResp = ur.urlopen(url)
    print("hi")
    
    # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    
    # Finally decode the array to OpenCV usable format ;)
    img2 = cv2.imdecode(imgNp,-1)
    MIN_MATCH_COUNT = 10
    #ret,img2=rec.read()
    img1 = cv2.imread('QR.jpeg',0)          # queryImage
    #img2 = cv2.imread('vraj2.jpeg',0) # trainImage
    #   img1=cv2.imread("QR.jpeg",0)
    # Initiate SIFT detector
    
    #img1=cv2.imread("QR.jpeg",0)
    sift = cv2.xfeatures2d.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
        
        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        
        if M is None:
            print('no')
        elif(len(M)>2):
            dst=cv2.perspectiveTransform(pts,M)
            dst=np.int32(dst)
            img2=cv2.polylines(img2,[np.int32(dst)],True,255,3,cv2.LINE_AA)
            a0=dst[0][0][0]
            a1=dst[0][0][1]
            a2=dst[1][0][0]
            a3=dst[1][0][1]
            a4=dst[2][0][0]
            a5=dst[2][0][1]
            a6=dst[3][0][0]
            a7=dst[3][0][1]
            
            
            d0=np.array([[a0,a1],[a2,a3]])
            d1=np.array([[a2,a3],[a4,a5]])
            d2=np.array([[a4,a5],[a6,a7]])
            d3=np.array([[a6,a7],[a0,a1]])
            
            
            
            
            det0=np.linalg.det(d0)
            det1=np.linalg.det(d1)
            det2=np.linalg.det(d2)
            det3=np.linalg.det(d3)
            
            area=0.5*abs(det0+det1+det2+det3)
            #print(d0)
            #print(d0.shape)
            print(area)
    else:
     print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
     matchesMask = None
     draw_params = dict(matchColor = (0,255,0), # draw matches in green color
     singlePointColor = None,
     matchesMask = matchesMask, # draw only inliers
                       flags = 2)
        
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    cv2.imshow('matches',img3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()

