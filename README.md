# Zabka Go
Backend do projektu "Żabka Go" na zaliczenie przedmiotu "Aplikacje Mobilne"
## Usage
Application is prepared for containerization with docker-compose plugin. To test application use: \
`git clone https://github.com/adammazur016/zabkaGo_flask` \
`cd zabkaGo_flask` \
`cp .env.example .env` \
`docker-compose up` \
Database should be initialized with default tables and application should be ready to use: \
Default flask address: http://0.0.0.0:5000 \
Default phpmyadmin address: http://0.0.0.0:8080 \
Default database address: 0.0.0.0:3306 \

## Restarting database initialization
Database initializes only during first start. Data is persistent and won't reinitialize until volume is deleted.
TO-DO: List commands for removing volume