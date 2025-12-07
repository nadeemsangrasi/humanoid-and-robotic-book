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

Start the Docusaurus development server to view the textbook locally. By default, this will open the site in your browser at `http://localhost:3000/humanoid-robotic-book/` (or another available port with the correct base URL).

```bash
npm start
# Or with yarn:
yarn start
```

To run the development server on a specific port (e.g., 3000):

```bash
npx docusaurus start --port 3000
```

## 5. Build the Static Site

To create a production-ready static build of the textbook, run:

```bash
npm run build
# Or with yarn:
yarn build
```

This will generate the static files in the `build/` directory, which can then be deployed to a web server (e.g., GitHub Pages).

## 6. Additional Development Commands

### Serve the Built Site Locally

To serve the built site locally for testing:

```bash
npm run serve
# Or with yarn:
yarn serve
```

### Check for Broken Links

To validate internal and external links in the documentation:

```bash
npx remark --use validate-links docs/**/*.md docs/**/*.mdx
```

### Lint Markdown/MDX Files

To check for formatting and syntax issues in documentation files:

```bash
npx eslint . --ext md,mdx,js,ts,jsx,tsx
```

## 7. Project Structure

The textbook is organized into modules as follows:

- **Introduction**: `docs/introduction/`
- **Quarter Overview**: `docs/quarter-overview/`
- **Module 1 - ROS 2 Fundamentals**: `docs/module-1-ros2/`
- **Module 2 - Gazebo and Unity Simulation**: `docs/module-2-gazebo-unity/`
- **Module 3 - NVIDIA Isaac Sim**: `docs/module-3-nvidia-isaac/`
- **Module 4 - Vision-Language-Action Models**: `docs/module-4-vla/`
- **Capstone Project**: `docs/capstone/`
- **Glossary**: `docs/glossary.md`

## 8. Adding New Content

To add new chapters to the textbook:

1. Create a new `.mdx` file in the appropriate module directory
2. Follow the chapter template structure with proper frontmatter:
   ```md
   ---
   title: 'Your Chapter Title'
   slug: /module-1-ros2/your-chapter-slug
   sidebar_position: X
   ---
   ```
3. Add the new chapter to the `sidebars.ts` file to make it appear in the navigation
4. Include proper learning objectives, diagrams (using Mermaid syntax), code examples, and exercises as per the textbook standards