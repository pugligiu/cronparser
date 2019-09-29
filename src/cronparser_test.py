import unittest
from unittest import mock
import cronparser


class CronParserTestCorrectString(unittest.TestCase):
    '''
    Test suite for the class CronParser in case of correct input
    '''

    def setUp(self):
        self.parser1 = cronparser.CronParser("*/15 0 1,15 1-12 0-6 /usr/bin/find")
        self.parser2 = cronparser.CronParser("*/15 0 1,15 JAN-DEC SUN-SAT /usr/bin/find")
        self.parser3 = cronparser.CronParser("*/15 0 1,15 2/3 3/2 /usr/bin/find")
        self.parser4 = cronparser.CronParser("*/15 0 1,15 FEB/3 WED/2 /usr/bin/find")
        self.parser5 = cronparser.CronParser("2/5 0 1,15 MAR,APR,MAY MON,TUE,THU,FRI /usr/bin/find")
        self.parser6 = cronparser.CronParser("2 3-10 2/22 JUN,JUL,AUG,SEP,OCT,NOV * /usr/bin/find")

    def tearDown(self):
        del self.parser1
        del self.parser2
        del self.parser3
        del self.parser4
        del self.parser5
        del self.parser6

    def test_get_minutes(self):

        res = self.parser1.get_minutes()
        self.assertEqual(res, ("MINUTE", [0, 15, 30, 45]))

        res = self.parser5.get_minutes()
        self.assertEqual(res, ("MINUTE", [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57]))

        res = self.parser6.get_minutes()
        self.assertEqual(res, ("MINUTE", [2]))

    def test_get_hours(self):

        res = self.parser1.get_hours()
        self.assertEqual(res, ("HOUR", [0]))

        res = self.parser6.get_hours()
        self.assertEqual(res, ("HOUR", [3, 4, 5, 6, 7, 8, 9, 10]))

    def test_get_month_days(self):

        res = self.parser1.get_month_days()
        self.assertEqual(res, ("DAY OF MONTH", [1, 15]))

        res = self.parser6.get_month_days()
        self.assertEqual(res, ("DAY OF MONTH", [2, 24]))

    def test_get_months(self):

        res = self.parser1.get_months()
        self.assertEqual(res, ("MONTH", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))

        res = self.parser2.get_months()
        self.assertEqual(res, ("MONTH", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))

        res = self.parser3.get_months()
        self.assertEqual(res, ("MONTH", [2, 5, 8, 11]))

        res = self.parser4.get_months()
        self.assertEqual(res, ("MONTH", [2, 5, 8, 11]))

        res = self.parser5.get_months()
        self.assertEqual(res, ("MONTH", [3, 4, 5]))

        res = self.parser6.get_months()
        self.assertEqual(res, ("MONTH", [6, 7, 8, 9, 10, 11]))

    def test_get_week_days(self):

        res = self.parser1.get_week_days()
        self.assertEqual(res, ("DAY OF WEEK", [0, 1, 2, 3, 4, 5, 6]))

        res = self.parser2.get_week_days()
        self.assertEqual(res, ("DAY OF WEEK", [0, 1, 2, 3, 4, 5, 6]))

        res = self.parser3.get_week_days()
        self.assertEqual(res, ("DAY OF WEEK", [3, 5]))

        res = self.parser4.get_week_days()
        self.assertEqual(res, ("DAY OF WEEK", [3, 5]))

        res = self.parser5.get_week_days()
        self.assertEqual(res, ("DAY OF WEEK", [1, 2, 4, 5]))

        res = self.parser2.get_week_days()
        self.assertEqual(res, ("DAY OF WEEK", [0, 1, 2, 3, 4, 5, 6]))

    def test_get_command(self):

        res = self.parser1.get_command()
        self.assertEqual(res, ("COMMAND", "/usr/bin/find"))

    def test_print_cron_table(self):

        with mock.patch('sys.stdout') as fake_stdout:
            self.parser6.print_cron_table()

            fake_stdout.assert_has_calls([

                mock.call.write("minute        2"),
                mock.call.write("\n"),
                mock.call.write("hour          3 4 5 6 7 8 9 10"),
                mock.call.write("\n"),
                mock.call.write("day of month  2 24"),
                mock.call.write("\n"),
                mock.call.write("month         6 7 8 9 10 11"),
                mock.call.write("\n"),
                mock.call.write("day of week   0 1 2 3 4 5 6"),
                mock.call.write("\n"),
                mock.call.write("command       /usr/bin/find"),
                mock.call.write("\n")
            ])


class CronParserTestIncorrectString(unittest.TestCase):
    '''
    Test suite for the class CronParser in case of incorrect input

    Note: the coverage is not completed
    '''

    def setUp(self):
        self.parser1 = cronparser.CronParser("1-2-3 0-0 -1, 13 AUG,7 /usr/bin/find")
        self.parser2 = cronparser.CronParser("1/2/3 24 32/1 JAN,MON 0,1,2,3,4,5,6,7 /usr/bin/find")

    def tearDown(self):
        del self.parser1
        del self.parser2

    def test_get_minutes(self):

        with self.assertRaisesRegex(ValueError, "Error in minute field: the value has to be like: 1/2 or"):
            self.parser1.get_minutes()

        with self.assertRaisesRegex(ValueError, "Error in minute field: the value has to be like: 1/2 or"):
            self.parser2.get_minutes()

    def test_get_hours(self):

        with self.assertRaisesRegex(ValueError, "Error in hour field: the second value in the interval has to be bigger than first one"):
            self.parser1.get_hours()

        with self.assertRaisesRegex(ValueError, "Error in hour field: the value has to be in the interval"):
            self.parser2.get_hours()

    def test_get_month_days(self):

        with self.assertRaisesRegex(ValueError, "Error in day of month field: the value has to be integer or correct string name"):
            self.parser1.get_month_days()

        with self.assertRaisesRegex(ValueError, "Error in day of month field: the value has to be in the interval"):
            self.parser2.get_month_days()

    def test_get_months(self):

        with self.assertRaisesRegex(ValueError, "Error in month field: the value has to be in the interval"):
            self.parser1.get_months()

        with self.assertRaisesRegex(ValueError, "Error in month field: the value has a string not known"):
            self.parser2.get_months()

    def test_get_week_days(self):

        with self.assertRaisesRegex(ValueError, "Error in day of week field: not valid value"):
            self.parser1.get_week_days()

        with self.assertRaisesRegex(ValueError, "Error in day of week field: the value has to be like: 1/2 or"):
            self.parser2.get_week_days()

    def test_new_parser(self):
        with self.assertRaisesRegex(ValueError, "The permitted special chars are"):
            cronparser.CronParser("1&-2-3 0-0 -1, 13 AUG,7 /usr/bin/find")
