db.getSiblingDB("markets").createUser(
        {
            user: "app",
            pwd: "qwe123",
            roles: [
                {
                    role: "readWrite",
                    db: "markets"
                }
            ]
        }
);