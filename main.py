import cv2
import utils
import time
import specific_pokemon


def main():
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

    # display captured images
    while True:
        start_time = time.time()
        # capture frame
        success, frame = cap.read()

        if not success:
            logger.add_printout("no frame")
            cv2.destroyAllWindows()
        else:
            logger.add_printout("got frame;")
            # display frame
            cv2.imshow("HDMI Video Capture", frame)
            cv2.waitKey(1)

            # search for pokemon
            if search_engine.is_mewtwo(frame):
                logger.add_printout(" mewtwo detected;")
                if search_engine.is_mewtwo_shiny(frame):
                    utils.save_shiny(frame)
                    # TODO add code that turns off the controller
                    logger.add_printout("shiny found omg !!!!11111eleven")
                    logger.print()
                    break
                else:
                    logger.add_printout(" mewtwo isn't shiny;")

        # fps calculation
        delta_time = time.time() - start_time
        # is delta time not zero
        if delta_time:
            fps_averager.insert_new_value(1 / delta_time)
            logger.add_printout(" fps: " + str(fps_averager.get_fps()) + ";")
        logger.print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nmanual intervention")
    finally:
        print("programm ended")
