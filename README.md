# Algoverify
Verifies Algorand Smart Contract Codes against the one stored on Chain.
Provides support for Teal and Reach Smart Contracts.
Backend is written with FastApi and mongo-db while the frontend is written with ReactJs and Typescript.

# FRONTEND
The frontend is written in ReactJs and Typescript hosted on netflify.
It can be accessed via https://algoverify.netlify.app.

## Local Set Up
 - clone the repository
 - cd into `frontend` folder.
 - run `yarn install` or `npm install` to install dependencies.
 - run `yarn start` or `npm start` to start the frontend.

# BACKEND
The backend is written in python using FastApi and it uses mongo db to store data.
It is hosted on aws ec2 and can be accessed via https://algoverify.xyz .
## PostMan Documentation
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c1d8ca7e3ea318be050b?action=collection%2Fimport#?env%5BAlgoVerify%20%7C%20Live%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoiaHR0cHM6Ly9hbGdvdmVyaWZ5Lnh5eiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiaHR0cHM6Ly9hbGdvdmVyaWZ5Lnh5eiIsInNlc3Npb25JbmRleCI6MH1d)

## Local Set Up
- clone the repository
- cd into `backend` folder
- create a virtual environment and activate (you can use pipenv or venv for this)
- Install the requirements in `requirements.txt` (For venv)
- Create a  `.env` file with variables specified in `env.example` file (You can use [mongodb Atlas](https://www.mongodb.com/atlas/database) for free mongo db cluster).
- run `python main.py`
- You can also run the backend using docker (`Dockerfile`).

### NB: To verify reach contracts you need to have Docker installed.
