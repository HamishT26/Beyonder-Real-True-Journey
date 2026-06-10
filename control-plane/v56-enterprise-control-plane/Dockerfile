FROM node:24-alpine
WORKDIR /app
COPY dashboard ./dashboard
COPY scripts ./scripts
COPY package.json ./
EXPOSE 8560
CMD ["npm", "run", "preview"]
