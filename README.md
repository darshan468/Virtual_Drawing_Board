**🖌️ Virtual Drawing Board using Computer Vision**

*📖 Project Description*

The Virtual Drawing Board is a real-time computer vision application that enables users to draw digitally in the air using hand gestures. By utilizing a webcam and advanced hand-tracking techniques, the system eliminates the need for traditional input devices such as a mouse, stylus, or touchscreen.

This project demonstrates the practical implementation of gesture recognition and human-computer interaction, making it suitable for applications in education, design, and interactive systems.

*🎯 Objectives*
To develop a touchless drawing interface using hand gestures
To implement real-time hand tracking with high accuracy
To provide an intuitive and user-friendly drawing experience
To explore the capabilities of computer vision in interactive applications

*✨ Key Features*
Real-time hand detection and tracking
Gesture-based drawing functionality
Dynamic color selection
Eraser tool for corrections
Smooth drawing experience with minimal latency
Live video feed integration with drawing overlay

*🧰 Tech Stack*
Programming Language: Python
Libraries & Frameworks:
OpenCV (for image processing)
MediaPipe (for hand tracking)
NumPy (for numerical operations)

*🏗️ System Architecture*

*The system follows a pipeline-based architecture:*

Video Capture: Webcam captures real-time frames
Preprocessing: Frames are processed for better detection
Hand Detection: MediaPipe identifies hand landmarks
Gesture Recognition: Finger positions determine actions
Drawing Engine: Tracks movement and renders on canvas
Display Output: Final output is shown with overlay
