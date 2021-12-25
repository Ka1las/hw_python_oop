from dataclasses import astuple, dataclass
from typing import List, Tuple, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить строку."""
        return self.get_template_message().format(
            *astuple(self)
        )

    def get_template_message(self) -> str:
        """Получить шаблон строки."""
        return (
            "Тип тренировки: {}; Длительность: {:.3f} ч.; Дистанция: {:.3f}"
            " км; Ср. скорость: {:.3f} км/ч; Потрачено ккал: {:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info: InfoMessage = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return training_info


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
            (
                self.coeff_calorie_1
                * self.get_mean_speed() - self.coeff_calorie_2)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.M_IN_HR
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_3: float = 0.035
    coeff_calorie_4: int = 2
    coeff_calorie_5: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
            (
                self.coeff_calorie_3 * self.weight
                + self.get_mean_speed()
                * self.coeff_calorie_4
                // self.height
                * self.coeff_calorie_5
                * self.weight
            )
            * self.duration
            * self.M_IN_HR
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    coeff_calorie_4: int = 2
    coeff_calorie_6: float = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = (
            (self.get_mean_speed() + self.coeff_calorie_6)
            * self.coeff_calorie_4
            * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    training = dictionary.get(workout_type)
    if training is None:
        raise ValueError('Такой тренировки нет')
    return training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages: List[Tuple[str, List[int]]] = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
