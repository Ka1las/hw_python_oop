from typing import List, Tuple


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: int,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: int = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HR: int = 60
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: int = 2
    coeff_calorie_5: float = 0.029
    coeff_calorie_6: float = 1.1

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        traning_info = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return traning_info


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = (
            (
                self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.M_IN_HR
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

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
        calories = (
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
        speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = (
            (self.get_mean_speed() + self.coeff_calorie_6)
            * self.coeff_calorie_4
            * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
