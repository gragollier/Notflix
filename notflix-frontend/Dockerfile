FROM node AS builder

WORKDIR /src/app
COPY ./package*.json ./
RUN npm ci
COPY ./ ./
RUN npm run build

FROM nginx
COPY --from=builder /src/app/build /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
