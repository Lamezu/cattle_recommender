def setup_database_constraints(driver):
    """
    Initializes the database schema by setting up necessary constraints.
    These constraints ensure data integrity and automatically create indexes for performance.
    """
    queries = [
        "CREATE CONSTRAINT farmer_id_unique IF NOT EXISTS FOR (f:Farmer) REQUIRE f.farmer_id IS UNIQUE",
        "CREATE CONSTRAINT cow_id_unique IF NOT EXISTS FOR (c:Cow) REQUIRE c.cow_id IS UNIQUE",
        "CREATE CONSTRAINT breed_name_unique IF NOT EXISTS FOR (b:Breed) REQUIRE b.name IS UNIQUE",
        "CREATE CONSTRAINT environment_type_unique IF NOT EXISTS FOR (e:Environment) REQUIRE e.type IS UNIQUE"
    ]
    
    with driver.session() as session:
        for query in queries:
            session.run(query)
