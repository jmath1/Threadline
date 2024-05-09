FROM node:22
WORKDIR /app
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
