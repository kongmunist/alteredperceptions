#ifndef __IOSTREAM_INCLUDED__
#define __IOSTREAM_INCLUDED__

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <vector>
#include <unistd.h>
#include <thread>

using namespace cv;
using namespace std;

class Camera 
{
	public:
		Camera(void);
		~Camera(void);
		Mat captureVideo(void);
		
	private:
                Mat frame;
		double dWidth;
		double dHeight;
		double fps;
			
};


#endif	// __IOSTREAM_INCLUDED__
