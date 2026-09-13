FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
COPY apps/dashboard/package.json ./

EXPOSE 3000
CMD ["npm", "run", "dev"]

