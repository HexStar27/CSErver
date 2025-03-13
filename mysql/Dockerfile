# Gets latest version of mysql
FROM mysql:latest

# Load management database structure
ADD base_db.sql /etc/mysql/base_db.sql
RUN cp /etc/mysql/base_db.sql /docker-entrypoint-initdb.d
# Load in-game database data
ADD base_db.sql /etc/mysql/game_db.sql
RUN cp /etc/mysql/base_db.sql /docker-entrypoint-initdb.d
