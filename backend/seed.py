def pokreni_automatski_seed(db, Misici, Vezbe, MisiciVezbe):
    #Za misice
    potrebni_misici=["Grudi", "Leđa", "Noge", "Ramena", "Biceps", "Triceps"]
    for naziv_misica in potrebni_misici:
        postoji = Misici.query.filter_by(naziv=naziv_misica).first()
        if not postoji:
            print(f"Mišić '{naziv_misica}' fali u bazi. Vraćam ga...")
            novi_misic = Misici(naziv=naziv_misica)
            db.session.add(novi_misic)

    db.session.commit()

    #Za vezbe
    potrebne_vezbe = ["Bench Press", "Razvlačenje bučicama", "Zgibovi", "Mrtvo dizanje", "Čučanj"]
    for ime_vezbe in potrebne_vezbe:
        postoji = Vezbe.query.filter_by(ime=ime_vezbe).first()
        if not postoji:
            print(f"Vežba '{ime_vezbe}' fali u bazi. Vraćam ga...")
            nova_vezba = Vezbe(ime=ime_vezbe)
            db.session.add(nova_vezba)

    db.session.commit()

    grudi = Misici.query.filter_by(naziv="Grudi").first()
    ledja = Misici.query.filter_by(naziv="Leđa").first()
    bench = Vezbe.query.filter_by(ime="Bench Press").first()
    razvlacenje = Vezbe.query.filter_by(ime="Razvlačenje bučicama").first()
    zgibovi = Vezbe.query.filter_by(ime="Zgibovi").first()
    mrtvo = Vezbe.query.filter_by(ime="Mrtvo dizanje").first()

    potrebne_veze = [
        {"misici_id": grudi.id, "vezbe_id": bench.id},
        {"misici_id": grudi.id, "vezbe_id": razvlacenje.id},
        {"misici_id": ledja.id, "vezbe_id": zgibovi.id},
        {"misici_id": ledja.id, "vezbe_id": mrtvo.id}
    ]

    for veza in potrebne_veze:
        postoji = MisiciVezbe.query.filter_by(misici_id=veza["misici_id"], vezbe_id=veza["vezbe_id"]).first()
        if not postoji:
            print(f"🔗 Veza između mišića ID:{veza['misici_id']} i vežbe ID:{veza['vezbe_id']} fali. Vraćam je...")
            nova_veza = MisiciVezbe(misici_id=veza["misici_id"], vezbe_id=veza["vezbe_id"])
            db.session.add(nova_veza)

    db.session.commit()