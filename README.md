# Twitch Streamer Live Checker

This script checks if specified Twitch streamers are live and opens their streams in a web browser when they go live. It also periodically prompts the user if they want to reopen any previously watched streams.

## Prerequisites

- Python 3.x
- `requests` library (install via `pip install requests`)

## Setup

1. Clone this repository or download the script.
2. Replace `your_client_id` and `your_client_secret` in the script with your Twitch API credentials.

## Usage

Run the script:

```bash
python twitch_live_checker.py
```

## How It Works

1. **Authentication**: The script uses your Twitch API credentials to obtain an OAuth token.
2. **Streamer Status Check**: It checks if the specified streamers are live by querying the Twitch API.
3. **Alerts**: When a streamer goes live, the script opens their stream in a web browser and plays a beep sound.
4. **Periodic Prompt**: Every hour, the script prompts the user to ask if they want to reopen any previously watched streams.

## Default Streamers

If no streamers are specified by the user, the script monitors the following default streamers:
- `theprimeagen`
- `squishymuffinz`
- `rocketleague`
- `johnnyboi_i`
- `rlesports`
- `ranny`

## Custom Streamers

You can specify custom streamers by entering their usernames separated by commas within 15 seconds after running the script. If you don't provide any input, the script will use the default list of streamers.

## Script Details

### get_app_access_token(client_id, client_secret)

Fetches an OAuth token from Twitch.

### is_live(username, access_token)

Checks if a specific streamer is live on Twitch.

### input_with_timeout(timeout=15)

Prompts the user to input streamer names within a specified timeout period.

### prompt_for_input(queue, prompt, timeout=15)

Prompts the user for input with a timeout.

### prompt_reopen(queue)

Periodically prompts the user if they want to reopen previously watched streams.

### main()

Main function that initializes the script, monitors streamers, and handles user prompts.

## Example

```bash
python twitch_live_checker.py
```

You will be prompted to enter streamer names separated by commas. If no input is provided within 15 seconds, the script will use the default list of streamers.

## Contributing

Feel free to submit issues or pull requests for improvements or additional features.
