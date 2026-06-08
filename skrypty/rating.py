def player_rating(speed, dribbling, strength, decisions):
    weights = {
        "speed": 0.3,
        "dribbling": 0.3,
        "strength": 0.2,
        "decisions": 0.2
    }

    rating = (
        speed * weights["speed"] +
        dribbling * weights["dribbling"] +
        strength * weights["strength"] +
        decisions * weights["decisions"]
    )

    return round(rating, 2)


# przykład (Topi Keskinen)
print(player_rating(9, 8, 6, 7))
