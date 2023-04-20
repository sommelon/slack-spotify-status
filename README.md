# ARCHIVED
### Development continues here: https://github.com/sommelon/spotify-slack-status




# Display the current song as yout status on Slack
- No need to add an app to your workspace
- Uses Selenium to automate the task, so not very lightweigth


## Setup
1. Run `pip install -r requirements.txt`
2. Copy contents of `env.example` to `.env`
3. Create a Spotify app at https://developer.spotify.com/dashboard
4. Update the variables in `.env`

## Usage
1. Run `python3 selenium/main.py`
2. Log in to Slack
3. Log in to Spotify (a window in your default browser should automatically open)
4. Start playing songs


## Issues
### If you want to log in to a different Spotify account
- Remove `.cache` file

### If you opened a new window to log in via 3rd party provider and the status doesn't update
- Copy the URL of the current workspace and open it in the first tab
- Close all other windows
- You shouldn't use the opened browser for anything else
