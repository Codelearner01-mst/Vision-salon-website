import requests
import threading

api_url = "http://127.0.0.1:5000/book-appointment"
def send_booking(quest_name, email, phone):
    payload =  {
        "stylist_id": 1,
        "service_id": 2,
        "total": 95,
        "date": "2026-07-21",
        "time_id": 5,
        "guest_details": {
          "guest_name":quest_name,
          "email":email,
          "phone_number": phone,
          "note": "Test race condition",
        }}
    print(f"[User {quest_name}] Clicking 'Book Now'...")
    response = requests.post(api_url,json = payload)
    print(f"Result for User {quest_name} Status Code: {response.status_code} | Data: {response.text}")

if __name__ == "__main__":
   user1 = threading.Thread(target=send_booking, args=("John Doe","Johndoe33@gmail.com","985567899"))
   user2 = threading.Thread(target=send_booking, args=("paul","paul44@gmail.com","44646766768"))

    # Fire them both off at the exact same split-second!
   user1.start()
   user2.start()

    # Tell this script to wait until both requests finish before ending
   user1.join()
   user2.join()