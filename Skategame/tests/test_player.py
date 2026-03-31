import pytest
from game.player import Player


def test_create_valid_player():
    player = Player(1, "Alex")

    assert player.id == 1
    assert player.name == "Alex"
    assert player.score == 0
    assert player.status == "active"


def test_receive_letters_increases_score():
    player = Player(1, "Alex")

    player.receive_letters()

    assert player.score == 1


def test_eliminate_changes_status_to_eliminated():
    player = Player(1, "Alex")

    player.eliminate()

    assert player.status == "eliminated"


def test_eliminated_player_cannot_receive_letters():
    player = Player(1, "Alex")
    player.eliminate()

    with pytest.raises(ValueError):
        player.receive_letters()