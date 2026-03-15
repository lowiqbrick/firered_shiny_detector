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


def show_pixel_in_image(
    image: cv2.typing.MatLike, pixel: utils.Point, *args: int
) -> cv2.typing.MatLike:
    grid = 0
    for arg in args:
        grid = arg

    height, width = image.shape[:2]

    # get pixel
    assert pixel.x <= width
    assert pixel.y <= height
    channel1, channel2, channel3 = (
        image[pixel.y][pixel.x][0],
        image[pixel.y][pixel.x][1],
        image[pixel.y][pixel.x][2],
    )

    for height_index in range(0, height):
        for width_index in range(0, width):
            if height_index == pixel.y or width_index == pixel.x:
                image[height_index][width_index][0] = 255
                image[height_index][width_index][1] = 255
                image[height_index][width_index][2] = 255
            elif (
                # grid enabled
                grid != 0
                # not at the left or top of the image
                and (height_index != 0 and width_index != 0)
                # condition for the grid
                and ((height_index % grid) == 0 or (width_index % grid) == 0)
            ):
                image[height_index][width_index][0] = 122
                image[height_index][width_index][1] = 122
                image[height_index][width_index][2] = 122
            else:
                image[height_index][width_index][0] = (
                    image[height_index][width_index][0] / 2 + channel1 / 2
                )
                image[height_index][width_index][1] = (
                    image[height_index][width_index][1] / 2 + channel2 / 2
                )
                image[height_index][width_index][2] = (
                    image[height_index][width_index][2] / 2 + channel3 / 2
                )

    return image


if __name__ == "__main__":
    mewtwo_reference = cv2.imread("selected_references/fight_menue_reference.png")
    pixel_emphasised = show_pixel_in_image(mewtwo_reference, utils.Point(1400, 350), 50)
    cv2.imshow("pixel example", pixel_emphasised)
    cv2.waitKey(1)

    time.sleep(10)
    cv2.destroyAllWindows()
