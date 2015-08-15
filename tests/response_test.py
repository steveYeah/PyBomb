from nose.tools import *
from pybomb import response


def setup():
    global mock_response, pybomb_response

    class MockResponse(object):
        def __init__(self):
            self.url = ''
            self.num_results = 1
            self.results = ['result']

        def json(self):
            return {
                'number_of_total_results': self.num_results,
                'results': self.results
            }

    mock_response = MockResponse()
    pybomb_response = response.create_response(mock_response)


def test_response_factory_should_return_response_object():
    assert isinstance(pybomb_response, response.Response)


def test_response_factory_response_object_should_have_correct_uri():
    assert pybomb_response.uri == mock_response.url


def test_response_factory_response_object_should_have_correct_num_results():
    assert pybomb_response.num_results == mock_response.num_results


def test_response_factory_response_object_results_should_be_list():
    assert isinstance(pybomb_response.results, list)


def test_response_factory_response_object_should_have_correct_results():
    assert pybomb_response.results[0] == mock_response.results[0]
