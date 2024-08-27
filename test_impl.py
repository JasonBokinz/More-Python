import unittest
import impl

class TestPhysicalInfo(unittest.TestCase):

    def test_valid_name(self):
        valid_names = ["Jo", "J1" "John123", "J123", "jay", " Jay", "-Jay", "123Jason"]
        space = ["John Smith", "Jo ", "J1 "]
        dash = ["John-Smith", "Jo-", "J1-"]
        more = ["Test-123 abc", "Hello World", "abc-123", "word-123-", "--a---"]
        valid_names.extend(space)
        valid_names.extend(dash)
        valid_names.extend(more)
        for name in valid_names:
            with self.subTest(name=name):
                info = impl.PhysicalInfo()
                self.assertEqual(None, info.set_name(name))

    def test_invalid_name(self):
        invalid_names = ["J", "j", "12", "-----", "J$", "*", "Jason*", 2, 2.0, 'c', "", " ", 1]
        more = ["!@#$", None, "ab@cd ef", "_", "+", ]
        invalid_names.extend(more)
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    info = impl.PhysicalInfo()
                    info.set_name(name)

    def test_valid_gender(self):
        valid_genders = ["M", "F"]
        for gender in valid_genders:
            with self.subTest(gender=gender):
                info = impl.PhysicalInfo()
                self.assertEqual(None, info.set_gender(gender))

    def test_invalid_gender(self):
        invalid_genders = ["m", "f", "MM", "FF", 1, 2.0, "John", "", 'm', " ", "1", "-", " M", " F", None]
        for gender in invalid_genders:
            with self.subTest(gender=gender):
                with self.assertRaises(ValueError):
                    info = impl.PhysicalInfo()
                    info.set_gender(gender)

    def test_valid_height(self):
        for height in range(17, 85):
            with self.subTest(height=height):
                info = impl.PhysicalInfo()
                self.assertEqual(None, info.set_height(height))

    def test_invalid_height(self):
        invalid_heights = [16, 85, 15.0, -15, -85 -17, -84, -50, 17.0, 84.0, 50.0, "string", 'c', None]
        for height in invalid_heights:
            with self.subTest(height=height):
                with self.assertRaises(ValueError):
                    info = impl.PhysicalInfo()
                    info.set_height(height)

    def test_valid_temperature(self):
        valid_temps = [95.0, 98.6, 100.23, 104.0, 101.243]
        for temp in valid_temps:
            with self.subTest(temp=temp):
                info = impl.PhysicalInfo()
                self.assertEqual(None, info.set_temperature(temp))

    def test_invalid_temperature(self):
        invalid_temps = [94.9, 104.1, "string", 'c', 94, 95, 104, 100, 105, -94.0, -104,1, -94, -95, -104, -100, None]
        for temp in invalid_temps:
            with self.subTest(temp=temp):
                with self.assertRaises(ValueError):
                    info = impl.PhysicalInfo()
                    info.set_temperature(temp)

    def test_valid_date(self):
        valid_days = ["01-01-2023", "01-31-2023", "02-28-2023", "03-31-2023", "04-30-2023", "05-31-2023", "06-30-2023", "07-31-2023", "08-31-2023", "09-30-2023", "10-31-2023", "11-30-2023", "12-31-2023"]
        valid_dates = ["02-29-2020", "01-01-1900", "01-01-2100"]
        valid_dates.extend(valid_days)
        valid_dates.extend(["02-29-2024", "02-28-2024", "01-01-1900", "01-01-2100"])
        for date in valid_dates:
            with self.subTest(date=date):
                info = impl.PhysicalInfo()
                self.assertEqual(None, info.set_date(date))

    def test_invalid_date(self):
        invalid_days = ["02-30-2020", "02-30-1900", "02-30-2022", "01-00-2023", "01--2023", "01-1-2023", "01-32-2023", "02-30-2023", "03-32-2023", "04-31-2023", "05-32-2023", "06-31-2023", "07-32-2023", "08-32-2023", "09-31-2023", "10-32-2023", "11-31-2023", "12-32-2023"]
        invalid_months = ["00-01-2023", "1-01-2023", "13-01-2023", "111-11-2023", 0, 1.0, 'c', None]
        invalid_year = ["01-01-", "01-01-1", "01-01-22", "01-01-233", "01-01-1899", "01-01-2101"]
        invalid_dates = ["02-29-2001", "02-29-1900", "02-30-2022", "01-00-2023", "01--2023", "01-1-2023", "01-32-2023", "02-30-2023", "03-32-2023", "04-31-2023", "05-32-2023", "06-31-2023", "07-32-2023", "08-32-2023", "09-31-2023", "10-32-2023", "11-31-2023", "12-32-2023"]
        invalid_dates.extend(invalid_days)
        invalid_dates.extend(invalid_months)
        invalid_dates.extend(invalid_year)
        for date in invalid_dates:
            with self.subTest(date=date):
                with self.assertRaises(ValueError):
                    info = impl.PhysicalInfo()
                    info.set_date(date)

if __name__ == '__main__':
    unittest.main()