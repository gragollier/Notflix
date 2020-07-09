FROM node:14

COPY ./package*.json ./
RUN npm ci
COPY ./ ./

ENTRYPOINT [ "node", "server.js" ]

