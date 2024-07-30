# Resy Roulette

**Resy Roulette** is a functional flask app catering to indecisive casual diners and food fanatics alike. The app allows its users to specify certain optional queries for restaurants, for example, the number of guests, location, or cuisine, before returning a random restaurant or restaurants that satisfy the requests.

## Features
**Resy Roulette** is written in Python in a Flask app, with plans of futures migration to AWS for hosting. The app helps users decide on a restaurant to eat at, with optional queries such as:
- Restaurant location
- Restaurant cuisine(s)
- and Number of guests,

helping to satisfy any requests.

The restaurants are found using calls to the Resy API.

## Quickstart
You need to create a .env file in the main directory and input your authentication key to use the app and the post requests. 
To start in the Terminal:```flask --app main  run    ```
## Future Plans
- Migrate to AWS
