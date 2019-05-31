# Introduction
This is a repository to store the files of a new work timer app idea

# What you need to develop

This app was built using python3, so to develop you need to set a Python3 environment.
Python packages you will need:

- PyQt5
- pyinstaller
- qdarkstyle

I suggest you to install the virtualenv and virtualenvwrapper packages too, and create a python virtual environment on your machine. This way, you can have different python interpreters for each project you are working on.

# Step-by-step environment configuration tutorial

First, you will need to install python3 on your system, and configure a virtual enviroment for this project (I strongly suggest doing this). For this, you can follow the following tutorial (Install the latest python3 version available):

http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/

Do the steps until the **workon** topic.

After that, you will nedd to install the app required packages. This project has a requirements.txt file, which can be used to install all of them with a single command. Go to the main project folder, and on the terminal, type the following command:

```bash
pip install -r requirements.txt
```

And... you are done!

# Project folder structure

./requirements.txt   -> File used to install all the project python packages  
./**timer_app.py**   -> Project main file  
./**timer_app.spec**  -> Build configuration file
./dist/**timer_app.exe**   -> Executable builded with the pyinstaller command  
./sample/resources/images  -> Folder to store all the app images  
./sample/**main_window.py**   -> Python class for the main app window  
./sample/settings/**settings_widget.py**   -> Python class for the settings page widget  
./sample/times/**times_widget.py**   -> Python class for the checkout time calculator widget  
./sample/utils/**utils.py**  -> Python file containing all the util functions used on the app  

# Building a new executable file

After making the changes on the source code (timer_app.py), to build the new application, you will have to run the following command:

```bash
pyinstaller --onefile -w timer_app.spec
```

The --onefile flag will create a one file bundled executable  
The -w flag will hide the console when the app open  
The timer_app.spec is the configuration file that stores all the build configuration


# Setting a nice python development environment on vscode

If you use vscode, you can paste this on your .vscode/settings.json, located on this project folder:

```json
{
 "python.linting.pylintArgs": [
      "--extension-pkg-whitelist=PyQt5",
      "--max-line-length=120"
  ],
  "python.formatting.autopep8Args": [
      "--max-line-length=120"
  ],
  "python.linting.maxNumberOfProblems": 120,
  "[python]": {
      "editor.rulers": [
          120
      ],
      "editor.tabSize": 4
  }
}
```

This will setup some flags for the python linter i use (Pylint, you should install it on vscode!) and modify the max line lenght and tabsize