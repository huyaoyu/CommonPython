from __future__ import print_function

import argparse
import copy
import cv2
import json
import numpy as np
import os
import yaml

from CommonPython.Filesystem.Filesystem import get_filename_parts, test_directory

def parse_yaml(fn):
    # Load the YAML file.
    with open(fn, "r") as stream:
        try:
            y = yaml.safe_load(stream)
        except yaml.YAMLError as ex:
            print(ex)
            raise Exception("yaml.safe_load() failed.")
    
    return y

class OCVCalib(object):
    def __init__(self):
        super(OCVCalib, self).__init__()

        self.name              = None
        self.T_cam_imu         = None
        self.T_cn_cnm1         = None
        self.cam_overlaps      = None
        self.camera_model      = None
        self.distortion_coeffs = None
        self.distortion_model  = None
        self.intrinsics        = None

        self.imageHeight = None
        self.imageWidth  = None

        self.R = None
        self.T = None

    def convert_intrinsics(self, a):
        """
        Assume a is a 1D NumPy array.
        """

        assert a.shape[0] == 4
        assert len( a.shape ) == 1

        # Create a 3x3 zero matrix.
        m = np.zeros((3, 3), dtype=np.float64)

        # Fill in the elements.
        m[0, 0] = a[0]
        m[1, 1] = a[1]
        m[0, 2] = a[2]
        m[1, 2] = a[3]
        m[2, 2] = 1.0

        return m

    def convert_from_dict(self, d, name):
        self.name = name

        if ( "T_cam_imu" in d ):
            self.T_cam_imu = np.array( d["T_cam_imu"], dtype=np.float64 )
        
        if ( "T_cn_cnm1" in d ):
            self.T_cn_cnm1 = np.array( d["T_cn_cnm1"], dtype=np.float64 )
            self.R = copy.deepcopy( self.T_cn_cnm1[0:3, 0:3] ).reshape((3,3))
            self.T = copy.deepcopy( self.T_cn_cnm1[0:3, 3] ).reshape((3,1))
        
        if ( "cam_overlaps" in d ):
            self.cam_overlaps = np.array( d["cam_overlaps"], dtype=np.int64 )

        if ( "camera_model" in d ):
            self.camera_model = d["camera_model"]

        if ( "distortion_coeffs" in d ):
            self.distortion_coeffs = np.zeros((5, ), dtype=np.float64)
            self.distortion_coeffs[0:4] = np.array( d["distortion_coeffs"], dtype=np.float64 )
        
        if ( "distortion_model" in d ):
            self.distortion_model = d["distortion_model"]
        
        if ( "intrinsics" in d ):
            self.intrinsics = np.array( d["intrinsics"], dtype=np.float64 )
            self.intrinsics = self.convert_intrinsics(self.intrinsics)

        if ( "resolution" in d ):
            self.resolution  = np.array( d["resolution"], dtype=np.int64 )
            self.imageHeight = int(self.resolution[1])
            self.imageWidth  = int(self.resolution[0])
        
        if ( "rostopic" in d ):
            self.rostopic = d["rostopic"]

    def dump_2_file(self, d, prefix="", suffix="", flagReference=False):
        if ( self.intrinsics is not None ):
            np.savetxt( "%s/%sCameraMatrix%s.dat" % (d, prefix, suffix), self.intrinsics, fmt="%+.12e" )
        
        if ( self.distortion_coeffs is not None ):
            np.savetxt( "%s/%sDistortionCoefficient%s.dat" % (d, prefix, suffix), self.distortion_coeffs, fmt="%+.12e" )

        if ( flagReference ):
            if ( self.resolution is not None ):
                dictImageSize = { \
                    "height": int(self.resolution[1]), \
                    "width": int(self.resolution[0]), \
                    "size": int(self.resolution[0] * self.resolution[1] * 3)
                    }
                
                with open( "%s/ImageSize.json" % (d), "w" ) as stream:
                    json.dump(dictImageSize, stream)
        
        if ( self.R is not None ):
            np.savetxt( "%s/R.dat" % (d), self.R, fmt="%+.12e" )

        if ( self.T is not None ):
            np.savetxt( "%s/T.dat" % (d), self.T, fmt="%+.12e" )

    def __str__(self):
        s = "%s\n" % (self.name)
        s += "T_cam_imu = \n{}\n".format(self.T_cam_imu)
        s += "T_cn_cnm1 = \n{}\n".format(self.T_cn_cnm1)
        s += "cam_overlaps = {}\n".format(self.cam_overlaps)
        s += "camera_model = {}\n".format(self.camera_model)
        s += "distortion_coeffs = {}\n".format(self.distortion_coeffs)
        s += "distortion_model = {}\n".format(self.distortion_model)
        s += "intrinsics = \n{}\n".format(self.intrinsics)
        s += "resolution = {}\n".format(self.resolution)
        s += "rostopic = {}\n".format(self.rostopic)

        return s

class StereoCalib(object):
    def __init__(self):
        super(StereoCalib, self).__init__()

        self.cams = []

        self.R1 = None
        self.R2 = None
        self.P1 = None
        self.P2 = None
        self.Q  = None
        self.Roi1 = None
        self.Roi2 = None

        self.rmap = [[None],[None]]

    def stereo_yaml_2_ocv(self, fn, silent=True):
        # Load the YAML file.
        y = parse_yaml(fn)
        
        # Convert to OCVCalib objects.
        self.cams.append( OCVCalib() )
        self.cams[0].convert_from_dict(y["cam0"], "cam0")

        self.cams.append( OCVCalib() )
        self.cams[1].convert_from_dict(y["cam1"], "cam1")

        if ( not silent ):
            print(self.cams[0])
            print(self.cams[1])

        # cam1.T_cn_cnm1 == cam1.T_cam_imu.dot( np.linalg.inv( cam0.T_cam_imu ) )

        # Compute the rectification matrices.
        self.R1, self.R2, self.P1, self.P2, self.Q, self.Roi1, self.Roi2 = \
        cv2.stereoRectify(\
            self.cams[0].intrinsics, self.cams[0].distortion_coeffs,\
            self.cams[1].intrinsics, self.cams[1].distortion_coeffs,\
            (self.cams[0].imageWidth, self.cams[0].imageHeight),\
            self.cams[1].R, self.cams[1].T,\
            flags = cv2.CALIB_ZERO_DISPARITY, alpha = 0, newImageSize = (self.cams[0].imageWidth, self.cams[0].imageHeight))

        map1, map2 = cv2.initUndistortRectifyMap(\
            self.cams[0].intrinsics, self.cams[0].distortion_coeffs,\
            self.R1, self.P1,\
            ( self.cams[0].imageWidth, self.cams[0].imageHeight ), cv2.CV_16SC2)
        self.rmap[0] = [ map1, map2 ]

        map1, map2 = cv2.initUndistortRectifyMap(\
            self.cams[1].intrinsics, self.cams[1].distortion_coeffs,\
            self.R2, self.P2,\
            ( self.cams[1].imageWidth, self.cams[1].imageHeight ), cv2.CV_16SC2)
        self.rmap[1] = [ map1, map2 ]

    def dump_2_file(self, d):
        test_directory(d)

        # Save the camera calibrations into files.
        self.cams[0].dump_2_file(d, suffix="Left", flagReference=True)
        self.cams[1].dump_2_file(d, suffix="Right")

        np.savetxt( "%s/R1.dat"   % (d), self.R1,   fmt="%+.12e" )
        np.savetxt( "%s/R2.dat"   % (d), self.R2,   fmt="%+.12e" )
        np.savetxt( "%s/P1.dat"   % (d), self.P1,   fmt="%+.12e" )
        np.savetxt( "%s/P2.dat"   % (d), self.P2,   fmt="%+.12e" )
        np.savetxt( "%s/Q.dat"    % (d), self.Q,    fmt="%+.12e" )
        np.savetxt( "%s/Roi1.dat" % (d), self.Roi1, fmt="%+.12e" )
        np.savetxt( "%s/Roi2.dat" % (d), self.Roi2, fmt="%+.12e" )

    def rectify_image(self, img, idx):
        return cv2.remap( img, self.rmap[idx][0], self.rmap[idx][1], cv2.INTER_LINEAR )

if __name__ == "__main__":
    print("Convert a YAML calibration file to OpenCV files.")

    parser = argparse.ArgumentParser(description="Convert a YAML calibration file to files that could be read by OpenCV.")

    parser.add_argument("infile", type=str, \
        help="The input file.")
    
    parser.add_argument("--out-dir", type=str, default="", \
        help="The output directory. Leave blank for default.")

    args = parser.parse_args()

    # Stereo calibration.
    sc = StereoCalib()
    sc.stereo_yaml_2_ocv(args.infile)

    # Outout file.
    outDir = args.out_dir

    if ( "" == outDir ):
        parts = get_filename_parts(args.infile)
        outDir = "%s/OpenCV" % (parts[0])
    
    sc.dump_2_file(outDir)
