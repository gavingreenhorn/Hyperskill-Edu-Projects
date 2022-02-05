from dataclasses import dataclass, fields
from typing import ClassVar


class InvalidArgsError(Exception):
    def __init__(self, w_out):
        self.message = f'Incorrect number of arguments passed for {w_out}'
        super().__init__(self.message)


class InvalidWorkoutError(Exception):
    def __init__(self, w_out):
        self.message = f'Unknown workout type "{w_out}"'
        super().__init__(self.message)


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HR: ClassVar[int] = 60
    LEN_STEP: ClassVar[float] = 0.65
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        dist: float = self.get_distance()
        speed: float = self.get_mean_speed()
        cal: float = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__,
                           self.duration, dist, speed, cal)


class Running(Training):
    """Тренировка: бег."""
    COEFF_CAL_1: ClassVar[int] = 18
    COEFF_CAL_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CAL_1 * self.get_mean_speed() - self.COEFF_CAL_2)
                * self.weight
                / self.M_IN_KM * (self.duration * self.MIN_IN_HR))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CAL_1: ClassVar[float] = 0.035
    COEFF_CAL_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CAL_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CAL_2 * self.weight)
                * (self.duration * self.MIN_IN_HR))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CAL_1: ClassVar[float] = 1.1
    COEFF_CAL_2: ClassVar[int] = 2
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CAL_1) * self.COEFF_CAL_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout := WORKOUT_TYPES.get(workout_type):
        if len(fields(workout)) == len(data):
            return workout(*data)
        raise InvalidArgsError(workout)
    raise InvalidWorkoutError(workout_type)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


WORKOUT_TYPES: dict = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('SWM', [720, 1, 80, 25]),          # InvalidArgsError
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('FLY', [9000, 1, 50])              # InvalidWorkoutError
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
