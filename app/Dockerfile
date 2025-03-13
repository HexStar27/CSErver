# pull the Node.js Docker image
FROM node:alpine

# create the directory inside the container
WORKDIR /usr/src/app

# copy the package.json files from local machine to the workdir in container
COPY package*.json ./
# run npm install in our local machine
RUN npm install

# copy all other files to the container
COPY . .

EXPOSE 5000

CMD ["node", "app.js"]