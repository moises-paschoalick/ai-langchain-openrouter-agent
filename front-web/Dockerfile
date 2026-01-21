FROM node:20-alpine

WORKDIR /app

COPY front-web/package.json front-web/package-lock.json* ./

RUN npm ci

COPY front-web .

RUN npm run build

# Serve com nginx
FROM nginx:stable-alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]