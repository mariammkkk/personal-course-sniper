# VERSION 1: Personal Course Sniper

A Python-based script that automates the process of monitoring course availability. It uses an API to check the status of course indices and notifies the user via SMS when a desired course becomes available.

---

## Features

- **Automated Course Monitoring**: Continuously polls the API for real-time updates on course status.
- **Multiple Indices**: Supports monitoring multiple course indices simultaneously.
- **SMS Notifications**: Sends a notification via Twilio when a course becomes available.
- **Configurable Options**: Users can input the year, term, and desired course indices to monitor.

---

## Requirements

- Python 3.7 or higher
- A Twilio account with active credentials for SMS notifications

---

## Installation

1. Clone the repository:
   `git clone https://github.com/mariammkkk/personal-course-sniper.git`\
   `cd personal-course-sniper`
   
2. Install required dependencies:
   `pip install -r requirements.txt`

3. Create a `.env` file in the project directory with the following environmental variables:
  - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
  - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
  - `TWILIO_PHONE_NUMBER`: The Twilio phone number to send notifications from
  - `PERSONAL_PHONE_NUMBER`: Your personal phone number to receive notifications for when a section is open

## Running the Script
`python3 sniper.py`

