import requests


class Request(object):

    @staticmethod
    def request(mode, url, headers, params=None):
        """

        :param mode: RESTful request object method call
        :param url: To call api
        :param headers: requests headers
        :param params: requests parameters
        :return: requests Response object
        """

        options = {
            'get': requests.get,
            'put': requests.put,
            'post': requests.post,
            'delete': requests.delete
            }
        return options[mode](url, params=params, headers=headers)

    @staticmethod
    def extract(headers, params, req):
        """
            Recursive partner of the request method. Extracts paginated json data from passed request Response
        :param headers: Inherited from and passed to originating request
        :param params: Inherited from and passed to originating request
        :param req: requests Response object
        :return: list of extracted json data
        """

        content = req.json()
        if not isinstance(content, list):
            content = [content]

        if req.links['current']['url'] == req.links['last']['url']:
            return content

        mode = req.request.method.lower()
        next_url = req.links['next']['url']
        req = Request.request(mode, next_url, headers, params)
        content += Request.extract(headers, params, req)
        return content


