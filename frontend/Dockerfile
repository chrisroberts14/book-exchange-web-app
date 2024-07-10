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

# Use a lightweight image for serving the built app
FROM nginx:alpine

# Copy the built app from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 5173 to the outside world
EXPOSE 5173

# Start Nginx server to serve the app
CMD ["nginx", "-g", "daemon off;"]
