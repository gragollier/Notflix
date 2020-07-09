FROM node:14

COPY ./package*.json ./
RUN npm ci
COPY ./ ./

EXPOSE 4000

ENTRYPOINT [ "node", "server.js" ]

