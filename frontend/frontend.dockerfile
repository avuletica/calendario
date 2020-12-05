FROM node:10

WORKDIR /app
COPY . /app

RUN npm install -g @angular/cli @angular-devkit/build-angular && npm install

EXPOSE 4200

CMD ["npm", "start"]
