from typing import Dict, NewType, Union, NamedTuple

Passport = NewType("Passport", str)  # an encoded list of visas
Permission = NewType("Permission", dict)
Visa = NewType("Visa", Dict[str, Union[str, int, None]])


class Config(NamedTuple):
    """The app configuration."""

    rems_url: str
    repository: str
    jwt_exp: int
    public_key: dict
    private_key: dict
    host: str = "0.0.0.0"
    port: Union[int, str] = 8080
