# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

This guide provides instructions to set up and run the Physical AI & Humanoid Robotics textbook project locally. The project is built using Docusaurus v3.

## 1. Prerequisites

Ensure you have the following installed:

-   **Node.js**: Version 18.0 or higher. You can download it from [nodejs.org](https://nodejs.org/).
-   **npm** (Node Package Manager): Usually comes bundled with Node.js. You can verify with `npm -v`.

## 2. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone [REPOSITORY_URL] # Replace with actual repository URL
cd humanoid-robotic-book # Or your project's root directory
```

## 3. Install Dependencies

Navigate to the project root and install the Docusaurus dependencies:

```bash
npm install
# Alternatively, if you use yarn:
yarn install
```

## 4. Run the Development Server

Start the Docusaurus development server to view the textbook locally. This will open the site in your browser at `http://localhost:3000` (or another available port).

```bash
npm start
# Or with yarn:
yarn start
```

## 5. Build the Static Site

To create a production-ready static build of the textbook, run:

```bash
npm run build
# Or with yarn:
yarn build
```

This will generate the static files in the `build/` directory, which can then be deployed to a web server (e.g., GitHub Pages).