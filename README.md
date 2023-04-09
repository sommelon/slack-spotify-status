## Display the current song as yout status on Slack
- No need to add an app to your workspace
- Uses Selenium to automate the task, so not very lightweigth

1. Run `main.py`
2. Log in to Slack
3. Log in to Spotify
4. Start playing songs


## Issues
### If you want to log in to a different Spotify account
- Remove `.cache` file

### If you opened a new window to log in via 3rd party provider and the status doesn't update
- Copy the URL of the current workspace and open it in the first tab
- Close all other windows
- You shouldn't use the opened browser for anything else
