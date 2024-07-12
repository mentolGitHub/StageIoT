import numpy as np
import cv2 as cv



def contours_cleanup(contours):
    fixed_contours=[]
    for i in contours:
        if len(i)>10:
            fixed_contours.append( i)
    return fixed_contours

def local_contour(frame):
    contours = []
    max=0
    for l in range(0, round(len(frame))-5):
        contours.append([])

        for p in range(0,round(len(frame[0]))-5):
            x=frame[l,p+4]-frame[l,p]
            y=frame[l+4,p]-frame[l,p]

            
            x = np.sqrt(x[0]**2+x[1]**2+x[2]**2)
            y = np.sqrt(y[0]**2+y[1]**2+y[2]**2)
            
            pixel_contour = np.sqrt([x**2+ y**2])
            if pixel_contour[0]> max:
                max = pixel_contour[0] 
            # print(pixel_contour[0])
            contours[l].append(pixel_contour[0])
    contours = contours*255/max
    
    contours = np.mat(np.array(contours))
    return contours

def main():
    opened = False

    while not opened:
        cap = cv.VideoCapture(0)
        cap2 = cv.VideoCapture(2)
        if not cap.isOpened():
            print("Cannot open camera")    
        else:
            opened = True

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        ret, frame2 = cap2.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        imgray = cv.rotate(cv.cvtColor(frame, cv.COLOR_BGR2GRAY),cv.ROTATE_90_CLOCKWISE)
        imgray2 = cv.rotate(cv.cvtColor(frame2, cv.COLOR_BGR2GRAY),cv.ROTATE_90_CLOCKWISE)
        #analyse en composante principale
        
        cv.imshow("left", imgray)
        cv.imshow("right", imgray2)
        

        #disparity check
        stereo = cv.StereoBM.create(numDisparities=32, blockSize=21)
        disparity = stereo.compute(imgray,imgray2)
        norm_image = cv.normalize(disparity, None, alpha = 0, beta = 1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
        cv.imshow('not gray',norm_image)

        #distance evaluation



        
        if cv.waitKey(1) == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def test():
    pass



if __name__ == "__main__":
    test()
    main()