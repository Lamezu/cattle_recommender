import csv
import os
import random
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BREEDS = [
    {
        "name": "Holstein",
        "primary_use": "dairy",
        "price_min": 1800,
        "price_max": 3500,
        "description_templates": [
            "High-yield dairy cow with consistent milk production and strong udder conformation.",
            "Proven Holstein genetics with high fat and protein content in milk.",
            "Adaptable to intensive barn systems. Excellent production record.",
        ],
    },
    {
        "name": "Angus",
        "primary_use": "beef",
        "price_min": 2500,
        "price_max": 5500,
        "description_templates": [
            "Polled beef breed with superior marbling and easy calving record.",
            "Hardy Angus with efficient grazing behavior and calm temperament.",
            "Prime beef genetics. Excellent feedlot performance and carcass quality.",
        ],
    },
    {
        "name": "Hereford",
        "primary_use": "beef",
        "price_min": 2000,
        "price_max": 4800,
        "description_templates": [
            "Docile Hereford with strong foraging ability and structural soundness.",
            "Classic white-faced beef breed. Long productive lifespan.",
            "Efficient feed conversion. Ideal for extensive grassland operations.",
        ],
    },
    {
        "name": "Simmental",
        "primary_use": "dual",
        "price_min": 2200,
        "price_max": 5000,
        "description_templates": [
            "Versatile dual-purpose breed with strong growth and solid milk production.",
            "Large-framed Simmental with excellent maternal traits and high weaning weights.",
            "Suited for both beef and dairy production systems.",
        ],
    },
    {
        "name": "Limousin",
        "primary_use": "beef",
        "price_min": 2800,
        "price_max": 5800,
        "description_templates": [
            "Elite lean beef breed with high dressing percentage and fine bone structure.",
            "Highly muscled conformation. Top carcass yield. Valued in premium markets.",
            "Low subcutaneous fat. Ideal for butcher trade and feedlot programs.",
        ],
    },
    {
        "name": "Brahman",
        "primary_use": "beef",
        "price_min": 1800,
        "price_max": 4200,
        "description_templates": [
            "Heat-tolerant beef breed. Naturally resistant to ticks and parasites.",
            "Resilient Brahman genetics with excellent adaptability to harsh climates.",
            "Long-lived breed with strong foraging ability in tropical conditions.",
        ],
    },
    {
        "name": "Jersey",
        "primary_use": "dairy",
        "price_min": 1500,
        "price_max": 3200,
        "description_templates": [
            "High butterfat dairy breed. Efficient feed-to-milk conversion.",
            "Small-framed Jersey producing rich, high-value milk for artisan operations.",
            "Docile temperament. Consistent production with good heat tolerance.",
        ],
    },
    {
        "name": "Charolais",
        "primary_use": "beef",
        "price_min": 3000,
        "price_max": 6500,
        "description_templates": [
            "Large-framed beef breed with impressive muscle development and rapid growth.",
            "Premium Charolais genetics. Exceptional daily gain and carcass yield.",
            "White-coated breed with proven performance in feedlot and grass-fed systems.",
        ],
    },
    {
        "name": "Wagyu",
        "primary_use": "beef",
        "price_min": 8000,
        "price_max": 25000,
        "description_templates": [
            "Ultra-premium beef breed with verified extreme marbling score.",
            "Authentic Wagyu genetics with documented lineage. Investment-grade cattle.",
            "Extraordinary intramuscular fat. Commands the highest beef market prices.",
        ],
    },
    {
        "name": "Gyr",
        "primary_use": "dairy",
        "price_min": 1200,
        "price_max": 3000,
        "description_templates": [
            "Tropical dairy breed with solid production under heat stress.",
            "Zebu-type breed widely used in crossbreeding programs in Latin America.",
            "Hardy Gyr with consistent yield in hot and humid environments.",
        ],
    },
]

ENVIRONMENTS = [
    {"type": "Granja abierta"},
    {"type": "Establo intensivo"},
    {"type": "Pastoreo en montaña"},
    {"type": "Pastoreo extensivo"},
    {"type": "Granja tecnificada"},
    {"type": "Pastoreo tropical"},
    {"type": "Establo semi-intensivo"},
]

NAME_QUALIFIERS = [
    "Prime", "Elite", "Select", "Reserve", "Gold",
    "Classic", "Champion", "Heritage", "Alpha", "Royal",
    "Black", "Red", "Star", "Supreme", "Grand",
]

TOTAL_COWS = 500
TOTAL_FARMERS = 70
RATING_PROBABILITY = 0.65

GENDER_WEIGHTS = {
    "dairy": 0.88,
    "beef":  0.62,
    "dual":  0.72,
}

SECURITY_ANSWERS = [
    "sunflower", "mountain", "river", "copper", "thunder",
    "falcon", "maple", "granite", "meadow", "silver",
    "timber", "canyon", "prairie", "blossom", "harvest",
    "willow", "ranger", "cloudy", "pepper", "anchor",
    "rooster", "clover", "rustic", "golden", "storm",
    "bridle", "pasture", "acorn", "barley", "cricket",
]


def generate_cows() -> list[dict]:
    base_per_breed = TOTAL_COWS // len(BREEDS)
    counts = [base_per_breed] * len(BREEDS)
    for i in random.sample(range(len(BREEDS)), TOTAL_COWS - base_per_breed * len(BREEDS)):
        counts[i] += 1

    cows = []
    cow_counter = 1
    used_names: set[str] = set()

    for breed, count in zip(BREEDS, counts):
        name_pool = [
            (q, l, n)
            for q in NAME_QUALIFIERS
            for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for n in range(1, 100)
        ]
        random.shuffle(name_pool)
        pool_iter = iter(name_pool)

        for _ in range(count):
            while True:
                q, l, n = next(pool_iter)
                candidate = f"{breed['name']} {q} {l}{n:02d}"
                if candidate not in used_names:
                    used_names.add(candidate)
                    break

            cows.append({
                "cow_id":      f"C{cow_counter:04d}",
                "name":        candidate,
                "price":       round(random.uniform(breed["price_min"], breed["price_max"]), 2),
                "description": random.choice(breed["description_templates"]),
                "gender":      "female" if random.random() < GENDER_WEIGHTS[breed["primary_use"]] else "male",
                "breed":       breed["name"],
                "environment": random.choice(ENVIRONMENTS)["type"],
            })
            cow_counter += 1

    return cows


def generate_farmers() -> list[dict]:
    farmers = []
    used_names: set[str] = set()

    for i in range(1, TOTAL_FARMERS + 1):
        while True:
            name = fake.name()
            if name not in used_names:
                used_names.add(name)
                break

        farmers.append({
            "farmer_id":       f"F{i:04d}",
            "name":            name,
            "security_answer": random.choice(SECURITY_ANSWERS),
        })

    return farmers


def generate_relationships(farmers: list[dict], cows: list[dict]) -> tuple[list, list, list]:
    cow_ids = [c["cow_id"] for c in cows]
    buys, viewed, rated = [], [], []

    for farmer in farmers:
        fid    = farmer["farmer_id"]
        bought = set(random.sample(cow_ids, random.randint(3, 10)))

        for cid in bought:
            buys.append({"farmer_id": fid, "cow_id": cid})

        n_viewed_target = random.randint(max(10, len(bought)), 30)
        pool            = [c for c in cow_ids if c not in bought]
        extra           = random.sample(pool, min(max(0, n_viewed_target - len(bought)), len(pool)))
        for cid in bought | set(extra):
            viewed.append({"farmer_id": fid, "cow_id": cid})

        if random.random() < RATING_PROBABILITY:
            for cid in random.sample(list(bought), random.randint(1, len(bought))):
                rated.append({"farmer_id": fid, "cow_id": cid, "stars": random.randint(1, 5)})

    return buys, viewed, rated


def validate_relationships(buys, rated) -> bool:
    buys_set  = {(r["farmer_id"], r["cow_id"]) for r in buys}
    rated_set = {(r["farmer_id"], r["cow_id"]) for r in rated}
    orphans   = rated_set - buys_set
    if orphans:
        print(f"  VALIDATION FAILED — {len(orphans)} RATED entries not in BUYS: {list(orphans)[:5]}")
        return False
    print("  Validation passed — all RATED pairs exist in BUYS.")
    return True


def compute_ratings(cows: list[dict], rated: list[dict]) -> None:
    from collections import defaultdict
    stars_by_cow = defaultdict(list)
    for r in rated:
        stars_by_cow[r["cow_id"]].append(r["stars"])
    for cow in cows:
        stars = stars_by_cow.get(cow["cow_id"], [])
        cow["rating"] = round(sum(stars) / len(stars), 2) if stars else ""


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {filename:<22}  {len(rows):>5} rows  →  {path}")


def export_csvs(farmers, cows, buys, viewed, rated) -> None:
    compute_ratings(cows, rated)

    print("=== GENERATE CSVs ===\n")

    write_csv("farmers.csv",
              ["farmer_id", "name", "security_answer"],
              farmers)

    write_csv("cows.csv",
              ["cow_id", "name", "price", "description", "gender", "rating", "breed", "environment"],
              cows)

    write_csv("breeds.csv",
              ["name"],
              [{"name": b["name"]} for b in BREEDS])

    write_csv("environments.csv",
              ["type"],
              ENVIRONMENTS)

    write_csv("buys.csv",
              ["farmer_id", "cow_id"],
              buys)

    write_csv("viewed.csv",
              ["farmer_id", "cow_id"],
              viewed)

    write_csv("rated.csv",
              ["farmer_id", "cow_id", "stars"],
              rated)

    print(f"\n  All files written to: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    farmers = generate_farmers()
    cows    = generate_cows()
    buys, viewed, rated = generate_relationships(farmers, cows)

    if validate_relationships(buys, rated):
        export_csvs(farmers, cows, buys, viewed, rated)
