import cv2
import time
import datetime
from gpiozero import LED

import utils


def main():
    # start controller pin
    controller = LED(21)

    # get video source (0: switch 2; 1: pc webcam)
    cap = cv2.VideoCapture(0)

    # set limits for capture of switch 2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    loop_structs = utils.LoopStructs()
    loop_variables = utils.LoopVariables()

    print("started at " + str(datetime.datetime.now()))

    # display captured images
    while True:
        is_detected = False
        start_time = time.time()
        # capture frame
        success, frame = cap.read()

        if not success:
            loop_structs.logger.add_printout("no frame")
            cv2.destroyAllWindows()
        else:
            loop_structs.logger.add_printout("got frame;")
            # display frame
            cv2.imshow("HDMI Video Capture", cv2.resize(src=frame, dsize=(1000, 500)))
            cv2.waitKey(1)

            loop_structs.logger.add_printout(
                " " + str(loop_variables.reset_counter) + " resets;"
            )
            loop_structs.logger.add_printout(
                " "
                + utils.period_to_str(
                    round(loop_structs.period_timer.get_passed_time(), 2)
                )
                + "s period;"
            )

            is_detected = loop_structs.search_engine.is_mewtwo_normal(frame)
            if is_detected:
                loop_structs.logger.add_printout(" mewtwo detected;")
            else:
                loop_structs.logger.add_printout(" mewtwo not detected;")

            loop_structs.period_timer.preemptive_check(
                is_detected, loop_variables.is_last_detected
            )
            if loop_structs.period_timer.is_pokemon_present():
                loop_structs.period_imager.save_encounter(frame)

            if not is_detected and loop_structs.period_timer.get_passed_time() >= 18.0:
                utils.save_shiny(frame)
                # turn off the controller
                controller.on()
                loop_structs.logger.add_printout("shiny found omg !!!!11111eleven")
                print(loop_structs.logger.print(), end="")
                date_time = str(datetime.datetime.now())
                # notify me
                try:
                    loop_structs.sender.send("shiny suspected at " + str(date_time))
                except ConnectionError:
                    print("\nfailed to send message")
                finally:
                    break

        # fps calculation
        delta_time = time.time() - start_time
        if delta_time:
            loop_structs.fps_averager.insert_new_value(1 / delta_time)
            loop_structs.logger.add_printout(
                " fps: " + str(loop_structs.fps_averager.get_fps()) + ";"
            )
        print(loop_structs.logger.print(), end="")

        # take sample images
        loop_structs.period_imager.take_image(
            loop_structs.period_timer.get_passed_time(), frame
        )

        # update for next period
        if not is_detected and loop_variables.is_last_detected:
            loop_variables.reset_counter += 1
            loop_structs.period_timer.reset()
            loop_structs.period_imager.reset(loop_variables.reset_counter)
            if loop_variables.last_image is not None:
                loop_structs.period_imager.save_encounter(loop_variables.last_image)

        loop_variables.is_last_detected = is_detected
        if frame is not None:
            loop_variables.last_image = frame


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nmanual intervention")
    finally:
        print("\nprogram ended")
