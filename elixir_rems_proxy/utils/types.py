from typing import Any, Dict, NewType, Union

Passport = NewType('Passport', str)  # an encoded list of visas
Permission = NewType('Permission', dict)
Visa = NewType('Visa', Dict[str, Union[str, int, None]])
