import cv2
import numpy as np
import utils


class PokemonSearchEngine:
    def __init__(self):
        self.mewtwo_reference = cv2.imread(
            "selected_references/fight_menue_reference.png"
        )

    def is_mewtwo(self, captured_image: cv2.typing.MatLike) -> bool:
        return utils.is_status_menue_equal(self.mewtwo_reference, captured_image)

    def is_mewtwo_shiny(self, captured_image: cv2.typing.MatLike) -> bool:
        return not utils.is_pokemon_equal(self.mewtwo_reference, captured_image)


if __name__ == "__main__":
    search_engine = PokemonSearchEngine()
    black_image = np.zeros((1020, 1980, 3))
    print(
        "does reference of mewtwo equal a black image: "
        + str(search_engine.is_mewtwo(black_image))
    )
    for index in range(6, 1):
        print(index)
