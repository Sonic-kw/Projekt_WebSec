FROM node:20-alpine

WORKDIR /app

COPY . /app 

EXPOSE 5173

RUN npm install

ENTRYPOINT ["npm", "run", "dev"]