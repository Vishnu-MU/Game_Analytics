queries = {
    "Competitions": {
        "List all competitions along with their category name": """
            SELECT c.competition_name, cat.category_name
            FROM competitions c
            JOIN categories cat ON c.category_id = cat.category_id
        """,
        "Count the number of competitions in each category": """
            SELECT cat.category_name, COUNT(c.competition_id) AS competition_count
            FROM categories cat
            LEFT JOIN competitions c ON cat.category_id = c.category_id
            GROUP BY cat.category_name
        """,
        "Find all competitions of type 'doubles'": """
            SELECT competition_name
            FROM competitions
            WHERE type = 'doubles'
        """,
        "Get competitions that belong to a specific category (e.g., ITF Men)": """
            SELECT c.competition_name, cat.category_name
            FROM competitions c
            INNER JOIN categories cat ON c.category_id = cat.category_id
            WHERE cat.category_name = 'ITF Men'
        """,
        "Identify parent competitions and their sub-competitions": """
            SELECT parent.competition_name AS Parent_Competition, child.competition_name AS Sub_Competition
            FROM competitions child
            INNER JOIN competitions parent ON child.parent_id = parent.competition_id
        """,
        "Analyze the distribution of competition types by category": """
            SELECT cat.category_name, c.type, COUNT(c.competition_id) AS competition_count
            FROM competitions c
            INNER JOIN categories cat ON c.category_id = cat.category_id
            GROUP BY cat.category_name, c.type
            ORDER BY cat.category_name, c.type
        """,
        "List all competitions with no parent (top-level competitions)": """
            SELECT competition_name
            FROM competitions
            WHERE parent_id IS NULL
        """
    },
    "Complexes": {
        "List all venues along with their associated complex name": """
            SELECT v.venue_name, c.complex_name
            FROM venues v
            JOIN complexes c ON v.complex_id = c.complex_id
        """,
        "Count the number of venues in each complex": """
            SELECT c.complex_name , COUNT(v.venue_id) AS venue_count
            FROM complexes c
            LEFT JOIN venues v ON v.complex_id = c.complex_id
            GROUP BY c.complex_name
        """, 
        "Get details of venues in a specific country (e.g., Chile)": """
            SELECT venue_id ,venue_name,city_name
            FROM venues
            WHERE country_name = 'Chile'
        """,
        "Identify all venues and their timezones": """
            SELECT venue_id ,venue_name,city_name,timezone
            FROM venues
        """,
        "Find complexes that have more than one venue": """
            SELECT c.complex_name , COUNT(v.venue_id) AS venue_count
            from complexes c
            LEFT JOIN venues v ON c.complex_id = v.complex_id
            GROUP BY c.complex_name
            having COUNT(v.venue_id) > 1;  
        """,
        "List venues grouped by country": """
            SELECT country_name , venue_name
            FROM venues
            order BY country_name;  
        """,
        "Find all venues for a specific complex (e.g., Nacional)": """
            SELECT v.venue_name
            FROM venues v
            JOIN complexes c ON v.complex_id = c.complex_id
            wHERE c.complex_name = 'Nacional'
        """
    },
    "Competitors": {
        "Get all competitors with their rank and points.": """
            SELECT c.competitor_id , c.name , r.rank , r.points
            FROM competitor c
            JOIN rankings r ON c.competitor_id = r.competitor_id
        """,
        "Find competitors ranked in the top 5": """
            SELECT c.competitor_id , c.name , r.rank
            FROM competitor c
            JOIN rankings r ON c.competitor_id = r.competitor_id
            WHERE r.rank <= 5
        """,
        "List competitors with no rank movement (stable rank)": """
            SELECT c.competitor_id , c.name , r.rank , r.movement
            FROM competitor c
            JOIN rankings r ON c.competitor_id = r.competitor_id
            WHERE movement = 0
        """,
        "Get the total points of competitors from a specific country (e.g., Croatia)": """
            SELECT c.country , SUM(r.points) as total_points
            FROM rankings r
            JOIN competitor c ON c.competitor_id = r.competitor_id
            WHERE c.country = 'Croatia'
        """,
        "Count the number of competitors per country": """
            SELECT country, count(competitor_id) as total_competitor
            FROM competitor
            GROUP BY country
        """,
        "Find competitors with the highest points in the current week": """
            SELECT c.competitor_id, c.name ,r.points
            FROM competitor c
            JOIN rankings r ON c.competitor_id = r.competitor_id
            WHERE r.points = (SELECT MAX(points) FROM rankings)
        """ 
    }    
    }