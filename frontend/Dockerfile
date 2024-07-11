# Use a base image with Node.js 18
FROM node:20-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --silent

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 3000 to the outside world
EXPOSE 3000

# Start Nginx server to serve the app
CMD ["nginx", "-g", "daemon off;"]
