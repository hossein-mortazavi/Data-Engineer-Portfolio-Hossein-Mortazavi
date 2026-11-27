"""Exception hierarchy used across projects.

The split matters operationally: ``TransientError`` is the only category a retry
policy should act on by default, while ``DataValidationError`` signals bad data that
must be quarantined rather than retried.
"""


class PortfolioError(Exception):
    """Base class for all errors raised deliberately by this repository."""


class ConfigurationError(PortfolioError):
    """Required configuration is missing or malformed."""


class TransientError(PortfolioError):
    """A failure that is expected to succeed if the operation is repeated."""


class DataValidationError(PortfolioError):
    """Input data violates a declared contract; retrying will not help."""
