FROM node:14

COPY ./package*.json ./
RUN npm ci
COPY ./ ./

EXPOSE 4500

ENTRYPOINT [ "node", "server.js" ]
