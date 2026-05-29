import main
import utils
import pytest
import cv2
from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory
import time
import numpy as np

Device.pin_factory = MockFactory()


def regular_timing():
    return [17.5, 1.25]


def irregular_timing():
    return [18.5, 0.25]


def main_cycle(
    time_list: list[float],
    black_image: cv2.typing.MatLike,
    mewtwo_image: cv2.typing.MatLike,
    controller: LED,
    loop_structs: utils.LoopStructs,
    loop_variables: utils.LoopVariables,
):
    start_time = time.time()
    is_detected = main.image_processing(
        black_image, controller, loop_structs, loop_variables
    )
    main.loop_update(is_detected, start_time, black_image, loop_structs, loop_variables)
    time.sleep(time_list[0])

    start_time = time.time()
    is_detected = main.image_processing(
        mewtwo_image, controller, loop_structs, loop_variables
    )
    time.sleep(time_list[1])
    main.loop_update(
        is_detected, start_time, mewtwo_image, loop_structs, loop_variables
    )


def test_regular():
    mewtwo_image = cv2.imread("selected_references/mewtwo_reference.png")
    assert mewtwo_image is not None
    black_image = np.zeros((1080, 1920, 3))
    loop_structs = utils.LoopStructs()
    loop_variables = utils.LoopVariables()
    controller = LED(21)

    # get through startup process
    main_cycle(
        regular_timing(),
        black_image,
        mewtwo_image,
        controller,
        loop_structs,
        loop_variables,
    )

    for _ in range(0, 3):
        main_cycle(
            regular_timing(),
            black_image,
            mewtwo_image,
            controller,
            loop_structs,
            loop_variables,
        )

    assert loop_variables.period_length_last_loop == pytest.approx(
        expected=sum(regular_timing()), abs=0.02
    )

    # do one more black image to count the last for-loop iteration
    start_time = time.time()
    is_detected = main.image_processing(
        black_image, controller, loop_structs, loop_variables
    )
    main.loop_update(is_detected, start_time, black_image, loop_structs, loop_variables)

    assert loop_variables.reset_counter == 4


def test_fail_on_irregular():
    # expect an exception to be raised
    with pytest.raises(utils.NoNewMewtwoException):
        mewtwo_image = cv2.imread("selected_references/mewtwo_reference.png")
        assert mewtwo_image is not None
        black_image = np.zeros((1080, 1920, 3))
        loop_structs = utils.LoopStructs()
        loop_variables = utils.LoopVariables()
        controller = LED(21)

        # get through startup process
        main_cycle(
            regular_timing(),
            black_image,
            mewtwo_image,
            controller,
            loop_structs,
            loop_variables,
        )

        # one regular cycle
        main_cycle(
            regular_timing(),
            black_image,
            mewtwo_image,
            controller,
            loop_structs,
            loop_variables,
        )

        # give black image in timeout to simulate shiny
        main_cycle(
            irregular_timing(),
            black_image,
            black_image,
            controller,
            loop_structs,
            loop_variables,
        )


if __name__ == "__main__":
    pass
