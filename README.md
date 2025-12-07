# Physical AI & Humanoid Robotics Textbook

**A comprehensive educational resource on Physical AI and Humanoid Robotics built with Docusaurus**

---

## Overview

This repository contains a complete textbook on **Physical AI & Humanoid Robotics**, structured as a Docusaurus-based website. The textbook is designed as a 13-week curriculum covering the fundamental concepts, technologies, and applications in humanoid robotics and physical artificial intelligence.

## Course Structure

The textbook is organized into four progressive modules:

1. **Module 1: The Robotic Nervous System (ROS 2)**
   - ROS 2 architecture, nodes, topics, and services
   - Bridging Python agents to ROS controllers using `rclpy`
   - URDF (Unified Robot Description Format) for humanoid robots

2. **Module 2: The Digital Twin (Gazebo & Unity)**
   - Physics simulation and environment construction
   - Gazebo physics: gravity, collisions, constraints
   - Unity rendering & Human-Robot Interaction (HRI)
   - Sensor simulation: LiDAR, depth cameras, IMUs

3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)**
   - NVIDIA Isaac Sim: photorealistic simulation and synthetic data generation
   - Isaac ROS: hardware-accelerated perception
   - Nav2 for bipedal humanoid navigation

4. **Module 4: Vision-Language-Action (VLA)**
   - Whisper for voice-to-command pipeline
   - LLM-based cognitive planning (natural language to ROS 2 action graph)
   - Capstone: Autonomous humanoid executing voice commands

## Features

- **13-week curriculum** with structured learning path
- **Interactive documentation** built with Docusaurus v3
- **Mermaid diagrams** for visual explanations
- **Conceptual code examples** in Python and ROS 2
- **Comprehensive glossary** of robotics and AI terms
- **GitHub Pages deployment** for easy access

## Prerequisites

- Node.js v18.x or higher
- npm (Node Package Manager)
- Basic programming experience (preferably Python)
- Understanding of linear algebra and calculus
- Familiarity with basic physics concepts

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nadeemsangrasi/humanoid-and-robotic-book.git
   cd humanoid-and-robotic-book
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm start
   ```
   The textbook will be available at `http://localhost:3000/humanoid-robotic-book/`

4. **Build the static site:**
   ```bash
   npm run build
   ```

## Project Structure

```
├── docs/                    # Textbook content
│   ├── introduction/        # Course introduction
│   ├── quarter-overview/    # 13-week curriculum overview
│   ├── module-1-ros2/       # ROS 2 fundamentals
│   ├── module-2-gazebo-unity/ # Simulation environments
│   ├── module-3-nvidia-isaac/ # Advanced simulation
│   ├── module-4-vla/        # Vision-Language-Action models
│   ├── capstone/            # Final project
│   └── glossary.md          # Robotics terminology
├── specs/                   # Project specifications
├── src/                     # Custom Docusaurus components
├── static/                  # Static assets
├── docusaurus.config.ts     # Docusaurus configuration
├── sidebars.ts              # Navigation sidebar configuration
└── package.json             # Project dependencies and scripts
```

## Deployment

The textbook is deployed on GitHub Pages at: [https://nadeemsangrasi.github.io/humanoid-and-robotic-book/](https://nadeemsangrasi.github.io/humanoid-and-robotic-book/)

## Contributing

This project uses Spec-Driven Development (SDD) methodology with:
- Detailed specifications in the `specs/` directory
- Structured task management in `specs/001-physical-ai-textbook/tasks.md`
- Architectural planning in `specs/001-physical-ai-textbook/plan.md`

## License

This project is licensed under the ISC License.

---

**Keywords:** robotics, humanoid robotics, physical AI, ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA, textbook, docusaurus, simulation, artificial intelligence