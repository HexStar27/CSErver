# Gets latest version of mysql
FROM mysql:latest

ARG MYSQL_BASE_PASS
ARG MYSQL_GAME_PASS

#RUN echo "s/REPLACEME_BP/$MYSQL_ROOT_PASSWORD/"

# Load management database structure
ADD base_db.sql /etc/mysql/base_db.sql
#RUN echo "s/REPLACEME_BP/`cat /run/secrets/MYSQL_BASE_PASS`/" | sed -i -f - /etc/mysql/base_db.sql
#RUN echo "s/REPLACEME_GP/`cat /run/secrets/MYSQL_GAME_PASS`/" | sed -i -f - /etc/mysql/base_db.sql
RUN sed -i -e "s/REPLACEME_BP/${MYSQL_BASE_PASS}/" -e "s/REPLACEME_GP/${MYSQL_GAME_PASS}/" /etc/mysql/base_db.sql
RUN cp /etc/mysql/base_db.sql /docker-entrypoint-initdb.d
# Load in-game database data
ADD game_db.sql /etc/mysql/game_db.sql
#RUN echo "s/REPLACEME_BP/`cat /run/secrets/MYSQL_BASE_PASS`/" | sed -i -f - /etc/mysql/game_db.sql
#RUN echo "s/REPLACEME_GP/`cat /run/secrets/MYSQL_GAME_PASS`/" | sed -i -f - /etc/mysql/game_db.sql
RUN sed -i -e "s/REPLACEME_BP/${MYSQL_BASE_PASS}/" -e "s/REPLACEME_GP/${MYSQL_GAME_PASS}/" /etc/mysql/game_db.sql
RUN cp /etc/mysql/game_db.sql /docker-entrypoint-initdb.d
