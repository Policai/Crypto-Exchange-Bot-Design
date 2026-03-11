FROM node:20-alpine
WORKDIR /app
COPY admin-panel/package*.json ./
RUN npm install
COPY admin-panel .
CMD ["npm", "run", "dev"]
