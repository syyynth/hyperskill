import os

from hstest import FlaskTest, dynamic_test, WrongAnswer

from .base import (
    test_correct_request,
    test_bad_request,
    test_get_events,
    test_today_events,
    check_events_in_range,
    check_get_delete_by_id
)


class ServerTest(FlaskTest):
    source = 'app'

    funcs = [
        test_correct_request,
        test_bad_request,
        test_get_events,
        test_today_events,
        check_events_in_range,
        check_get_delete_by_id
    ]

    def generate(self):
        if os.path.exists('event.db'):
            try:
                os.remove('event.db')
            except Exception:
                raise WrongAnswer("Can't delete the database file before starting the tests!")
        return []

    @dynamic_test(data=funcs)
    def test_correct_request(self, func):
        return func(self)


if __name__ == '__main__':
    ServerTest().run_tests()
