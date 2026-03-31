import pytest
from game.game import Game
from game.player import Player
from game.settings import Settings


def create_game():
    p1 = Player(1, "A")
    p2 = Player(2, "B")
    settings = Settings("SKATE", 1, 2)
    return Game([p1, p2], settings), p1, p2


def test_create_valid_game():
    game, p1, p2 = create_game()

    assert len(game.players) == 2
    assert game.settings is not None
    assert game.is_started is False


def test_start_game_sets_first_turn():
    game, p1, p2 = create_game()

    game.start(p1, [p2], "kickflip")

    assert game.is_started is True
    assert game.current_turn is not None
    assert game.current_turn.attacker == p1
    assert game.current_turn.defenders == [p2]
    assert game.current_turn.trick == "kickflip"


def test_cannot_start_game_twice():
    game, p1, p2 = create_game()

    game.start(p1, [p2], "kickflip")

    with pytest.raises(ValueError):
        game.start(p1, [p2], "kickflip")

def test_start_raises_error_if_first_attacker_is_not_in_game():
    game, p1, p2 = create_game()
    outsider = Player(99, "Outsider")

    with pytest.raises(ValueError):
        game.start(outsider, [p2], "kickflip")


def test_start_raises_error_if_defenders_are_not_correct():
    game, p1, p2 = create_game()

    with pytest.raises(ValueError):
        game.start(p1, [], "kickflip")


def test_create_turn_raises_error_if_game_not_started():
    game, p1, p2 = create_game()

    with pytest.raises(ValueError):
        game.create_turn(p1, [p2], "kickflip")


def test_create_turn_raises_error_if_a_turn_is_already_in_progress():
    game, p1, p2 = create_game()
    game.start(p1, [p2], "kickflip")

    with pytest.raises(ValueError):
        game.create_turn(p2, [p1], "heelflip")

def test_finish_current_turn_raises_error_if_turn_is_not_finished():
    game, p1, p2 = create_game()
    game.start(p1, [p2], "kickflip")

    with pytest.raises(ValueError):
        game.finish_current_turn()


def test_finish_current_turn_gives_letter_to_failed_defender():
    game, p1, p2 = create_game()
    game.start(p1, [p2], "kickflip")

    game.current_turn.set_defense_failure(p2)
    game.finish_current_turn()

    assert p2.score == 1


def test_finish_current_turn_adds_turn_to_history():
    game, p1, p2 = create_game()
    game.start(p1, [p2], "kickflip")

    finished_turn = game.current_turn
    game.current_turn.set_defense_failure(p2)
    game.finish_current_turn()

    assert finished_turn in game.turn_history
    assert game.current_turn is None


def test_finish_current_turn_eliminates_player_when_score_reaches_word_length():
    game, p1, p2 = create_game()

    p2.score = 4
    game.start(p1, [p2], "kickflip")

    game.current_turn.set_defense_failure(p2)
    game.finish_current_turn()

    assert p2.score == 5
    assert p2.status == "eliminated"

def test_check_winner_returns_none_when_more_than_one_player_is_active():
    game, p1, p2 = create_game()

    winner = game.check_winner()

    assert winner is None


def test_check_winner_returns_winner_when_only_one_player_is_active():
    game, p1, p2 = create_game()
    p2.eliminate()

    winner = game.check_winner()

    assert winner == p1
    assert game.winner == p1
    assert game.is_finished is True


def test_get_next_attacker_returns_other_player_in_1v1():
    game, p1, p2 = create_game()

    next_attacker = game.get_next_attacker(p1)

    assert next_attacker == p2


def test_prepare_next_turn_creates_new_turn_with_next_attacker():
    game, p1, p2 = create_game()
    game.start(p1, [p2], "kickflip")

    game.current_turn.set_defense_failure(p2)
    game.finish_current_turn()

    next_attacker = game.get_next_attacker(p1)
    game.prepare_next_turn(next_attacker, "heelflip")

    assert game.current_turn is not None
    assert game.current_turn.attacker == p2
    assert game.current_turn.defenders == [p1]
    assert game.current_turn.trick == "heelflip"


def test_prepare_next_turn_raises_error_if_game_is_finished():
    game, p1, p2 = create_game()
    p2.eliminate()
    game.check_winner()

    with pytest.raises(ValueError):
        game.prepare_next_turn(p1, "kickflip")