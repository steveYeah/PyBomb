from nose.tools import *
from pybomb import response


def setup():
    global mock_response, pybomb_response

    class MockResponse(object):
        def __init__(self):
            self.url = ''
            self.num_total_results = 1
            self.num_page_results = 1
            self.results = ['result']

        def json(self):
            return {
                'number_of_total_results': self.num_total_results,
                'number_of_page_results': self.num_page_results,
                'results': self.results
            }

    mock_response = MockResponse()
    pybomb_response = response.create_response(mock_response)


def test_response_factory_should_return_response_object():
    """
    When the response factory is used correctly then it should return a pybomb.response.Response
    """
    assert isinstance(pybomb_response, response.Response)


def test_response_factory_response_object_should_have_correct_uri():
    """
    When the response factory is used correctly the pybomb.response.Response will have the correct
    uri
    """
    assert pybomb_response.uri == mock_response.url


def test_response_factory_response_object_should_have_correct_num_total_results():
    """
    When the response factory is used correctly the pybomb.response.Response will have the correct
    total number of results
    """
    assert pybomb_response.num_total_results == mock_response.num_total_results


def test_response_factory_response_object_should_have_correct_num_page_results():
    """
    When the response factory is used correctly the pybomb.response.Response will have the correct
    number of page results
    """
    assert pybomb_response.num_page_results == mock_response.num_page_results


def test_response_factory_response_object_results_should_be_list():
    """
    When the response factory is used correctly the pybomb.response.Response will have a list of
    results
    """
    assert isinstance(pybomb_response.results, list)


def test_response_factory_response_object_should_have_correct_results():
    """
    When the response factory is used correctly the pybomb.response.Response will have the correct
    result items
    """
    assert pybomb_response.results[0] == mock_response.results[0]
