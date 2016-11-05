def pytest_addoption(parser):
    parser.addoption('--repeat', default=1, type='int', metavar='repeat',
                     help='Repeat each test specified number of times')


def pytest_generate_tests(metafunc):
    for i in range(1, metafunc.config.option.repeat + 1):
        metafunc.addcall()
