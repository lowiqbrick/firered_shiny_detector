import cv2
import os
import utils
import time
import specific_pokemon

if __name__ == "__main__":
    # load all reference images
    search_engine = specific_pokemon.PokemonSearchEngine()

    # averaging pfs values
    fps_averager = utils.FPSAverager(60)

    # get video source (0: switch 2; 1: pc webcam)
    cap = cv2.VideoCapture(0)

    # set limits for capture of switch 2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # display captured images
    while True:
        start_time = time.time()
        printout = ""
        # capture frame
        success, frame = cap.read()

        if not success:
            printout += "video could not be read"
            cap.release()
            cv2.destroyAllWindows()
            break
        else:
            printout += "got frame;"
            # display frame
            cv2.imshow("HDMI Video Capture", frame)
            cv2.waitKey(1)

            # search for pokemon
            if search_engine.is_mewtwo(frame):
                printout += " mewtwo detected;"
                if search_engine.is_mewtwo_shiny(frame):
                    utils.save_shiny(frame)
                    # TODO add code that turns off the controller
                    printout += "shiny found omg !!!!11111eleven"
                    break
                else:
                    printout += " mewtwo isn't shiny;"

        # fps calculation
        fps_averager.insert_new_value(1 / (time.time() - start_time))
        printout += " fps: " + str(fps_averager.get_fps()) + ";"

        # print info on screen
        terminal_columns = os.get_terminal_size().columns
        if len(printout) > terminal_columns:
            printout = printout[:terminal_columns]
        elif len(printout) < terminal_columns:
            printout = printout + " " * (terminal_columns - len(printout))
        print(printout, end="\r")
