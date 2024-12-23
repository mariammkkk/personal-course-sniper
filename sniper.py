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

# Preprocess course data to create a hash map of index -> openStatusText.
def preprocess_course_data(year, term):
    logging.info(f"Preprocessing course data for year: {year}, term: {term}")
    URL = f"{API_BASE_URL}year={year}&term={term}&campus=NB&subject=198"
    response = requests.get(URL)
    response.raise_for_status()
    courses_data = response.json()

    # Create a hash map for indices
    index_status_map = {}
    for course in courses_data:
        courseName = course.get("title")
        for section in course.get("sections", []):
            idx = section.get("index")
            open_status = section.get("openStatusText")
            index_status_map[idx] = {"status": open_status, "title": courseName}

    logging.info(f"Course data preprocessed. Total indices: {len(index_status_map)}")
    return index_status_map

# Fetches status for all specified indices used the prepocessed hashmap
def fetch_courses_status(preprocessed_data, indices):
    logging.info("Fetching statuses from preprocessed data...")
    status_map = {index: preprocessed_data.get(index, None) for index in indices}
    logging.info(f"Statuses fetched: {status_map}")
    return status_map

# Send notification via Twilio once a course is available to snipe 
def send_notification(requestedIndex, course_title):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body = f"COURSE OPEN: COURSE TITLE: [{course_title}], INDEX: [{requestedIndex}]",
        from_ = TWILIO_PHONE_NUMBER,
        to = PERSONAL_PHONE_NUMBER
    )
    logging.info(f"Course is open! Notification sent successfully: SID {msg.sid}")

# Course sniping LOOP
snipe = 0
def course_sniper(year, term, indices):
    global snipe
    logging.info("Starting course sniper...")
    preprocessed_data = preprocess_course_data(year, term)

    while indices:
        statuses = fetch_courses_status(preprocessed_data, indices)
        for index in list(indices):
            course_info = preprocessed_data.get(index)
            if course_info and course_info.get("status") == "OPEN":
                course_title = course_info.get("title", "Unknown Title")
                send_notification(index, course_title)
                indices.remove(index)
        if indices:
            logging.info(f"Waiting for indices: {indices}. Retrying in 5 seconds.")
            snipe += 1
            logging.info(f"SNIPE NUMBER: {snipe}")
            time.sleep(5)

if __name__ == '__main__':
     print("---- Welcome to Course Sniper ----")
     year = input("Enter YEAR of desired course : ")
     term = input("Enter TERM of desired course (FALL - 9, SPRING - 1, SUMMER - 7, WINTER - 0): ")
     indices = input("Enter INDICES of desired course (SEPARATED BY COMMAS): ").split(',')
     indices = [index.strip() for index in indices]
     course_sniper(year, term, indices)