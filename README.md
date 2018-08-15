# Gimprove - Backend

## Project Overview
Gimprove is a lightweight system built to digitalize fitness equipment. Once installed on regular machines, Gimprove
allows users to automatically track all relevant keyfigures of their activities such as the number of repetitions
or the weight used. Users get feedback in realtime and can analyze their progress in the Gimprove App. For more 
information about Gimprove, visit the [Gimprove-Website](www.gimprove.com).

Here's an overview over the Gimprove system and it's components:
![Overview over the single components of the Gimprove System](photos/ReadMe/GimproveSystem.png) 

There are three respositories for this project:
1) [Gimprove Backend](https://bitbucket.org/den_mei/gimprove_backend/src/master/): 
Gimprove Plattform hosting the Gimprove Website and providing the Gimprove-API.
2) [Gimprove-App](https://bitbucket.org/den_mei/gimprove_app/src/master/): User Interface.
3) [Gimprove-Client](https://bitbucket.org/den_mei/gimprove_app/src/master/): Client that is attached on the machines.

## Repository Overview
This repository contains the code for the Gimprove-server and serves for two purposes at the moment:

1) **Landing Page:** Code for the [Gimprove-Landing Page](www.gimprove.com)
2) **Tracker-Backend:** Server-logic of the Gimprove system. Includes a REST-API to retrieve, update, 
create and delete data from the git push application. To enable real-time tracking, websocket communication is used.

## Usage
To run the application locally, execute `python3 manage.py runserver`. The app will start to run under the following 
address: http://127.0.0.1:8000.

To test the tracker application, execute `python3 manage.py test tracker`.

### Build With

### Contributing
**Dennis Meisner:** meisnerdennis@web.de
