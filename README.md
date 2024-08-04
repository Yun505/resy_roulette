# Resy Roulette

**Resy Roulette** is a functional flask app catering to indecisive casual diners and food fanatics alike. The app allows its users to specify certain optional queries for restaurants, for example, the number of guests, location, or cuisine, before returning a random restaurant or restaurants that satisfy the requests.

## Features
**Resy Roulette** is written in Python in a Flask app, with plans of futures migration to AWS for hosting. The app helps users decide on a restaurant to eat at, with optional queries such as:
- Restaurant location
- Restaurant cuisine(s)
- and Number of guests,

helping to satisfy any requests.

The restaurants are found using calls to the Resy API.

![image](https://github.com/user-attachments/assets/c0b249ce-fef6-4609-b040-940e98ed8a01)


## Quickstart
### Installing Dependencies
Start by installing the dependencies in the `requirements.txt` file, either locally or within a virtual environment. This assumes you have pip installs, which is packaged automatically with all Python installations.

#### Local Installation
Just open a terminal in the main `resy_roulette` folder and run the following command:
```pip install -r requirements.txt```

#### Virtual Environment
Create a virtual environment in the `resy_roulette` folder. We recommend using `venv`, as it comes prepackaged with all Python installations. For help creating the virtual environment, we recommend checking out the `venv` documentation. Create a terminal instance, making sure you are in your virtual environment, and run the following command:
```pip install -r requirements.txt```

### Variable Setup
#### Getting API Keys and Tokens
The authorization, auth token, and universal auth can be found by sending any search query (or making any action, for that matter) on the Resy website with an account, inspecting the page, clicking to the network section, selecting any valid API request (we recommend the "search" request), and viewing the headers. The fields will be labelled as in our template (see next section).

#### Changing Environment Variables
Create a .env file in the main directory. You will need to collect your API token and key from Resy to use this app locally. Copy and paste the following template into `resy_roulette/.env`:
```
AUTHORIZATION='ResyAPI api_key="<Authorization>"'
XRESYAUTHTOKEN=<X-Resy-Auth-Token>
XRESYUNIVERSALAUTH=<X-Resy-Universal-Auth>
```
The authorization, auth token, and universal auth can be found by sending any search query (or making any action, for that matter) on the Resy website with an account, inspecting the page, clicking to the network section, selecting any valid API request (we recommend the "search" request), and viewing the headers. The fields will be labelled as in our template.

#### Change in Scripts
Alternatively, you can change the variables directly in the `retrieve.py` file. Search for the following line:
```
header = {"Authorization":os.environ["AUTHORIZATION"],
          "X-Resy-Auth-Token":os.environ["XRESYAUTHTOKEN"],
          "X-Resy-Universal-Auth": os.environ["XRESYUNIVERSALAUTH"]}
```

and replace it with

```
header = {"Authorization":<Authorization>,
          "X-Resy-Auth-Token":<X-Resy-Auth-Token>,
          "X-Resy-Universal-Auth": <X-Resy-Universal-Auth>}
```

replacing the fields with your corresponding keys and tokens.

### Launching the App
To launch the app locally, run the following command in your terminal:
```flask --app main  run    ```
## Future Plans
- Migrate to AWS

## Contributions
Big thanks to [Henry Liu](https://github.com/HenryLiu714) for his help with this project. Any additional contributions or pull requests are welcome from anyone!
