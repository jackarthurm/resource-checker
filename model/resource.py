from abc import ABC, abstractmethod
import logging
from typing import Any

import requests
from requests import Response

from model.exceptions import CheckResourceError, RetrieveResourceError
from model.rules import Rule


class Resource(ABC):

    def __init__(self, location: str, rule: Rule) -> None:
        self._location: str = location
        self._rule: Rule = rule

    @abstractmethod
    def retrieve_content(self) -> Any:
        pass

    def check(self) -> bool:

        try:
            content: Any = self.retrieve_content()
        except Exception:
            logging.warning(f'Error retrieving resource at location {self._location}')
            raise RetrieveResourceError

        try:
            success: bool = self._rule.check_content(content)
        except Exception:
            logging.warning(f'Error checking resource at location {self._location}')
            raise CheckResourceError

        return success


class TextResource(Resource):

    @abstractmethod
    def retrieve_content(self) -> str:
        pass


class HTMLWebResource(TextResource):

    def __init__(self, url: str, rule: Rule) -> None:
        super(HTMLWebResource, self).__init__(url, rule)

    def retrieve_content(self) -> str:
        response: Response = requests.get(
            self._location,
            headers=dict(
                Accept='application/html'
            )
        )
        response.raise_for_status()
        return response.text


class JSONWebResource(TextResource):

    def __init__(self, url: str, rule: Rule) -> None:
        super(JSONWebResource, self).__init__(url, rule)

    def retrieve_content(self) -> str:
        response: Response = requests.get(
            self._location,
            headers=dict(
                Accept='application/json'
            )
        )
        response.raise_for_status()
        return response.text
