# Evolutionary_algorithms_benchmark_platform
A website for ranking evolutionary algorithms uploaded by users. <br />
As there is a risk that the uploaded code may be an exploit, each algorithm is executed in a dedicated AWS Firecracker microVM.

## Main Features
- User registration with email confirmation  
- Uploading algorithms by users
- Background testing of algorithms on complex and diverse mathematical functions
- Secure execution of untrusted code by utilizing microVMs as a sandbox environment
- Visualized benchmark results of all user-submitted algorithms, presented through three different ranking methods
- Viewing information on the user dashboard  
- Admin panel for managing users, information, and uploaded algorithms   

## Technologies
- **Frontend:** React, JavaScript, HTML, CSS  
- **Backend:** Flask (Python)
- **Tests:** pytest
- **Database:** MySQL, Redis (for server-side session management), SQLAlchemy (ORM)  
- **MicroVMs:** Managed and launched using AWS Firecracker, with setup and execution handled via shell scripts initiated from the backend  


# Setup and Launch instructions
## run frontend
### installing Node.js if is not present
sudo apt update <br />
sudo apt install nodejs npm <br />

### running app
cd react-app <br />
npm install <br />
npm start <br />


## run backend
python3 -m venv .venv <br />
source .venv/bin/activate <br />
pip install -r requirements.txt <br />
chmod +x run_app.sh <br />
sudo ./run_app.sh <br />


## setup MySql database
### installing mysql server
sudo apt update <br />
sudo apt install mysql-server <br />
### creating mysql user
sudo mysql -u root <br />
CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'test_password'; <br />
GRANT ALL PRIVILEGES ON \*.\* TO 'test_user'@'localhost' WITH GRANT OPTION; <br />
EXIT; <br />

### creating DB
sudo mysql -u test_user -p <br />
CREATE DATABASE alg_ranking_db; <br />
EXIT; <br />

## setup Redis database
### installing redis
sudo apt update <br />
sudo apt install redis-server <br />

### starting redis
sudo systemctl start redis.service <br />

### checking redis state
systemctl status redis.service <br />
*● redis-server.service - Advanced key-value store* <br />
     *Loaded: loaded (/lib/systemd/system/**redis-server.service**; enabled; vendor >* <br />
     *Active: active (running) since Mon 2024-08-19 17:52:10 CEST; 1 day 15h ago*

### enabling autostart
sudo systemctl enable redis-server.service <br />


## setup sandbox environment
there is a Readme file in /backend/microVM directory containing the instructions

## run tests
(from base directory)
cd backend <br />
source .venv/bin/activate <br />
(pip install -r requirements.txt *if not done earlier*) <br/ >
cd .. <br />
PYTHONPATH=./backend pytest

## important information
admin user passes: <br />
email: 'admin' <br />
password: 'admin' <br />

Two examplary evolutionary algorithm with required interface are located in: <br />
*/backend/algorithm.py* <br />
*/backend/algorithm_v2.py* <br />
