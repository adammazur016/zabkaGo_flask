## How to use .env and .flaskenv
**.env** and **.flaskenv** are environmental variables used to configure application. They may contain api keys or passwords
which shouldn't be pushed to GitHub repo.

To make your configuration type:
* Linux: `cp .env.example .env` and `cp .flaskenv.example .flaskenv` 
* Windows: `copy .env.example .env` and `copy .flaskenv.example .flaskenv`
* or simply make copy via your file manager

Then use text editor to edit variables to your need.