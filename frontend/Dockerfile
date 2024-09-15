# Use Node official image
FROM node:14

# Set work directory
WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy application code
COPY . .

# Build React app
RUN npm run build

# Expose the frontend port
EXPOSE 3000

# Serve the React app using a basic HTTP server
CMD ["npm", "start"]
