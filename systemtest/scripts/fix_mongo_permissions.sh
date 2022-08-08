mongo --host 127.0.0.1 --port 27017 -u root -p root_password123 --authenticationDatabase admin < dbs/market_db.js
mongo --host 127.0.0.1 --port 27017 -u root -p root_password123 --authenticationDatabase admin < dbs/wallet_db.js
mongo --host 127.0.0.1 --port 27017 -u root -p root_password123 --authenticationDatabase admin < dbs/balance_db.js
mongo --host 127.0.0.1 --port 27017 -u root -p root_password123 --authenticationDatabase admin < dbs/trollbox_db.js
