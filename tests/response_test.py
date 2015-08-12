from nose.tools import *
from pybomb.clients import response


def setup():
    global mock_response

    class MockResponse(object):
        def __init__(self):
            self.url = ''

        def json(self):
            return {
                'number_of_total_results': 1,
                'results': ['result']
            }

    mock_response = MockResponse()


def test_response_factory_should_return_response_object():
    pybomb_response = response.create_response(mock_response)

    assert isinstance(pybomb_response, response.Response)


def test_response_factory_response_object_should_have_correct_uri():
    pybomb_response = response.create_response(mock_response)

    assert pybomb_response.uri == mock_response.url


def test_response_factory_response_object_should_have_correct_num_results():
    pybomb_response = response.create_response(mock_response)

    assert pybomb_response.num_results == 1


def test_response_factory_response_object_results_should_be_list():
    pybomb_response = response.create_response(mock_response)

    assert isinstance(pybomb_response.results, list)


def test_response_factory_response_object_should_have_correct_results():
    pybomb_response = response.create_response(mock_response)

    assert pybomb_response.results[0] == 'result'
