import numpy as np
import cv2
import glob
import argparse
import os
#import yaml
#import _pickle as pickle


class StereoCalibration(object):
    def __init__(self):
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS +
                         cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.criteria_cal = (cv2.TERM_CRITERIA_EPS +
                             cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((8*6, 3), np.float32)
        
        # resize the grid
        # the *30 at the end represents the 30mm size of each square in the checker board. 
        # If you print a checker board of a different size, please change the size here.
        self.objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)*30 

        # Arrays to store object points and image points from all the images.
        self.objpoints_l = []  # 3d point in real world space
        self.objpoints_r = []  # 3d point in real world space
        self.imgpoints_l = []  # 2d points in image plane.
        self.imgpoints_r = []  # 2d points in image plane.
        self.objpoints_stereo = []  # 3d point in real world space
        self.imgpoints_l_stereo = []  # 2d points in image plane.
        self.imgpoints_r_stereo = []  # 2d points in image plane.

        self.cal_path =  ""
        #self.cal_path = "/home/research/Public/Projects/Lantern3/cal_images/"
        self.read_images(self.cal_path)

    def read_images(self, cal_path):

        images_left = list()
        left_cal_path = os.path.join(self.cal_path ,'images/left')
        print(left_cal_path)
        for root,dir, files in os.walk(left_cal_path):
            for file in files:
                if file.endswith(".png"):
                    images_left.append(os.path.join(left_cal_path, file))

        right_cal_path = os.path.join(self.cal_path ,'images/right')
        images_right = list()
        for root,dir, files in os.walk(right_cal_path):
            for file in files:
                if file.endswith(".png"):
                    images_right.append(os.path.join(right_cal_path,file))
        assert(len(images_left) == len(images_right))
        images_left.sort()
        images_right.sort()

        for i, fname in enumerate(images_right):
            print(images_left[i], images_right[i])
            img_l = cv2.imread(images_left[i])
            img_r = cv2.imread(images_right[i])

            gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
            gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret_l, corners_l = cv2.findChessboardCorners(gray_l, (8, 6), None)
            ret_r, corners_r = cv2.findChessboardCorners(gray_r, (8, 6), None)

            # if((ret_l==0) or (ret_r == 0)):
            #     print("skipping this set")
            #     continue

            # If found, add object points, image points (after refining them) 
            # self.objpoints.append(self.objp)

            if ret_l is True:
                rt = cv2.cornerSubPix(gray_l, corners_l, (11, 11),
                                      (-1, -1), self.criteria)
                self.imgpoints_l.append(corners_l)
                self.objpoints_l.append(self.objp)

                # Draw and display the corners
                # ret_l = cv2.drawChessboardCorners(img_l, (8, 6),
                #                                   corners_l, ret_l)
                #cv2.imshow(images_left[i], img_l)
                #cv2.waitKey(500)

            if ret_r is True:
                rt = cv2.cornerSubPix(gray_r, corners_r, (11, 11),
                                      (-1, -1), self.criteria)
                self.imgpoints_r.append(corners_r)
                self.objpoints_r.append(self.objp)

                # Draw and display the corners
                # ret_r = cv2.drawChessboardCorners(img_r, (8, 6),
                #                                   corners_r, ret_r)
                #cv2.imshow(images_right[i], img_r)
                #cv2.waitKey(500)

            if((ret_l is True) and (ret_r is True)):
                self.imgpoints_l_stereo.append(corners_l)
                self.imgpoints_r_stereo.append(corners_r)
                self.objpoints_stereo.append(self.objp)
            else:
                print("Skipping this set for stereo calibration; checkerboard not found in one or of both the images")
                
            img_shape = gray_l.shape[::-1]

        rt, self.M1, self.d1, self.r1, self.t1 = cv2.calibrateCamera(
            self.objpoints_l, self.imgpoints_l, img_shape, None, None)
        rt, self.M2, self.d2, self.r2, self.t2 = cv2.calibrateCamera(
            self.objpoints_r, self.imgpoints_r, img_shape, None, None)

        self.camera_model = self.stereo_calibrate(img_shape)

    def stereo_calibrate(self, dims):
        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC
        # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
        flags |= cv2.CALIB_USE_INTRINSIC_GUESS
        flags |= cv2.CALIB_FIX_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_ASPECT_RATIO
        flags |= cv2.CALIB_ZERO_TANGENT_DIST
        # flags |= cv2.CALIB_RATIONAL_MODEL
        # flags |= cv2.CALIB_SAME_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_K3
        # flags |= cv2.CALIB_FIX_K4
        # flags |= cv2.CALIB_FIX_K5
        print("Images read, calibrating...")
        stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                cv2.TERM_CRITERIA_EPS, 100, 1e-5)
        ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
            self.objpoints_stereo, self.imgpoints_l_stereo,
            self.imgpoints_r_stereo, self.M1, self.d1, self.M2,
            self.d2, dims,
            criteria=stereocalib_criteria, flags=flags)

        print('RMS error:', ret)
        print('Intrinsic_mtx_1', M1)
        print('dist_1', d1)
        print('Intrinsic_mtx_2', M2)
        print('dist_2', d2)
        print('R', R)
        print('T', T)
        print('E', E)
        print('F', F)

        cv_file = cv2.FileStorage("images/calibration.yml", cv2.FILE_STORAGE_WRITE)
        cv_file.write("M1", M1)
        cv_file.write("d1", d1)
        cv_file.write("M2", M2)
        cv_file.write("d2", d2)
        cv_file.write("R", R)
        cv_file.write("T", T)
        cv_file.write("E", E)
        cv_file.write("F", F)
        cv_file.write("R1", np.asarray(self.r1))
        cv_file.write("R2", np.asarray(self.r2))
        cv_file.release()
        cv_file = cv2.FileStorage("intrinsics.yml", cv2.FILE_STORAGE_WRITE)
        cv_file.write("M1", M1)
        cv_file.write("D1", d1)
        cv_file.write("M2", M2)
        cv_file.write("D2", d2)
        cv_file.release()
        cv_file = cv2.FileStorage("extrinsics.yml", cv2.FILE_STORAGE_WRITE)
        cv_file.write("R", R)
        cv_file.write("T", T)
        cv_file.release()

        # for i in range(len(self.r1)):
        #     print("--- pose[", i+1, "] ---")
        #     self.ext1, _ = cv2.Rodrigues(self.r1[i])
        #     self.ext2, _ = cv2.Rodrigues(self.r2[i])
        #     print('Ext1', self.ext1)
        #     print('Ext2', self.ext2)

        print('')

        camera_model = dict([('M1', M1), ('M2', M2), ('dist1', d1),
                            ('dist2', d2), ('rvecs1', self.r1),
                            ('rvecs2', self.r2), ('R', R), ('T', T),
                            ('E', E), ('F', F)])

        cv2.destroyAllWindows()
        # with open('camera_calibration.yaml', 'w') as outfile:
        #     outfile.write(yaml.dump(camera_model, default_flow_style = False))
        # print('xxxxxxxxxxxxxxxxxxxxx')
        #with open('camera_calibration.yaml', 'r') as infile:
        #    print(yaml.load(infile))
        #np.save('Intrinsic_mtx_1.npy', M1)
        #np.save('Intrinsic_mtx_2.npy', M2)
        #np.save('dist1.npy', d1)
        #np.save('dist2.npy', d2)
        #np.save('rvecs1.npy', self.r1)
        #np.save('rvecs2.npy', self.r2)        #tmp = np.load('calibration_stats.npy', allow_pickle=True)
        #np.save('R.npy', R)
        #np.save('T.npy', T)        #print(tmp)
        #np.save('E.npy', E)
        #np.save('F.npy', F)
        return camera_model

if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--filepath', required = True, help='String Filepath')
    #args = parser.parse_args()
    #print('Calibration image directory ',args.filepath)
    cal_data = StereoCalibration()
