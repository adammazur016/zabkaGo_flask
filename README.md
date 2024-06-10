# Zabka Go
Backend do projektu "Żabka Go" na zaliczenie przedmiotu "Aplikacje Mobilne". \
Aplikacja frontendowa: https://github.com/adammazur016/zabbkaGo_android
## Usage
Application is prepared for containerization with docker-compose plugin. To test application use: \
`git clone https://github.com/adammazur016/zabkaGo_flask` \
`cd zabkaGo_flask` \
`cp .env.example .env` on Linux or `copy .env.example .env` on Windows \
`docker-compose up --build` \
*Note: You can use `docker-compose watch` instead to automatically sync docker-compose with local changes*

Database should be initialized with default tables and application should be ready to use.
* Default flask address: http://0.0.0.0:5000
* Default phpmyadmin address: http://0.0.0.0:8080
* Default database address: 0.0.0.0:3306
* Default Swagger API documentation: http://0.0.0.0:5000/swagger

## Restarting database initialization
Database initializes only during first start. Data is persistent and won't reinitialize until volume is deleted.
To create new database from scratch (e.g. after updating **init.sql** file) use:\
`docker-compose down --volumes`

**Warning: All data will be lost**
