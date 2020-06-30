from abc import ABC, abstractmethod
from typing import Any, Set

from bs4 import BeautifulSoup


class Rule(ABC):

    def __init__(self) -> None:
        self._negated = False

    def check_content(self, content: Any) -> bool:
        return not self._negated and self._check_content(content)

    @abstractmethod
    def _check_content(self, content: Any) -> bool:
        pass

    def negated(self) -> 'Rule':
        self._negated = not self._negated
        return self


class RuleSet(Rule):

    def __init__(self, *rules: Rule) -> None:
        super(RuleSet, self).__init__()

        self._rules: Set[Rule] = set(rules)

    @abstractmethod
    def _check_content(self, content: Any) -> bool:
        pass


class RuleUnion(RuleSet):

    def _check_content(self, content: Any) -> bool:
        return all(
            rule.check_content(content) for rule in self._rules
        )


class RuleIntersect(RuleSet):

    def _check_content(self, content: Any) -> bool:
        return any(
            rule.check_content(content) for rule in self._rules
        )


class BasicContainsTextRule(Rule):

    def __init__(self, text: str) -> None:
        super(BasicContainsTextRule, self).__init__()

        self._text: str = text

    def _check_content(self, content: str) -> bool:
        return self._text in content


class HTMLContainsTextRule(Rule):

    def __init__(self, text: str) -> None:
        super(HTMLContainsTextRule, self).__init__()

        self._text: str = text

    def _check_content(self, content: str) -> bool:
        bs: BeautifulSoup = BeautifulSoup(content, 'lxml')
        return self._text in bs.text
