FROM node:24-alpine

# Set environment variables
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

# Install necessary packages and create non-root user
RUN apk add --no-cache libc6-compat && \
    addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

WORKDIR /app

# Copy package files first (needed for corepack to detect pnpm version)
COPY package.json pnpm-lock.yaml ./

# Enable pnpm with correct version from package.json (must run as root)
RUN corepack enable pnpm && corepack prepare --activate

# Change ownership of the working directory
RUN chown -R nextjs:nodejs /app

# Switch to non-root user for dependency installation
USER nextjs

# Install dependencies (allow lockfile updates in development)
RUN pnpm install --no-frozen-lockfile

# Copy source code
COPY --chown=nextjs:nodejs . .

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "const http = require('http'); http.get('http://localhost:3000/api/health', (res) => process.exit(res.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

CMD ["pnpm", "dev"]
