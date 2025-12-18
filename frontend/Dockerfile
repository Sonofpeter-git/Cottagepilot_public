# Use the official Node.js image as the base image
FROM node:23-slim

# Set the working directory
WORKDIR /app
COPY package*.json ./

# Install dependencies
# Remove node_modules and package-lock.json if they exist
RUN rm -rf package-lock.json
RUN yarn
# Copy the rest of the backend files
COPY . .
RUN rm -rf node_modules/esbuild && yarn add --force esbuild && yarn add esbuild@latest


# Copy package.json and package-lock.json
#COPY package.json ./


EXPOSE 8080
# Start the application
CMD ["yarn", "dev"]