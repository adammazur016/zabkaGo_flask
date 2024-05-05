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
    Executes when one of Achievement subclass doesn't implement check_requirements()
    """
    print(f"\"Check function\" for one of achievements is not implemented")
    return False


def check_visit_count(needed_count: int, user_id: int) -> bool:
    """
    Checks if the user has visited specific amount of shops
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
    Checks if the user has enough points
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
    Checks if user got an achievement
    :return: True if achievement was already acquired, False otherwise
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
    Add achievement as acquired by user
    """
    if check_achievement_acquisition(user_id, achievement_id):
        return

    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"INSERT INTO users_achievements VALUES ({user_id}, {achievement_id})"
            cursor.execute(query)
        cnx.commit()

