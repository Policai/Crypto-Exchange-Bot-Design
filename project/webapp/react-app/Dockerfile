FROM node:20-alpine
WORKDIR /app
COPY webapp/react-app/package*.json ./
RUN npm install
COPY webapp/react-app .
CMD ["npm", "run", "dev"]
