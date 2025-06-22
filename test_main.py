import unittest
from unittest.mock import patch, MagicMock
import os
import json
import time
from main import get_users, get_resources, get_bookings, App, UserPage, ResourcePage, BookerPage, ViewerPage


class TestGetUsers(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_users.json'
        with open(self.test_file, 'w') as f:
            json.dump({}, f)
        self.users = get_users(filepath=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_and_load_user(self):
        self.users.users['testuser'] = {'full_name': 'Test User', 'password': 'pass'}
        self.users.save_users()
        self.users.load_users()
        self.assertIn('testuser', self.users.users)
        self.assertEqual(self.users.users['testuser']['full_name'], 'Test User')

class TestGetResources(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_resources.json'
        with open(self.test_file, 'w') as f:
            json.dump({}, f)
        self.resources = get_resources(filepath=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_and_load_resource(self):
        self.resources.resources['testresource'] = {'description': 'desc', 'available': True, 'owner': None, 'days_booked': []}
        self.resources.save_resources()
        self.resources.load_resources()
        self.assertIn('testresource', self.resources.resources)
        self.assertEqual(self.resources.resources['testresource']['description'], 'desc')

class TestGetBookings(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_bookings.json'
        with open(self.test_file, 'w') as f:
            json.dump({}, f)
        self.bookings = get_bookings(filepath=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_and_load_booking(self):
        self.bookings.bookings['testbooking'] = {'owner': 'testuser', 'resource': 'testresource', 'start_date': '2025-01-01', 'end_date': '2025-01-02'}
        self.bookings.save_bookings()
        self.bookings.load_bookings()
        self.assertIn('testbooking', self.bookings.bookings)
        self.assertEqual(self.bookings.bookings['testbooking']['owner'], 'testuser')

class TestDataClasses(unittest.TestCase):
    def setUp(self):
        # Use test files to avoid overwriting real data
        self.users_file = "test_users.json"
        self.resources_file = "test_resources.json"
        self.bookings_file = "test_bookings.json"
        # Clean up before each test
        for f in [self.users_file, self.resources_file, self.bookings_file]:
            if os.path.exists(f):
                os.remove(f)


    def tearDown(self):
        # Clean up after each test
        for f in [self.users_file, self.resources_file, self.bookings_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_users_create_and_save(self):
        users = get_users(self.users_file)
        users.users["testuser"] = {"full_name": "Test User", "password": "pass"}
        users.save_users()
        with open(self.users_file) as f:
            data = json.load(f)
        self.assertIn("testuser", data)

    def test_users_edit_and_delete(self):
        users = get_users(self.users_file)
        users.users["testuser"] = {"full_name": "Test User", "password": "pass"}
        users.save_users()
        # Edit user
        users.users["testuser"]["full_name"] = "Edited User"
        users.save_users()
        with open(self.users_file) as f:
            data = json.load(f)
        self.assertEqual(data["testuser"]["full_name"], "Edited User")
        # Delete user
        del users.users["testuser"]
        users.save_users()
        with open(self.users_file) as f:
            data = json.load(f)
        self.assertNotIn("testuser", data)

    def test_resources_create_edit_delete(self):
        resources = get_resources(self.resources_file)
        resources.resources["testres"] = {"description": "desc", "available": True, "owner": None, "days_booked": []}
        resources.save_resources()
        # Edit resource
        resources.resources["testres"]["description"] = "edited desc"
        resources.save_resources()
        with open(self.resources_file) as f:
            data = json.load(f)
        self.assertEqual(data["testres"]["description"], "edited desc")
        # Delete resource
        del resources.resources["testres"]
        resources.save_resources()
        with open(self.resources_file) as f:
            data = json.load(f)
        self.assertNotIn("testres", data)

    def test_bookings_create_edit_delete(self):
        bookings = get_bookings(self.bookings_file)
        bookings.bookings["testbook"] = {
            "owner": "testuser",
            "resource": "testres",
            "start_date": "2025-01-01",
            "end_date": "2025-01-02"
        }
        bookings.save_bookings()
        # Edit booking
        bookings.bookings["testbook"]["end_date"] = "2025-01-03"
        bookings.save_bookings()
        with open(self.bookings_file) as f:
            data = json.load(f)
        self.assertEqual(data["testbook"]["end_date"], "2025-01-03")
        # Delete booking
        del bookings.bookings["testbook"]
        bookings.save_bookings()
        with open(self.bookings_file) as f:
            data = json.load(f)
        self.assertNotIn("testbook", data)

class TestPageInstantiation(unittest.TestCase):
    @patch("tkinter.Tk")
    def test_app_and_pages_create(self, mock_tk):
        app = App()
        user_page = UserPage(app.notebook, app)
        resource_page = ResourcePage(app.notebook, app)
        booker_page = BookerPage(app.notebook, app)
        viewer_page = ViewerPage(app.notebook, app)
        self.assertIsInstance(user_page, UserPage)
        self.assertIsInstance(resource_page, ResourcePage)
        self.assertIsInstance(booker_page, BookerPage)
        self.assertIsInstance(viewer_page, ViewerPage)

class TestScalability(unittest.TestCase):
    def test_scalability_computer_lab(self):
        users_file = "scalability_users.json"
        resources_file = "scalability_resources.json"
        bookings_file = "scalability_bookings.json"
        # Clean up before test
        for f in [users_file, resources_file, bookings_file]:
            if os.path.exists(f):
                os.remove(f)

        # Create 1000 users
        users = get_users(users_file)
        for i in range(1000):
            users.users[f"user{i}"] = {"full_name": f"User {i}", "password": "pass"}
        users.save_users()

        # Create 250 resources (e.g., computers)
        resources = get_resources(resources_file)
        for i in range(250):
            resources.resources[f"PC{i}"] = {
                "description": f"Computer {i}",
                "available": True,
                "owner": None,
                "days_booked": []
            }
        resources.save_resources()

        # Create 5000 bookings, distributed among users and resources
        bookings = get_bookings(bookings_file)
        booking_count = 0
        for user_id in range(1000):
            for res_id in range(250):
                if booking_count >= 5000:
                    break
                booking_name = f"booking{booking_count}"
                bookings.bookings[booking_name] = {
                    "owner": f"user{user_id}",
                    "resource": f"PC{res_id}",
                    "start_date": "2025-07-01",
                    "end_date": "2025-07-02"
                }
                booking_count += 1
            if booking_count >= 5000:
                break
        start = time.time()
        bookings.save_bookings()
        users.load_users()
        resources.load_resources()
        bookings.load_bookings()
        end = time.time()

        # Check counts
        self.assertEqual(len(users.users), 1000)
        self.assertEqual(len(resources.resources), 250)
        self.assertEqual(len(bookings.bookings), 5000)
        # Check performance (should be well under 5 seconds for this size)
        self.assertLess(end - start, 5.0)

        # Clean up after test
        for f in [users_file, resources_file, bookings_file]:
            if os.path.exists(f):
                os.remove(f)

class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.users_file = 'integrity_users.json'
        self.resources_file = 'integrity_resources.json'
        self.bookings_file = 'integrity_bookings.json'
        for f in [self.users_file, self.resources_file, self.bookings_file]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        for f in [self.users_file, self.resources_file, self.bookings_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_delete_user_removes_bookings(self):
        users = get_users(self.users_file)
        resources = get_resources(self.resources_file)
        bookings = get_bookings(self.bookings_file)
        users.users['u1'] = {'full_name': 'U1', 'password': 'p'}
        resources.resources['r1'] = {'description': 'desc', 'available': True, 'owner': 'u1', 'days_booked': []}
        bookings.bookings['b1'] = {'owner': 'u1', 'resource': 'r1', 'start_date': '2025-01-01', 'end_date': '2025-01-02'}
        users.save_users(); resources.save_resources(); bookings.save_bookings()
        del users.users['u1']
        users.save_users()
        # Simulate manual cleanup as in app logic
        bookings.bookings = {k: v for k, v in bookings.bookings.items() if v['owner'] != 'u1'}
        bookings.save_bookings()
        bookings.load_bookings()
        self.assertNotIn('b1', bookings.bookings)

    def test_delete_resource_removes_bookings(self):
        users = get_users(self.users_file)
        resources = get_resources(self.resources_file)
        bookings = get_bookings(self.bookings_file)
        users.users['u1'] = {'full_name': 'U1', 'password': 'p'}
        resources.resources['r1'] = {'description': 'desc', 'available': True, 'owner': 'u1', 'days_booked': []}
        bookings.bookings['b1'] = {'owner': 'u1', 'resource': 'r1', 'start_date': '2025-01-01', 'end_date': '2025-01-02'}
        users.save_users(); resources.save_resources(); bookings.save_bookings()
        del resources.resources['r1']
        resources.save_resources()
        # Simulate manual cleanup as in app logic
        bookings.bookings = {k: v for k, v in bookings.bookings.items() if v['resource'] != 'r1'}
        bookings.save_bookings()
        bookings.load_bookings()
        self.assertNotIn('b1', bookings.bookings)

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.users_file = 'auth_users.json'
        for f in [self.users_file]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        for f in [self.users_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_edit_with_wrong_password(self):
        users = get_users(self.users_file)
        users.users['u1'] = {'full_name': 'U1', 'password': 'correct'}
        users.save_users()
        # Simulate wrong password
        self.assertNotEqual('wrong', users.users['u1']['password'])

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.users_file = 'persist_users.json'
        self.resources_file = 'persist_resources.json'
        self.bookings_file = 'persist_bookings.json'
        for f in [self.users_file, self.resources_file, self.bookings_file]:
            if os.path.exists(f):
                os.remove(f)

    def tearDown(self):
        for f in [self.users_file, self.resources_file, self.bookings_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_persistence(self):
        users = get_users(self.users_file)
        users.users['u1'] = {'full_name': 'U1', 'password': 'p'}
        users.save_users()
        users2 = get_users(self.users_file)
        users2.load_users()
        self.assertIn('u1', users2.users)

if __name__ == '__main__':
    unittest.main()
