import cv2
import time
import utils


def black_image_part(
    image: cv2.typing.MatLike, visible_area: utils.Rectangle
) -> cv2.typing.MatLike:
    """
    this function is for findung out,
    what rectangle values correspond to what area in the captured images
    and isn't used for anything more than debugging

    pokemon: approx. Rectangle(Point(1150, 80), Point(1550, 450))

    opponent status bar: approx. Rectangle(Point(300, 130), Point(840, 260))

    fight menue: approx. Rectangle(Point(975, 760), Point(1920, 1080))
    """
    height, width, _ = image.shape

    for height_index in range(0, height):
        for width_index in range(0, width):
            if visible_area.is_point_outside_rectangle(
                utils.Point(width_index, height_index)
            ):
                image[height_index][width_index][0] = 0
                image[height_index][width_index][1] = 0
                image[height_index][width_index][2] = 0

    return image


if __name__ == "__main__":
    mewtwo_reference = cv2.imread("selected_references/fight_menue_reference.png")
    blacked_image = black_image_part(
        mewtwo_reference[:][:][:],
        utils.Rectangle(utils.Point(1150, 80), utils.Point(1550, 450)),
    )
    cv2.imshow("black example", blacked_image)
    cv2.waitKey(1)

    time.sleep(5)
    cv2.destroyAllWindows()
