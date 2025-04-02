from faker import Faker
from models import db, Superhero, City, Hero, Power, HeroPower
from app import app

fake = Faker()

def seed_data():
    with app.app_context():
        try:
            # Ensure database schema is created
            db.create_all()

            # Clear existing data dynamically
            models = [HeroPower, Power, Hero, Superhero, City]
            for model in models:
                print(f"Clearing data for {model.__name__}...")
                db.session.query(model).delete(synchronize_session=False)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing data: {e}")
            return

        # Seed Cities
        cities = [City(name=fake.city()) for _ in range(70)]
        db.session.add_all(cities)
        db.session.commit()

        # Seed Superheroes
        superheroes = [
            Superhero(
                name=fake.name(),
                city_id=fake.random_element(cities).id
            ) for _ in range(10)
        ]
        db.session.add_all(superheroes)
        db.session.commit()

        # Seed Heroes
        heroes = [
            Hero(
                name=fake.name(),
                super_name=fake.word(),
                superpower=fake.word(),
                superhero_id=fake.random_element(superheroes).id
            ) for _ in range(100)
        ]
        db.session.add_all(heroes)

        # Add specific hero
        db.session.add(Hero(
            name="Clark Kent",
            super_name="Superman",
            superpower="Flight",
            superhero_id=fake.random_element(superheroes).id
        ))
        db.session.commit()

        # Seed Powers
        powers = []
        for _ in range(100):
            description = fake.text(max_nb_chars=50)
            if len(description) < 20:
                description = "Default description with sufficient length."
            power = Power(
                name=fake.word(),
                description=description
            )
            powers.append(power)
        db.session.add_all(powers)
        db.session.commit()

        # Seed HeroPowers
        hero_powers = [
            HeroPower(
                hero_id=fake.random_element(heroes).id,
                power_id=fake.random_element(powers).id,
                strength=fake.random_element(["Strong", "Weak", "Average"])
            ) for _ in range(150)
        ]
        db.session.add_all(hero_powers)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
