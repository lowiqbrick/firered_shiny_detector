import cv2
import copy
import time
import numpy as np

import utils
import specific_pokemon


def test_image_part_equal():
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    comp_area = utils.Rectangle(utils.Point(50, 50), utils.Point(400, 400))
    assert utils.is_image_part_equal(mewtwo_reference, mewtwo_reference, comp_area)


def test_image_part_equal_false():
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    mewtwo_reference_changed = copy.deepcopy(mewtwo_reference)
    mewtwo_reference_changed[100][100][0] = 255
    comp_area = utils.Rectangle(utils.Point(50, 50), utils.Point(400, 400))
    assert not utils.is_image_part_equal(
        mewtwo_reference, mewtwo_reference_changed, comp_area
    )


def test_is_mewtwo():
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    assert search_engine.is_mewtwo(mewtwo_reference)


def test_is_mewtwo_false():
    search_engine = specific_pokemon.PokemonSearchEngine()
    black_image = np.zeros((1020, 1980, 3))
    assert not search_engine.is_mewtwo(black_image)


def test_is_mewtwo_during_send_out():
    search_engine = specific_pokemon.PokemonSearchEngine()
    send_out_reference = cv2.imread("selected_references/send_out.png")
    assert send_out_reference is not None
    assert search_engine.is_mewtwo(send_out_reference)
    assert not search_engine.is_mewtwo_shiny(send_out_reference)


def test_is_mewtwo_shiny():
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    # the shiny function expects the pixel values to be different
    mewtwo_reference[350][1400][0] = 0
    assert search_engine.is_mewtwo_shiny(mewtwo_reference)


def test_is_mewtwo_shiny_false():  # 1400 350
    search_engine = specific_pokemon.PokemonSearchEngine()
    mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_reference is not None
    assert not search_engine.is_mewtwo_shiny(mewtwo_reference)


def test_is_pokemon_present():
    period_timer = utils.PeriodTime()
    period_timer.reset()
    assert period_timer.get_passed_time() < 0.01
    time.sleep(utils.TIME_FOR_SHINY - 0.25)
    assert not period_timer.is_pokemon_present()
    time.sleep(0.5)
    assert period_timer.is_pokemon_present()
