# SkillBridge API Backend

github : https://github.com/Upendraredd/skillbridge

database url : postgresql+psycopg://postgres:Upendra143@127.0.0.1:5432/skillbridge

The Core Technologies Explained
FastAPI: This is your web framework. We used it because it is incredibly fast, natively supports asynchronous code, and automatically generates interactive API documentation (that Swagger UI page at /docs).

PostgreSQL (via Neon): This is your relational database. Neon is a modern, serverless hosting provider for PostgreSQL. We used a relational database because your entities (Users, Batches, Sessions, Attendance) are highly connected, and SQL is the best tool for enforcing those relationships.

SQLAlchemy: This is an ORM (Object-Relational Mapper). Instead of writing raw SQL queries as strings (which is prone to errors and security risks), SQLAlchemy lets you interact with your database using standard Python classes and objects. It acts as the "translator."

JWT (JSON Web Tokens): This is your primary authentication method. Instead of storing a session ID in the database for every logged-in user, a JWT is a cryptographically signed "badge" the user holds. Your server can look at the badge, verify the signature, and instantly know who the user is and what their role is without querying the database.

Dual-Token Authentication (The specific security logic): For the Monitoring Officer, we required a standard login plus an API Key. Why? Because monitoring officers access highly sensitive, system-wide data. If a normal token is stolen, the attacker only gets 24 hours of access. By requiring an API key to generate a separate, short-lived (1 hour) token specifically for monitoring, we heavily restrict the "blast radius" if a token is compromised.

Pytest: The testing framework used to automatically ping your endpoints and ensure they return the correct HTTP status codes (like 200 OK, 401 Unauthorized, or 405 Method Not Allowed).
