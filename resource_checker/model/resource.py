from abc import ABC, abstractmethod
import logging
from typing import Any, Optional

import requests
from requests import Response

from resource_checker.model.exceptions import CheckResourceError, RetrieveResourceError
from resource_checker.model.rules import Rule


class Resource(ABC):

    def __init__(
        self,
        name: str,
        location: str,
        rule: Rule,
        description: Optional[str] = None
    ) -> None:

        self._name: str = name
        self._description: str = description
        self._location: str = location
        self._rule: Rule = rule

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def location(self) -> str:
        return self._location

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

    def retrieve_content(self) -> str:
        response: Response = requests.get(
            self._location,
            headers=dict(
                Accept='application/json'
            )
        )
        response.raise_for_status()
        return response.text
