from locators.modal_locators import IngredientDetailsModalLocators
from pages.base_page import BasePage


class IngredientDetailsModal(BasePage):
    """
    Page Object модалки деталей ингредиента.
    Открывается поверх страницы конструктора по клику на ингредиент
    и имеет собственный маршрут /ingredient/<id>.
    """

    def is_open(self) -> bool:
        return self.is_present(IngredientDetailsModalLocators.TITLE)

    def get_title(self) -> str:
        return self.find(IngredientDetailsModalLocators.TITLE).text

    def get_ingredient_name(self) -> str:
        return self.find(IngredientDetailsModalLocators.INGREDIENT_NAME).text

    def close(self) -> None:
        self.click(IngredientDetailsModalLocators.CLOSE_BUTTON)
        # Дожидаемся, что модалка реально исчезла, а не просто прошёл клик —
        # на случай анимации закрытия или задержки перед размонтированием.
        self.wait_for_invisibility(IngredientDetailsModalLocators.TITLE)
