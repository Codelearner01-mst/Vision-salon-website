"""
test_book.py - Unit tests for the booking system (book.py routes).

Tests cover three route endpoints:
  1. GET /book              - Renders the booking page with services, stylists, and time slots
  2. POST /check-day         - AJAX endpoint that checks stylist availability and returns booked time slots
  3. POST /book-appointment  - AJAX endpoint that creates an appointment and sends a confirmation email

Test data is seeded in setUp() with:
  - 2 services (Basic Haircut $25, Quality Brading $50)
  - 2 stylists (John Doe: Mon-Thu, Paul Aquero: Mon-Fri)
  - 2 booking times (10:00 AM, 12:00 PM)
  - 5 weekdays (Mon-Fri)
  - 3 existing appointments (for booked_times testing)

All tests use an in-memory SQLite database that is created and dropped per test.
send_email is mocked with @patch to prevent real emails from being sent.
"""

import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import BookingTimesModel, ServiceModel, TeamModel
from app.models.team_model import WeekdaysModel, TeamWorkdaysModel
from app.models.book_model import AppointmentsModel
from datetime import time, date


class TestBook(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        bt = BookingTimesModel(time=time(10, 0))
        bt2 = BookingTimesModel(time=time(12, 0))
        service = ServiceModel(headline='Haircut', name='Basic Haircut', description='A simple cut', image='img.jpg', duration_min=30, duration_max=60, price=25.0, descriptionII='Extra detail')
        service2 = ServiceModel(headline='Brading', name='Quality brading', description='A quality brading to look beauty', image='Image2.png', duration_min=25, duration_max=40, price=50.0, descriptionII='Another long description')
        team_member = TeamModel(name='John Doe', role='Stylist', image='john.jpg', bio='Experienced stylist')
        team_member2 = TeamModel(name='Paul Aquero', role='Stylist', image='paul.jpg', bio='An Extraodinary stylist')

        db.session.add_all([bt, bt2, service, service2, team_member, team_member2])
        db.session.commit()

        # Seed weekdays
        days = [
            WeekdaysModel(day_num=0, name='Monday'),
            WeekdaysModel(day_num=1, name='Tuesday'),
            WeekdaysModel(day_num=2, name='Wednesday'),
            WeekdaysModel(day_num=3, name='Thursday'),
            WeekdaysModel(day_num=4, name='Friday'),
        ]
        db.session.add_all(days)
        db.session.commit()

        # Assign workdays: John works Mon-Thu, Paul works Mon-Fri
        john_days = WeekdaysModel.query.filter(WeekdaysModel.day_num.in_([0, 1, 2, 3])).all()
        paul_days = WeekdaysModel.query.filter(WeekdaysModel.day_num.in_([0, 1, 2, 3, 4])).all()
        for day in john_days:
            db.session.add(TeamWorkdaysModel(member_id=team_member.id, day_id=day.id))
        for day in paul_days:
            db.session.add(TeamWorkdaysModel(member_id=team_member2.id, day_id=day.id))
        db.session.commit()

        # Seed appointments for booked_times testing
        # July 20, 2026 is a Monday (day_num=0) - both John and Paul work
        a1 = AppointmentsModel(stylist_id=team_member.id, service_id=service.id, total=service.price, date=date(2026, 7, 20), time_id=bt.id, note='First time client',quest_name="Kofi Baa",email="Kofi22@gmail.com",phone_number="0543267765")
        a2 = AppointmentsModel(stylist_id=team_member2.id, service_id=service2.id, total=service2.price, date=date(2026, 7, 20), time_id=bt2.id, note='Allergic to ammonia',quest_name="Yaa Beisua",email="Yaa22@gmail.com",phone_number="0543276065")
        # July 16, 2026 is a Thursday (day_num=3) - both work
        a3 = AppointmentsModel(stylist_id=team_member.id, service_id=service2.id, total=service2.price, date=date(2026, 7, 16), time_id=bt.id,quest_name=" John Blay",email="johnB34@gmail.com",phone_number="0543285645")
        db.session.add_all([a1, a2, a3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_book_page(self):
        """GET /book should render the booking page with services, stylists, time slots, and workday labels."""
        response = self.client.get("/book")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        self.assertIn(b"10:00 AM", response.data)
        self.assertIn(b"12:00 PM", response.data)
        self.assertIn(b"John Doe", response.data)
        self.assertIn(b"Basic Haircut", response.data)
        self.assertIn(b"$25.0", response.data)
        self.assertIn(b"50.0", response.data)
        self.assertNotIn(b"10.0", response.data)
        self.assertIn(b"stylist", response.data)
        self.assertNotIn(b"An Extraodinary stylist", response.data)
        self.assertNotIn(b"A quality brading to look beauty", response.data)
        self.assertNotIn(b"Doesn't exist", response.data)
        self.assertIn(b"Mon", response.data)
        self.assertIn(b"Thu", response.data)
        self.assertIn(b"Fri", response.data)
        self.assertNotIn(b"Tue", response.data)
        self.assertNotIn(b"Wed", response.data)

    def test_day_check(self):
        """Directly test TeamModel.day_is_available() for both stylists on various weekdays."""
        john = db.session.get(TeamModel, 1)
        paul = db.session.get(TeamModel, 2)
        all_stylists = TeamModel.query.all()
        self.assertTrue(john.day_is_available("2026-07-14"))
        self.assertFalse(john.day_is_available("2026-07-18"))
        self.assertTrue(paul.day_is_available("2026-07-17"))
        self.assertFalse(paul.day_is_available("2026-07-19"))
        for t in all_stylists:
            self.assertTrue(t.day_is_available("2026-07-20"))
            self.assertTrue(t.day_is_available("2026-07-16"))
            self.assertFalse(t.day_is_available("2026-07-19"))
            self.assertFalse(t.day_is_available("2026-07-18"))

    def test_check_day_any_stylist_available_all_booked(self):
        """POST /check-day with stylist_id=any when all stylists are booked at a time should return that time in booked_times."""
        # July 20, 2026 is a Monday - both John and Paul work
        # Currently John has 10:00, Paul has 12:00
        # Add Paul at 10:00 too, so 10:00 is fully booked (2 stylists, 2 appointments at 10:00)
        john = TeamModel.query.filter_by(name='John Doe').first()
        paul = TeamModel.query.filter_by(name='Paul Aquero').first()
        service = ServiceModel.query.first()
        bt = BookingTimesModel.query.first()  # 10:00 AM
        a4 = AppointmentsModel(
            stylist_id=paul.id, service_id=service.id, total=service.price,
            date=date(2026, 7, 20), time_id=bt.id,
            quest_name="Kwame", email="kwame@gmail.com", phone_number="0543285567"
        )
        db.session.add(a4)
        db.session.commit()

        response = self.client.post("/check-day",
            json={"stylist_id": "any", "date": "2026-07-20"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("success", data)
        self.assertEqual(data["success"], "Day is available")
        self.assertIn("booked_times", data)
        # 10:00 AM should be fully booked (both John and Paul have appointments at 10:00)
        self.assertEqual(len(data["booked_times"]), 1)
        self.assertEqual(data["booked_times"][0]["time"], "10:00 AM")
        
    def test_check_day_any_stylist_available_not_all_booked(self):
        """POST /check-day with stylist_id=any when not all stylists are booked at a time should return empty booked_times."""
        # July 20, 2026 is a Monday - both John and Paul work
        # John has 10:00, Paul has 12:00 - neither time is fully booked
        # (only 1 of 2 stylists booked at each time)
        response = self.client.post("/check-day",
            json={"stylist_id": "any", "date": "2026-07-20"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("success", data)
        self.assertEqual(data["success"], "Day is available")
        self.assertIn("booked_times", data)
        # No time is fully booked, so booked_times should be empty
        self.assertEqual(len(data["booked_times"]), 0)

    def test_check_day_any_stylist_available_no_bookings(self):
        """POST /check-day with stylist_id=any on a day with no bookings should return success + 0 booked times."""
        response = self.client.post("/check-day",
            json={"stylist_id": "any", "date": "2026-07-14"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("success", data)
        self.assertEqual(data["success"], "Day is available")
        self.assertIn("booked_times", data)
        self.assertEqual(len(data["booked_times"]), 0)

    def test_check_day_any_stylist_not_available(self):
        """POST /check-day with stylist_id=any on a weekend (nobody works) should return None message."""
        response = self.client.post("/check-day",
            json={"stylist_id": "any", "date": "2026-07-18"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("None", data)
        self.assertEqual(data["None"], "No stylist available on this day.")

    def test_check_day_specific_stylist_available(self):
        """POST /check-day with a specific stylist (John) on a workday should return success + 1 booked time."""
        john = TeamModel.query.filter_by(name='John Doe').first()
        response = self.client.post("/check-day",
            json={"stylist_id": john.id, "date": "2026-07-20"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('success', data)
        self.assertEqual(data["success"], "Day is available")
        self.assertIn("booked_times", data)
        self.assertEqual(len(data["booked_times"]), 1)

    def test_check_day_specific_stylist_not_available(self):
        """POST /check-day with John on a Friday (he does not work) should return None message."""
        john = TeamModel.query.filter_by(name='John Doe').first()
        response = self.client.post("/check-day",
            json={"stylist_id": john.id, "date": "2026-07-17"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("None", data)
        self.assertEqual(data["None"], "Selected sytlist is not available on this day")

    def test_check_day_paul_available_friday(self):
        """POST /check-day with Paul on a Friday (he works Fridays) should return success + 0 booked times."""
        paul = TeamModel.query.filter_by(name='Paul Aquero').first()
        response = self.client.post("/check-day",
            json={"stylist_id": paul.id, "date": "2026-07-17"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("success", data)
        self.assertEqual(data["success"], "Day is available")
        self.assertIn("booked_times", data)
        self.assertEqual(len(data["booked_times"]), 0)

    def test_check_day_invalid_request(self):
        """POST /check-day with an invalid stylist_id (not any and not an int) should return Error."""
        response = self.client.post("/check-day",
            json={"stylist_id": "invalid", "date": "2026-07-20"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Error", data)
        self.assertEqual(data["Error"], "The request was invalid")

    # ---------- book_appointment tests ----------

    def test_book_appointment_invalid_details(self):
        """Empty JSON body should return invalid."""
        response = self.client.post("/book-appointment", json={})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertEqual(data["invalid"], "Couldn't placed the order. Got invalid details!")

    def test_book_appointment_missing_guest_details(self):
        """Valid service/stylist/date/time but no guest_details should return invalid."""
        service = ServiceModel.query.first()
        stylist = TeamModel.query.first()
        bt = BookingTimesModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": service.id,
                "stylist_id": stylist.id,
                "total": service.price,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": None
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertEqual(data["invalid"], "Couldn't placed the order. Quest details was not provided!")

    @patch("app.book.book.send_email")
    def test_book_appointment_success(self, mock_send_email):
        """Valid booking should save appointment, return success message, and call send_email."""
        service = ServiceModel.query.first()
        stylist = TeamModel.query.first()
        bt = BookingTimesModel.query.first()

        # Count appointments before
        count_before = AppointmentsModel.query.count()

        response = self.client.post("/book-appointment",
            json={
                "service_id": service.id,
                "stylist_id": stylist.id,
                "total": service.price,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Test Guest",
                    "email": "testguest@gmail.com",
                    "phone_number": "0240000000",
                    "note": "This is a test booking"
                }
            })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("success", data)
        self.assertIn("Test Guest", data["success"])
        self.assertIn(service.name, data["success"])
        self.assertIn(stylist.name, data["success"])

        # Verify appointment was saved to the database
        count_after = AppointmentsModel.query.count()
        self.assertEqual(count_after, count_before + 1)

        # Verify the saved appointment has the correct data
        saved = AppointmentsModel.query.filter_by(quest_name="Test Guest").first()
        self.assertIsNotNone(saved)
        self.assertEqual(saved.email, "testguest@gmail.com")
        self.assertEqual(saved.phone_number, "0240000000")
        self.assertEqual(saved.note, "This is a test booking")
        self.assertEqual(saved.total, service.price)

        # Verify send_email was called with the right arguments
        mock_send_email.assert_called_once()
        call_kwargs = mock_send_email.call_args
        self.assertEqual(call_kwargs[1]["to"], "testguest@gmail.com")
        self.assertEqual(call_kwargs[1]["subject"], "Booking Confirmation - Vision Salon")
        self.assertEqual(call_kwargs[1]["name"], "Test Guest")

    @patch("app.book.book.send_email")
    def test_book_appointment_error(self, mock_send_email):
        """Non-existent service/stylist IDs should be caught by .get() validation and return invalid."""
        bt = BookingTimesModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": 9999,
                "stylist_id": 9999,
                "total": 25.0,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Error Guest",
                    "email": "error@gmail.com",
                    "phone_number": "0240000000",
                    "note": "This should fail"
                }
            })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("does not exist", data["invalid"])

        # Verify send_email was NOT called (validation failed before email)
        mock_send_email.assert_not_called()

    # ---------- missing key validation tests ----------

    def test_book_appointment_missing_service_id(self):
        """Payload without service_id key should return invalid message."""
        bt = BookingTimesModel.query.first()
        stylist = TeamModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "stylist_id": stylist.id,
                "total": 25.0,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Test",
                    "email": "test@gmail.com",
                    "phone_number": "0240000000",
                    "note": "note"
                }
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("Service", data["invalid"])

    def test_book_appointment_missing_stylist_id(self):
        """Payload without stylist_id key should return invalid message."""
        bt = BookingTimesModel.query.first()
        service = ServiceModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": service.id,
                "total": 25.0,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Test",
                    "email": "test@gmail.com",
                    "phone_number": "0240000000",
                    "note": "note"
                }
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("Stylist", data["invalid"])

    def test_book_appointment_missing_time_id(self):
        """Payload without time_id key should return invalid message."""
        service = ServiceModel.query.first()
        stylist = TeamModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": service.id,
                "stylist_id": stylist.id,
                "total": 25.0,
                "date": "2026-07-14",
                "guest_details": {
                    "guest_name": "Test",
                    "email": "test@gmail.com",
                    "phone_number": "0240000000",
                    "note": "note"
                }
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("Time", data["invalid"])

    def test_book_appointment_missing_date(self):
        """Payload without date key should return invalid message."""
        bt = BookingTimesModel.query.first()
        service = ServiceModel.query.first()
        stylist = TeamModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": service.id,
                "stylist_id": stylist.id,
                "total": 25.0,
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Test",
                    "email": "test@gmail.com",
                    "phone_number": "0240000000",
                    "note": "note"
                }
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("Date", data["invalid"])

    def test_book_appointment_nonexistent_service_id(self):
        """Payload with service_id that does not exist in DB should return invalid."""
        bt = BookingTimesModel.query.first()
        stylist = TeamModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": 9999,
                "stylist_id": stylist.id,
                "total": 25.0,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Test",
                    "email": "test@gmail.com",
                    "phone_number": "0240000000",
                    "note": "note"
                }
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("does not exist", data["invalid"])

    def test_book_appointment_nonexistent_stylist_id(self):
        """Payload with stylist_id that does not exist in DB should return invalid."""
        bt = BookingTimesModel.query.first()
        service = ServiceModel.query.first()
        response = self.client.post("/book-appointment",
            json={
                "service_id": service.id,
                "stylist_id": 9999,
                "total": 25.0,
                "date": "2026-07-14",
                "time_id": bt.id,
                "guest_details": {
                    "guest_name": "Test",
                    "email": "test@gmail.com",
                    "phone_number": "0240000000",
                    "note": "note"
                }
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("invalid", data)
        self.assertIn("does not exist", data["invalid"])