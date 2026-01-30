FROM node:18-alpine

# Install dependencies
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies (use npm install instead of npm ci)
RUN npm install

# Copy all files
COPY . .

# Build the application
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port 7860 for Hugging Face
EXPOSE 7860
ENV PORT 7860
ENV HOSTNAME "0.0.0.0"

# Start the application
CMD ["npm", "start", "--", "-p", "7860"]
