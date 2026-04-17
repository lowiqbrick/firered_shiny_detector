import cv2
import time
import datetime
from gpiozero import LED

import sms
import utils
import specific_pokemon


def main():
    # start controller pin
    controller = LED(21)

    # load all reference images
    search_engine = specific_pokemon.PokemonSearchEngine()

    # averaging pfs values
    fps_averager = utils.FPSAverager(60)

    # get video source (0: switch 2; 1: pc webcam)
    cap = cv2.VideoCapture(0)

    # status printer
    logger = utils.LoopReporter()

    # set limits for capture of switch 2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # sms notification (not mandatory)
    sender = sms.SMSSender()

    # keep time of the current period
    period_timer = utils.PeriodTime()

    # take an image every period
    period_imager = utils.PeriodImager()

    is_last_detected = False
    reset_counter = 0

    print("started at " + str(datetime.datetime.now()))

    # display captured images
    while True:
        is_detected = False
        start_time = time.time()
        # capture frame
        success, frame = cap.read()

        if not success:
            logger.add_printout("no frame")
            cv2.destroyAllWindows()
        else:
            logger.add_printout("got frame;")
            # display frame
            cv2.imshow("HDMI Video Capture", cv2.resize(src=frame, dsize=(1000, 500)))
            cv2.waitKey(1)

            logger.add_printout(" " + str(reset_counter) + " resets;")
            logger.add_printout(
                " "
                + utils.period_to_str(round(period_timer.get_passed_time(), 2))
                + "s period; "
            )

            is_detected = search_engine.is_mewtwo(frame)
            period_timer.preemptive_check(is_detected, is_last_detected)
            if period_timer.is_pokemon_present():
                period_imager.save_encounter(frame)

            # search for pokemon
            if is_detected or period_timer.is_pokemon_present():
                logger.add_printout(" detection;")

                if search_engine.is_mewtwo_shiny(frame):
                    utils.save_shiny(frame)
                    # turn off the controller
                    controller.on()
                    logger.add_printout("shiny found omg !!!!11111eleven")
                    print(logger.print(), end="")
                    date_time = str(datetime.datetime.now())
                    # notify me
                    try:
                        sender.send("shiny suspected at " + str(date_time))
                    except ConnectionError:
                        print("\nfailed to send message")
                    finally:
                        break
                else:
                    logger.add_printout(" not shiny;")

        # fps calculation
        delta_time = time.time() - start_time
        if delta_time:
            fps_averager.insert_new_value(1 / delta_time)
            logger.add_printout("fps: " + str(fps_averager.get_fps()) + ";")
        print(logger.print(), end="")

        # take sample images
        period_imager.take_image(period_timer.get_passed_time(), frame)

        # update for next period
        if not is_detected and is_last_detected:
            reset_counter += 1
            period_timer.reset()
            period_imager.reset(reset_counter)

        is_last_detected = is_detected


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nmanual intervention")
    finally:
        print("\nprogram ended")
