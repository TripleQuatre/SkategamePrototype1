import pytest
from game.turn import Turn
from game.player import Player


def create_players():
    attacker = Player(1, "Attacker")
    defender = Player(2, "Defender")
    return attacker, [defender]


def test_create_valid_turn():
    attacker, defenders = create_players()

    turn = Turn(attacker, defenders, "kickflip", 2)

    assert turn.attacker == attacker
    assert turn.defenders == defenders
    assert turn.trick == "kickflip"
    assert turn.turn_state == "defense_pending"


def test_use_defense_attempt_decreases_attempts():
    attacker, defenders = create_players()
    turn = Turn(attacker, defenders, "kickflip", 2)

    defender = defenders[0]

    turn.use_defense_attempt(defender)

    assert turn.defense_attempts_left[defender] == 1


def test_use_defense_attempt_raises_error_if_no_attempts_left():
    attacker, defenders = create_players()
    turn = Turn(attacker, defenders, "kickflip", 1)

    defender = defenders[0]

    turn.use_defense_attempt(defender)

    with pytest.raises(ValueError):
        turn.use_defense_attempt(defender)


def test_set_defense_success_records_result():
    attacker, defenders = create_players()
    turn = Turn(attacker, defenders, "kickflip", 2)

    defender = defenders[0]

    turn.set_defense_success(defender)

    assert turn.defense_results[defender] == "success"


def test_set_defense_failure_records_result():
    attacker, defenders = create_players()
    turn = Turn(attacker, defenders, "kickflip", 2)

    defender = defenders[0]

    turn.set_defense_failure(defender)

    assert turn.defense_results[defender] == "failure"


def test_turn_is_finished_when_all_defenders_have_results():
    attacker, defenders = create_players()
    turn = Turn(attacker, defenders, "kickflip", 2)

    defender = defenders[0]

    turn.set_defense_success(defender)

    assert turn.turn_state == "finished"
    assert turn.is_finished() is True