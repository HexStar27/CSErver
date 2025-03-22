# pull the Node.js Docker image
FROM node:latest

ARG SECRET
ARG MYSQL_BASE_PASS
ARG MYSQL_GAME_PASS


# Set the locale
RUN apt-get update && apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# create the directory inside the container
WORKDIR /usr/src/app

# copy the package.json files from local machine to the workdir in container
COPY package*.json ./

# run npm install in our local machine
RUN npm update
RUN npm audit fix --force

# copy all other files to the container
COPY . .

# self generating data for .env
#RUN echo "s/REPLACEME_SECRET/`cat /run/secrets/SECRET`/" | sed -i -f - .env
#RUN echo "s/REPLACEME_BASE_PASS/`cat /run/secrets/MYSQL_BASE_PASS`/" | sed -i -f - .env
#RUN echo "s/REPLACEME_GAME_PASS/`cat /run/secrets/MYSQL_GAME_PASS`/" | sed -i -f - .env
RUN sed -i -e "s/REPLACEME_SECRET/${SECRET}/" -e "s/REPLACEME_BASE_PASS/${MYSQL_BASE_PASS}/" -e "s/REPLACEME_GAME_PASS/${MYSQL_GAME_PASS}/" .env

EXPOSE 5000

CMD ["node", "app.js"]