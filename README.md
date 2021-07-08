# VideoCapture
Video capture using OpenCV and PySide6.

This is a simple application to capture image from camera. You can use mouse to grab a part of the video

**Quick start guide**
1. select you desired camera from the dropdown.
2. click on start capturing to start camera.
3. click on capture frame to draw rectangle on the video to capture.
4. save the file at your desired location

![image](https://user-images.githubusercontent.com/64060109/124935167-065a7200-e023-11eb-9ece-732d6ea7c24a.png)

Note the landscape image used in the above demo image is a Photo by <a href="https://unsplash.com/@cgcreates?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Cameron Gibson</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
To get the video devices I have used pygrabber library. You can also use the PyQt's QMultimedia to get the available video devices, 
but the current version of the PySide6 doesn't have the QMultimedia hence not used.
