# Test Timer
<div>
  <a href="https://github.com/BradleyBao/test-timer/releases/latest">
    <img src="https://img.shields.io/github/v/tag/BradleyBao/test-timer?label=ver&style=for-the-badge">
  </a>
</div> 

## A simple, formal, lightweight timer

This project is based on [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) and [PyQt-Fluent Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) 

![image](https://github.com/BradleyBao/test-timer/assets/80588549/6107d390-1c82-4b32-bb5a-0d6e0e36ce65)


## How to use

- F3 to open setting 
- F11 to full screen the timer 

## Features

Test-timer is a lightweight, simple timer app. 

The timer is the best for displaying on a demonstrative screen. 
Test timer has various settings that allow users to customize their own timers. 


- [x] Color Settings - Every text (text, timer, and background) can be displayed in any colours you want. 
- [x] Sizes - The sizes of texts and timer can be modified. 
- [x] 30 seconds countdown - The timer can remind users when only 30 seconds left. 
- [x] Plans - Users can create different "plans" to save the timer.
- [ ] Users can pause the timer any time.
- [ ] Users can stop the timer any time.
- [x] Timed to start timer.
- [ ] Click to start timer.
- [ ] Run in background.
- [x] Windows Taskbar Progress

![image](https://github.com/BradleyBao/test-timer/assets/80588549/844ed9e5-15ac-4d68-af4a-c3ada6e11776)


## Installation

Test-timer requires python >= 3.7 to run. 
You need to download [PyQt-Fluent Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) in order to run this program. 
Download qfluentwidgets folder and add it to the main directory.  

```cmd
pip install -r requirements.txt
```
```cmd
python app.py 
```

First time running the program, it will automatically create two files: log file and user data file. 
