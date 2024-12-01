# School schedule

An example django application that serves school schedule as API

# Running the app

To run the app:

    $ docker compose up

To generate the example data:

    $ docker compose exec web /bin/bash
    $ python manage.py shell < script/generate_test_data.py

To run the tests:

   $ docker compose -f docker-compose-test.yml run tests

# Some considerations

The test coverage is far from exhaustive. I hope, however that the app shows,
how we can create unittests thanks to dependency inversion and minimize
the need to use django client/real database to functional tests or unit
tests that interact with some layers.

There is no logic to clear cache.  It should be created in the future
endpoints that handle data creation.
