import logging

from resource_checker.model.resource import HTMLWebResource, Resource
from resource_checker.model.rules import HTMLContainsTextRule, RuleIntersect


class SwitchDockResource(HTMLWebResource):

    def __init__(self) -> None:
        super(SwitchDockResource, self).__init__(
            'https://store.nintendo.co.uk/nintendo-switch-accessory/nintendo-switch-dock-set/11'
            '469708.html',
            RuleIntersect(
                HTMLContainsTextRule('Sorry, this product is currently out of stock.'),
                HTMLContainsTextRule('Out of Stock')
            ).negated()
        )


if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)

    # The following illustrates the motivation for this project!

    switch_dock: Resource = SwitchDockResource()
    print(
        'Switch dock kit is '
        f'{ "back in" if switch_dock.check() else "still out of"}'
        ' stock'
    )
