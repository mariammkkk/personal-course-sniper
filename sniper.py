import os, time, json, requests, logging
from dotenv import load_dotenv
from twilio.rest import Client

logging.basicConfig(level=logging.INFO)

# Load information to set up notification system
logging.info("Loading environment variables...")
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
PERSONAL_PHONE_NUMBER = os.getenv('PERSONAL_PHONE_NUMBER')

# Define & fetch course data from Rutgers SOC API

# Rutgers terms: 9 - fall, 1 - spring,  7 - summer, 0 - winter
# Can filter link by adding '&subject=198&level=UG'
# 'subject' specifies which classes, 198 is all computer science courses
# 'level' specifies all classes available for undergrad at the moment

API_BASE_URL = 'https://classes.rutgers.edu//soc/api/courses.json?'

def fetch_course_status(year, term, index):
    logging.info(f"Fetching course status for year: {year}, term: {term}, index: {index}")
    URL = f"{API_BASE_URL}year={year}&term={term}&campus=NB&subject=198"
    response = requests.get(URL)
    response.raise_for_status()
    courses_data = response.json()
    for course in courses_data:
        for section in course.get("sections", []):
            if section.get("index") == str(index):
                status = section.get("openStatusText")
                logging.info(f"Course index {index} status: {status}")
                return status
    logging.warning(f"Index {index} not found in the course data")
    return None # no index found

# Send notification via Twilio once a course is available to snipe 
def send_notification(requestedIndex):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body = f"COURSE OPEN! INDEX: [{requestedIndex}]",
        from_ = TWILIO_PHONE_NUMBER,
        to = PERSONAL_PHONE_NUMBER
    )
    logging.info(f"Course is open! Notification sent successfully: SID {msg.sid}")

# Course sniping LOOP
def course_sniper(year, term, index):
    logging.info("Starting course sniper...")
    while True:
        course_status = fetch_course_status(year, term, index)
        if (course_status == "OPEN"):
            send_notification(index)
            break
        logging.info(f"Course {index} status: {course_status}. Retrying in 5 seconds.")
        time.sleep(5)   

if __name__ == '__main__':
     print("---- Welcome to Course Sniper ----")
     year = input("Enter YEAR of desired course : ")
     term = input("Enter TERM of desired course (FALL - 9, SPRING - 1, SUMMER - 7, WINTER - 0): ")
     index= input("Enter INDEX of desired course: ")
     course_sniper(year, term, index)