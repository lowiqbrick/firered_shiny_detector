import cv2
import time
import datetime


class Point:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, top_left: Point, bottom_right: Point):
        assert top_left.x < bottom_right.x
        assert top_left.y < bottom_right.y
        self.top_left = top_left
        self.bottom_right = bottom_right

    def is_point_in_rectangle(self, point: Point) -> bool:
        if (
            self.top_left.x <= point.x
            and self.top_left.y <= point.y
            and self.bottom_right.x > point.x
            and self.bottom_right.y > point.y
        ):
            return True
        False

    def is_point_outside_rectangle(self, point: Point) -> bool:
        return not self.is_point_in_rectangle(point)

    def opponent_stat_rec():
        # returns rectangle with the opponents status
        return Rectangle(Point(300, 130), Point(840, 260))

    def opponent_pokemon():
        # returns rectangle with the opponents pokemon sprite
        return Rectangle(Point(1150, 80), Point(1550, 450))


def is_image_part_equal(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
    comparison_area: Rectangle,
) -> bool:
    "compares part of two images specified in the comparison area on a pixel basis"
    for width_index in range(
        comparison_area.top_left.x,
        comparison_area.bottom_right.x,
    ):
        for height_index in range(
            comparison_area.top_left.y,
            comparison_area.bottom_right.y,
        ):
            if (
                reference_image[height_index][width_index][0]
                != captured_image[height_index][width_index][0]
                or reference_image[height_index][width_index][1]
                != captured_image[height_index][width_index][1]
                or reference_image[height_index][width_index][2]
                != captured_image[height_index][width_index][2]
            ):
                return False
    return True


def is_status_menue_equal(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
) -> bool:
    return is_image_part_equal(
        reference_image, captured_image, Rectangle.opponent_stat_rec()
    )


def is_pokemon_equal(
    reference_image: cv2.typing.MatLike,
    captured_image: cv2.typing.MatLike,
) -> bool:
    return is_image_part_equal(
        reference_image, captured_image, Rectangle.opponent_pokemon()
    )


def save_shiny(image: cv2.typing.MatLike):
    date_time = datetime.datetime.now()
    cv2.imwrite(
        "suspected_shiny_"
        + str(date_time.year)
        + "_"
        + str(date_time.month)
        + "_"
        + str(date_time.day)
        + "_"
        + str(date_time.hour)
        + "_"
        + str(date_time.minute)
        + "_"
        + str(date_time.second)
        + ".png",
        image,
    )


def black_image_part(
    image: cv2.typing.MatLike, visible_area: Rectangle
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
                Point(width_index, height_index)
            ):
                image[height_index][width_index][0] = 0
                image[height_index][width_index][1] = 0
                image[height_index][width_index][2] = 0

    return image


class FPSAverager:
    def __init__(self, size_limit: int):
        self.__max_size = size_limit
        self.__current_index = 0
        self.frame_list = []
        for _ in range(0, size_limit):
            self.frame_list.append(0)

    def insert_new_value(self, value: int):
        self.frame_list[self.__current_index] = value
        self.__current_index = (self.__current_index + 1) % self.__max_size

    def get_fps(self) -> int:
        assert len(self.frame_list) == self.__max_size
        return round(sum(self.frame_list) / len(self.frame_list), 1)


if __name__ == "__main__":
    mewtwo_reference = cv2.imread("selected_references/fight_menue_reference.png")
    blacked_image = black_image_part(
        mewtwo_reference[:][:][:],
        Rectangle(Point(1150, 80), Point(1550, 450)),
    )
    cv2.imshow("black example", blacked_image)
    cv2.waitKey(1)

    time.sleep(5)
    cv2.destroyAllWindows()
