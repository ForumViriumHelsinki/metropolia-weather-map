FROM node:alpine

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

COPY ./client/package*.json /app
COPY ./client /app
WORKDIR /app

RUN pnpm install
RUN pnpm dev