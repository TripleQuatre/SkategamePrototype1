import pytest
from game.settings import Settings


def test_create_valid_settings():
    settings = Settings("SKATE", 1, 2)

    assert settings.word == "SKATE"
    assert settings.max_attempts_attack == 1
    assert settings.max_attempts_defense == 2


def test_raise_error_if_word_is_empty():
    with pytest.raises(ValueError):
        Settings("", 1, 2)


def test_raise_error_if_word_is_too_long():
    with pytest.raises(ValueError):
        Settings("ABCDEFGHIJK", 1, 2)


def test_raise_error_if_attack_attempts_is_not_one():
    with pytest.raises(ValueError):
        Settings("SKATE", 2, 2)


def test_raise_error_if_defense_attempts_is_less_than_one():
    with pytest.raises(ValueError):
        Settings("SKATE", 1, 0)


def test_raise_error_if_defense_attempts_is_greater_than_three():
    with pytest.raises(ValueError):
        Settings("SKATE", 1, 4)