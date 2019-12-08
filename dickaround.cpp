// simple_camera.cpp
// MIT License
// Copyright (c) 2019 JetsonHacks
// See LICENSE for OpenCV license and additional information
// Using a CSI camera (such as the Raspberry Pi Version 2) connected to a 
// NVIDIA Jetson Nano Developer Kit using OpenCV
// Drivers for the camera and OpenCV are included in the base image

// #include <iostream>
#include <opencv2/opencv.hpp>
// #include <opencv2/videoio.hpp>
// #include <opencv2/highgui.hpp>

std::string gstreamer_pipeline (int capture_width, int capture_height, int display_width, int display_height, int framerate, int flip_method) {
    return "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)" + std::to_string(capture_width) + ", height=(int)" +
           std::to_string(capture_height) + ", format=(string)NV12, framerate=(fraction)" + std::to_string(framerate) +
           "/1 ! nvvidconv flip-method=" + std::to_string(flip_method) + " ! video/x-raw, width=(int)" + std::to_string(display_width) + ", height=(int)" +
           std::to_string(display_height) + ", format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink";
}

int main()
{
    int capture_width = 1280;
    int capture_height = 720 ;
    int display_width = 640 ;
    int display_height = 360 ;
    int framerate = 120 ;
    int flip_method = 0 ;

    std::string pipeline = gstreamer_pipeline(capture_width,
	capture_height,
	display_width,
	display_height,
	framerate,
	flip_method);
    std::cout << "Using pipeline: \n\t" << pipeline << "\n";
 
    cv::VideoCapture cap(pipeline, cv::CAP_GSTREAMER);
    if(!cap.isOpened()) {
	std::cout<<"Failed to open camera."<<std::endl;
	return (-1);
    }

    cv::namedWindow("CSI Camera", cv::WINDOW_NORMAL);
    cv::setWindowProperty("CSI Camera", cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN);
    cv::Mat img;
    cv::Mat img2;
    cv::Mat prevImg;
    cv::Mat tmp;
    int count = 0;
    float scale = .8;
    float scale2 = .5;

    float lag = .4;

    float rgbfactor[3] = {0,scale*2,scale*2};
    float iter = .08;
    float iters[3] = {iter, iter, -iter};
    
    cv::Scalar yea;
    yea = cv::Scalar::all(255);

    std::cout << "Hit ESC to exit" << "\n" ;
    while(true)
    {
    	if (!cap.read(img)) {
		std::cout<<"Capture read error"<<std::endl;
		break;
	}
	
	// 1. inverts image
	//img = 255-img;
	

       	/* */
 	// 2. rainbow cycle	
	img2 = img.mul(cv::Scalar(rgbfactor[0],rgbfactor[1],rgbfactor[2]));


	// 3. inverted rainbow cycle
	//img = yea-img.mul(cv::Scalar(rgbfactor[0]-scale2,rgbfactor[1]-scale2,rgbfactor[2]-scale2)));

	for (int j = 0; j < 3; j++){
		if (rgbfactor[j] > scale*3 || rgbfactor[j] < 0){
			iters[j] = -iters[j];
			//iters[(j+1) % 3] = -iters[(j+1) % 3];
			//iter = -iter; not right, but could be interesting
		}
		rgbfactor[j] += iters[j];
	}
	/**/
        std::cout << rgbfactor[0];


	/*
	// 4. ghostly afterimage
	img = img*(1-lag) + prevImg*lag;
	if (count == 0){
		count = 1;
		prevImg = img;
	} else{ 
		cv::imshow("CSI Camera", img);
	}*/
	
	
	// 5. Subtract last image - crappy motion detection AKA trex
	/*  
	if (count == 0){
		count = 1;
		prevImg = img;
	} else{ 
		cv::imshow("CSI Camera", img-prevImg);
	}*/
	
	// 6. Optical Flow
	//cv::calcOpticalFlowFarneback(prevImg,img,img,.5,1,5,1,5,5,cv::OPTFLOW_FARNEBACK_GAUSSIAN);
	

	//prevImg = img.clone();	


	cv::imshow("CSI Camera", img2);
	//Let us escape the fullscreen - alt+tab works too
	int keycode = cv::waitKey(30) & 0xff ; 
        if (keycode == 27) break ;
    }

	printf("andy sucks\n");
    cap.release();
    cv::destroyAllWindows() ;
    return 0;
}


