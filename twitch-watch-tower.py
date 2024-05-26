import logging
import threading
from queue import Queue, Empty
import requests
import webbrowser
import time
import winsound

# Alert sound settings
DURATION = 1000  # milliseconds
FREQ = 440  # Hz

# Replace these with your Twitch API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_app_access_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['access_token']

def is_live(username, access_token):
    url = f'https://api.twitch.tv/helix/streams?user_login={username}'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return len(data['data']) > 0, data['data'][0]['id'] if data['data'] else None

def input_with_timeout(timeout=15):
    logging.info(f"Enter streamer names separated by commas within {timeout} seconds, or press Enter to use default streamers:")
    input_list = []
    input_thread = threading.Thread(target=lambda: input_list.append(input()))
    input_thread.start()
    input_thread.join(timeout)
    if input_thread.is_alive():
        logging.info("Time's up! Using default streamer list...")
        return ""
    return input_list[0]

def prompt_for_input(queue, prompt, timeout=15):
    logging.info(prompt)
    input_thread = threading.Thread(target=lambda q: q.put(input()), args=(queue,))
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)
    if input_thread.is_alive():
        logging.info("Continuing without reopening tabs...")
        queue.put('no')

def prompt_reopen(queue):
    while True:
        try:
            logging.info("Waiting for check message...")
            message = queue.get(timeout=3600)  # timeout set to 3600 seconds (1 hour)
            logging.info(f"Received message: {message}")
            if message == 'check':
                logging.info("Received 'check' signal, preparing to prompt user.")
                winsound.Beep(FREQ, DURATION)
                prompt_queue = Queue()
                prompt_for_input(prompt_queue, "Do you want to reopen any previously watched streamer? Enter 'yes' to reopen all closed tabs, or press Enter to continue monitoring:")
                response = prompt_queue.get()
                logging.info(f"User response received: {response}")
                queue.put(response.strip().lower())
        except Empty:
            logging.info("No message received within timeout, continuing...")

def main():
    input_queue = Queue()
    thread = threading.Thread(target=prompt_reopen, args=(input_queue,))
    thread.daemon = True
    thread.start()

    input_streamers = input_with_timeout()

    if input_streamers.strip():
        streamers = [s.strip() for s in input_streamers.split(',')]
    else:
        streamers = ['theprimeagen', 'squishymuffinz', 'rocketleague', 'johnnyboi_i', 'rlesports', 'ranny']

    access_token = get_app_access_token(CLIENT_ID, CLIENT_SECRET)
    logging.info(f"Monitoring the following streamers: {', '.join(streamers)}")

    live_streams = {}
    time_last_checked = time.time()

    while True:
        if time.time() - time_last_checked >= 3600:  # Check every hour
            logging.info(f"About to send 'check' message to queue at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            input_queue.put('check')  # Send signal to prompt user
            time_last_checked = time.time()

        for streamer in streamers:
            try:
                live, stream_id = is_live(streamer, access_token)
                if live and streamer not in live_streams:
                    logging.info(f"{streamer} is live! Opening in browser...")
                    winsound.Beep(FREQ, DURATION)
                    webbrowser.open_new_tab(f'https://www.twitch.tv/{streamer}')
                    live_streams[streamer] = stream_id
                elif not live and streamer in live_streams:
                    logging.info(f"{streamer}'s stream has ended.")
                    del live_streams[streamer]
                else:
                    logging.info(f"{streamer} is not live or already opened. Checking again in 60 seconds.")
            except requests.RequestException as e:
                logging.error(f"Error checking stream status for {streamer}: {e}")
        
        time.sleep(60)  # Check every 60 seconds

if __name__ == '__main__':
    main()
