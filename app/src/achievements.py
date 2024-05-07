import mysql.connector
from src import app_config


class Achievement:
    id = 0
    name = ""
    description = ""

    @staticmethod
    def check_requirements(user_id: int):
        return dummy_check()


class VisitFiveShops(Achievement):
    id = 1
    name = "5 sklepów"
    description = "Odwiedź 5 sklepów"

    @staticmethod
    def check_requirements(user_id: int):
        return check_visit_count(needed_count=5, user_id=user_id)


class VisitFiftyShops(Achievement):
    id = 2
    name = "50 sklepów"
    description = "Odwiedź 50 sklepów"

    @staticmethod
    def check_requirements(user_id: int):
        return check_visit_count(needed_count=50, user_id=user_id)


class VisitHundredShops(Achievement):
    id = 3
    name = "100 sklepów"
    description = "Odwiedź 100 sklepów"

    @staticmethod
    def check_requirements(user_id: int):
        return check_visit_count(needed_count=100, user_id=user_id)


class GetTenPoints(Achievement):
    id = 4
    name = "10 punktów"
    description = "Zdobądź 10 punktów"

    @staticmethod
    def check_requirements(user_id: int):
        return check_point_count(needed_points=10, user_id=user_id)


class GetHundredPoints(Achievement):
    id = 5
    name = "100 punktów"
    description = "Zdobądź 100 punktów"

    @staticmethod
    def check_requirements(user_id: int):
        return check_point_count(needed_points=100, user_id=user_id)


VisitCountAchievements: list[Achievement] = [VisitFiveShops, VisitFiftyShops, VisitHundredShops]
PointCountAchievements: list[Achievement] = [GetTenPoints, GetHundredPoints]


def dummy_check() -> bool:
    """
    Placeholder function executed when the check_requirements() method is not implemented in one of the Achievement subclasses.

    :return: Always returns False.
    """
    print(f"The 'check_requirements()' function for one of the achievements is not implemented.")
    return False


def check_visit_count(needed_count: int, user_id: int) -> bool:
    """
    Checks if the user has visited a specific number of shops.

    :param needed_count: The required number of shop visits.
    :param user_id: The ID of the user.
    :return: True if the user has visited the required number of shops, False otherwise.
    """

    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT COUNT(place_id) FROM visits WHERE user_id = '{user_id}'"
            cursor.execute(query)
            visit_count = cursor.fetchone()[0]
    if visit_count >= needed_count:
        return True
    else:
        return False


def check_point_count(needed_points: int, user_id: int) -> bool:
    """
    Verifies if the user has a sufficient number of points.

    :param needed_points: The required number of points.
    :param user_id: The ID of the user whose points are being checked.
    :return: True if the user has enough points, False otherwise.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT rank_points FROM users WHERE id = '{user_id}'"
            cursor.execute(query)
            ranked_points = cursor.fetchone()[0]
    if ranked_points >= needed_points:
        return True
    else:
        return False


def check_triggers(user_id: int, achievements: list[Achievement]):
    for achievement in achievements:
        if achievement.check_requirements(user_id):
            add_achievement(user_id, achievement.id)


def check_achievement_acquisition(user_id: int, achievement_id: int):
    """
    Verifies if a user has acquired a specific achievement.

    :param user_id: The ID of the user.
    :param achievement_id: The ID of the achievement.
    :return: True if the achievement has been acquired by the user, False otherwise.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT EXISTS(SELECT * FROM users_achievements " \
                    f"WHERE user_id = '{user_id}' AND achievement_id = '{achievement_id}')"
            cursor.execute(query)
            is_acquired = cursor.fetchone()[0]
    if is_acquired:
        return True
    else:
        return False


def add_achievement(user_id: int, achievement_id: int) -> None:
    """
    Marks an achievement as acquired by a user.

    :param user_id: The ID of the user.
    :param achievement_id: The ID of the achievement.
    :return: None
    """
    if check_achievement_acquisition(user_id, achievement_id):
        return

    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"INSERT INTO users_achievements VALUES ({user_id}, {achievement_id})"
            cursor.execute(query)
        cnx.commit()

