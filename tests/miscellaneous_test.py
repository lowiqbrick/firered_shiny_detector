import utils


def test_period_to_string_length():
    assert len(utils.period_to_str(12.12)) == 5
    assert len(utils.period_to_str(12.1)) == 5
    assert len(utils.period_to_str(12)) == 5
