from time import sleep
import mysql.connector
import datetime
import threading
import pygame


db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="Pass",  # Replace with your MySQL password
    database="studyalarm"
)

cursor = db.cursor()
subject = ""
print("-----------------------------------------------------------")
print("Welcome to Study Alarm")
print("Here are your options:")
print("1. StartStudying")
print("2. ExitStudying")
print("-----------------------------------------------------------")

# Initialize pygame mixer
pygame.mixer.init()

# Function to play the alarm sound
def play_sound(stop_event):
    pygame.mixer.music.load('C:\\Videoer\\Alarm.mp3')
    pygame.mixer.music.play(-1)  # Loop the sound indefinitely
    while not stop_event.is_set():
        sleep(0.1)  # Check periodically if stop_event is set
    pygame.mixer.music.stop()  # Stop the music when stop_event is set

def StudySession():

    # Record start time
    python_timestamp = datetime.datetime.now().timestamp()
    dt_object = datetime.datetime.fromtimestamp(python_timestamp)
    day_of_week = dt_object.strftime('%A')
    start_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    print(day_of_week)
    print("Study Session Started")

    # Simulate study duration
    sleep(1800)

    # Record end time
    python_timestamp = datetime.datetime.now().timestamp()
    dt_object = datetime.datetime.fromtimestamp(python_timestamp)
    end_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    query = "INSERT INTO StudySessions (Subject, StartSession, EndSession, DayOfTheWeek) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (subject, start_time, end_time, day_of_week))
    db.commit()

    print("Study Session Ended. Time for a break!")

    # Play alarm sound
    stop_event = threading.Event()
    try:
        sound_thread = threading.Thread(target=play_sound, args=(stop_event,))
        sound_thread.start()
        input("Press Enter to stop the alarm and start your break: ")
        stop_event.set()
    finally:
        sound_thread.join()
        BreakSession()  # Start the break session

def BreakSession():
    print("Break Session started")
    sleep(300)  # Replace with actual break duration
    print("Break Session Ended. Time to study!")

    # Play alarm sound
    stop_event = threading.Event()
    try:
        sound_thread = threading.Thread(target=play_sound, args=(stop_event,))
        sound_thread.start()
        input("Press Enter to stop the alarm and return to studying: ")
        stop_event.set()
    finally:
        sound_thread.join()
        StudySession()  # Start the next study session




user_choice = input("Enter your choice: ")
if user_choice == "1":
    subject = input("What subject do you want to study?: ")
    StudySession()
elif user_choice == "2":
    cursor.close()
    quit()
