# FinalYearProject
Github repository for my final year project (BSc Computer Science International)

# How to run:

## To run the Backend on localhost:
<ol>
    <li>Navigate into the /backend directory and run 'npm install' to download all of the required modules</li>
    <li>Make a JSON file called 'jwtKey.json' with one value "token": and whatever password you would like</li>
    <li>Now some changes have to be made in the code to change environment variables.You can either initialise it with your own Firebase database or remove Firebase integration:
        <ul>
        <li>Removing Firebase integration:</li>
            <ol>
            <li>comment out the 4th line initialising config with firebase details</li>
            <li>comment out lines 21 to 24 containing firebase initialisation</li>
            <li>comment out lines 72 to 87 containing sending a log</li>
            <li>now the backend should run on localhost:3000</li>
            </ol>
        </ul>
        <ul>
            <li>Adding your own Firebase database:</li>
            <ol>
            <li>The report contains information on making a firebase real time database</li>
            <li>once this is made you can add your databases information in the '/services/firebase.js'</li>
            <li>now backend will run on localhost linked to database</li>
            </ol>
        </ul>
    </li>
</ol>

## To run the Frontend (only tested in PyCharm 2021.3.3):
<ol>
    <li>Obtain the weights and cfg for YOLOv3-416 from https://pjreddie.com/darknet/yolo/ . Place these in a subdirectory called 'yolo' in the 'assets' folder -> 'assets/yolo'</li>
    <li>Open the project in PyCharm. Press "Add Configuration..." to add a Python Interpreter.</li>
    <li>Press "Add New Configuration" and select Python.</li>
    <li>Select "Script path:" to "main.py" in the frontend directory. And select a Python Interpreter, this project was developed on Python 3.7
    (make a virtual environment with PyCharm if you would like. "Settings -> Python Interpreter -> Add.. -> Virtualenv Environment"). Make sure that the base Python interpreter used has the optional feature "tcl/tk and IDLE" </li>
    <li>At this point the project should run and might respond with some modules not found. To fix this, navigate to where the python interpreter is located. If you use a PyCharm Virtualenv this will be in 'venv/Scripts/'. From there check that the following modules are installed with the following commands.
    <ul>
        <li>pip install opencv-contrib-python</li>
        <li>pip install Pillow</li>
        <li>pip install requests</li>
    </li>

</ol>