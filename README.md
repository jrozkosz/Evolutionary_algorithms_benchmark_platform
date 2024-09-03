# ranking_algorithms
A website for ranking evolutionary algorithms uploaded by users <br />


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
GRANT ALL PRIVILEGES ON *.* TO 'test_user'@'localhost' WITH GRANT OPTION; <br />
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

examplary evolutionary algorithm with required interface is located in: /backend/algorithm.py

