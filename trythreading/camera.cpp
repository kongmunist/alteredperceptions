#include "./camLib.hpp"

using namespace cv;

// Allocate memory for the frames to store and start the camera...
Camera cam1;
const int frameBuffer = 50;	// Frame buffer around motion ...
vector<Mat> frameStack = *new vector<Mat> [frameBuffer*sizeof(cam1.captureVideo())];	
vector<Mat> contourStack = *new vector<Mat> [frameBuffer*sizeof(cam1.captureVideo())];	
int stopSig = 0;				// Global stop signal...


void processFrame(void) {
	Mat frame;
	Mat gauss;
	Mat gray;
	Mat contour;
    // Check if there is data in the frame buffer...
    while(!::stopSig) {
		// If the frame stack is not empty grab a frame w/o removing it for further processing...:
		if(!::frameStack.empty())  {       // If the original video stack is not empty...
			frame = ::frameStack.front();   // --> take a the first frame from the original stack w/o removing it...
			
			//----------------------------------OpenCV image manipulations---------------------------------------
			//contour = frame;                            // --> Just pass the original frae through...
			// https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#threshold
			//cvtColor(frame, gray, CV_RGB2GRAY);	      // Converts an image from one color space to another. -- 
			GaussianBlur(frame, gauss, Size(5,5), 0, 0);  // https://www.bogotobogo.com/OpenCV/opencv_3_tutorial_imgproc_gausian_median_blur_bilateral_filter_image_smoothing.php
			///cvtColor(gauss, gray, CV_RGB2GRAY);	                 // Converts an image from one color space to another. -- 
			//threshold(gauss, contour, 50,255,THRESH_BINARY);	// Applies a fixed-level threshold to each array element.
			//Laplacian(gray, contour, 165, 3, 1, 0, BORDER_DEFAULT);
			///Canny(gray, contour, 50, 150, 3);
                        contour = frame.clone();
			//---------------------------------------------------------------------------------------------------
		}
		
		// 1. If the contour-stack has more then 2 frames remove the last frame (at back of the stack)...
		if (::contourStack.size() > 2) {	// If the contour-stack has more then 2 frames...
			// Remove the last frame from the stack...:
			::contourStack.pop_back();	
		}
		// 2. If a new processed frame is available and the stack is not yet full..:
		if(!contour.empty() && ::contourStack.size() < ::frameBuffer) {
			// Put the new processed frame at the front location of the stack...:
			::contourStack.push_back(contour);
		} else if(::contourStack.size() >= ::frameBuffer) { // only in case the stack has run full...
			// Clear the entire stack...:
			::contourStack.clear();	
		}
			

	}
	cout << "processFrame: esc key is pressed by user" << endl;
	return;
}

void grabFrame(void) {
	Mat frame;
	
	::frameStack.clear();
	while(!::stopSig) {
		frame = ::cam1.captureVideo();			// Capture a frame from the live stream of camera...
		// 1. Remove one frame from the back, if the stack has more then 2 frames...
		if(::frameStack.size() > 2) {		//If the framestack has more then 2 frames...
			// This line removes the last frame from the stack...
			::frameStack.pop_back();
		} 
		// 2. Add a frame at the front of the stack if the stack is not full...
		if (::frameStack.size() < ::frameBuffer) { 
			// This line puts frame-by-frame at the back of the stack...
			::frameStack.push_back(frame);	// Put new frame on stack on the computer's RAM...
		} else {
			// This line clears the stack when it is full...
			::frameStack.clear();
		}
		
	}
	cout << "grabFrame: esc key is pressed by user" << endl;
	return;
}


int main(int argc, char* argv[])
{
	Mat frame;					// Captured single frames...
	Mat contour;				// Video stream showin countours of objects...

	// Start endless loop to capture frames...
	// This endless loop is stopped by user pressing the ESC key...
	// Generate new file name with a time-stamp right after the sequence that was captures
	::frameStack.clear();
	::contourStack.clear();
	thread t1(grabFrame);
	thread t2(processFrame);
        cv::namedWindow("ap", cv::WINDOW_NORMAL);
        cv::setWindowProperty("ap", cv::WND_PROP_FULLSCREEN, cv::WINDOW_FULLSCREEN);

	while(1) {
		if(::contourStack.size() >= 2)  {
			contour = ::contourStack.back();
                        if (contour.rows != 0)
			imshow("ap", contour);
		}
		
		if (waitKey(1) == 27) 		//wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
		{
			cout << "Main: esc key is pressed by user" << endl;
			::stopSig = 1;		// Signal to threads to end their run...
			
			frameStack.clear();
			contourStack.clear();
			break; 
		}
	}
	t1.join();
	t2.join();

    return 0;
}
