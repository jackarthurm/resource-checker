import logging

from resource_checker.model.resource import HTMLWebResource
from resource_checker.model.rules import HTMLContainsTextRule, RuleIntersect


if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)

    # The following illustrates the motivation for this project!

    switch_dock_resource: HTMLWebResource = HTMLWebResource(
        'Switch dock stock check',
        'https://store.nintendo.co.uk/nintendo-switch-accessory/nintendo-switch-dock-set/11'
        '469708.html',
        RuleIntersect(
            HTMLContainsTextRule('Sorry, this product is currently out of stock.'),
            HTMLContainsTextRule('Out of Stock')
        ).negated()
    )

    print(
        'Switch dock kit is '
        f'{ "back in" if switch_dock_resource.check() else "still out of"}'
        ' stock'
    )
