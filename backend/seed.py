def pokreni_automatski_seed(db, Vezbe):

    pocetne_vezbe = [

        "Overhead Barbell Press",
        "Dumbbell Shoulder Press",
        "Arnold Press",
        "Lateral Raise",
        "Rear Delt Fly",


        "Bench Press",
        "Incline Dumbbell Press",
        "Decline Bench Press",
        "Chest Fly",
        "Push-ups",


        "Pull-ups",
        "Lat Pulldown",
        "Barbell Row",
        "Seated Cable Row",
        "Hyperextension",


        "Barbell Biceps Curl",
        "Dumbbell Hammer Curl",
        "Preacher Curl",
        "Triceps Pushdown",
        "Skull Crusher",
        "Dips",


        "Plank",
        "Crunches",
        "Hanging Leg Raise",


        "Squat",
        "Leg Press",
        "Hack Squat",
        "Romanian Deadlift",
        "Leg Curl",
        "Calf Raise"
    ]

    proizvedene_promene = False
    for ime_vezbe in pocetne_vezbe:

        postoji = Vezbe.query.filter_by(ime=ime_vezbe).first()
        if not postoji:
            nova_vezba = Vezbe(ime=ime_vezbe)
            db.session.add(nova_vezba)
            proizvedene_promene = True

    if proizvedene_promene:
        db.session.commit()
        print("Uspešno unete vežbe u bazu")
    else:
        print("Vežbe su uspešno učitane")