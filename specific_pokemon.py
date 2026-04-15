import cv2
import numpy as np
import utils


class PokemonSearchEngine:
    def __init__(self):
        self.mewtwo_reference = cv2.imread("selected_references/mewtwo_reference.png")
        assert self.mewtwo_reference is not None

    def is_mewtwo(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.mewtwo_reference is not None
        return utils.is_image_part_equal(
            self.mewtwo_reference,
            captured_image,
            utils.Rectangle(utils.Point(310, 140), utils.Point(460, 185)),
        )

    def is_mewtwo_shiny(self, captured_image: cv2.typing.MatLike) -> bool:
        assert self.mewtwo_reference is not None
        mewtwo_point = utils.Point(1400, 350)
        return not utils.is_image_part_equal(
            self.mewtwo_reference,
            captured_image,
            utils.Rectangle(
                mewtwo_point, utils.Point(mewtwo_point.x + 1, mewtwo_point.y + 1)
            ),
        )


if __name__ == "__main__":
    search_engine = PokemonSearchEngine()
    black_image = np.zeros((1020, 1980, 3))
    print(
        "does reference of mewtwo equal a black image: "
        + str(search_engine.is_mewtwo(black_image))
    )
    for index in range(6, 1):
        print(index)
