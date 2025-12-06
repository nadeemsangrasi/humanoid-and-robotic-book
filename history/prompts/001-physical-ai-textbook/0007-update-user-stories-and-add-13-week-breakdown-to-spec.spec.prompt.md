---
id: 0007
title: Update User Stories and Add 13-Week Breakdown to Spec
stage: spec
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: User
command: |-
  Update the user stories with these slight adjustments:

  - **User Story 1** → add details about the final book layout/structure (Docusaurus folder hierarchy, sidebar navigation, frontmatter standards) and user interaction (student navigation flow, how exercises and code blocks are accessed).

  - **User Story 3** → update to explicitly state that the full content of the 4 modules will be divided into exactly 13 weeks of teaching material (Weeks 1–13).

  - **User Story 4** → rename the existing 4th user story to 5th; insert a new User Story 4 titled “Adding chapter content inside each module folder” (i.e., populating the module directories with the weekly chapters).

  - Keep the module descriptions exactly as before, but replace the previous loose structure with this precise 13-week division:

  **chapters**

  *Module 1: The Robotic Nervous System (ROS 2)*

  - Focus: Middleware for robot control.

  - ROS 2 Nodes, Topics, and Services.

  - Bridging Python Agents to ROS controllers using rclpy.

  - Understanding URDF for humanoids.

  *Module 2: The Digital Twin (Gazebo & Unity)*

  - Focus: Physics simulation and environment building.

  - Simulating physics, gravity, and collisions in Gazebo.

  - High-fidelity rendering and human-robot interaction in Unity.

  - Simulating sensors: LiDAR, Depth Cameras, and IMUs.

  *Module 3: The AI-Robot Brain (NVIDIA Isaac™)*

  - Focus: Advanced perception and training.

  - NVIDIA Isaac Sim: Photorealistic simulation and synthetic data generation.

  - Isaac ROS: Hardware-accelerated VSLAM and navigation.

  - Nav2: Path planning for bipedal humanoid movement.

  *Module 4: Vision-Language-Action (VLA)*

  - Focus: The convergence of LLMs and Robotics.

  - Voice-to-Action: Using OpenAI Whisper for voice commands.

  - Cognitive Planning: Using LLMs to translate natural language into ROS 2 actions sequences.

  - Capstone Project: The Autonomous Humanoid.

  **Week-by-Week Breakdown**

  Weeks 1–2: Introduction to Physical AI

  Weeks 3–5: ROS 2 Fundamentals

  Weeks 6–7: Robot Simulation with Gazebo

  Weeks 8–10: NVIDIA Isaac Platform

  Weeks 11–12: Humanoid Robot Development

  Week 13: Conversational Robotics
labels: ["specification", "user-story", "update", "docusaurus", "curriculum"]
links:
  spec: /mnt/d/speckKit-Hackathons/humanoid-robotic-book/specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
- /mnt/d/speckKit-Hackathons/humanoid-robotic-book/specs/001-physical-ai-textbook/spec.md
- /mnt/d/speckKit-Hackathons/humanoid-robotic-book/specs/001-physical-ai-textbook/checklists/requirements.md
tests: []
---

## Prompt

```text
Update the user stories with these slight adjustments:

- **User Story 1** → add details about the final book layout/structure (Docusaurus folder hierarchy, sidebar navigation, frontmatter standards) and user interaction (student navigation flow, how exercises and code blocks are accessed).

- **User Story 3** → update to explicitly state that the full content of the 4 modules will be divided into exactly 13 weeks of teaching material (Weeks 1–13).

- **User Story 4** → rename the existing 4th user story to 5th; insert a new User Story 4 titled “Adding chapter content inside each module folder” (i.e., populating the module directories with the weekly chapters).

- Keep the module descriptions exactly as before, but replace the previous loose structure with this precise 13-week division:

**chapters**

*Module 1: The Robotic Nervous System (ROS 2)*

- Focus: Middleware for robot control.

- ROS 2 Nodes, Topics, and Services.

- Bridging Python Agents to ROS controllers using rclpy.

- Understanding URDF for humanoids.

*Module 2: The Digital Twin (Gazebo & Unity)*

- Focus: Physics simulation and environment building.

- Simulating physics, gravity, and collisions in Gazebo.

- High-fidelity rendering and human-robot interaction in Unity.

- Simulating sensors: LiDAR, Depth Cameras, and IMUs.

*Module 3: The AI-Robot Brain (NVIDIA Isaac™)*

- Focus: Advanced perception and training.

- NVIDIA Isaac Sim: Photorealistic simulation and synthetic data generation.

- Isaac ROS: Hardware-accelerated VSLAM and navigation.

- Nav2: Path planning for bipedal humanoid movement.

*Module 4: Vision-Language-Action (VLA)*

- Focus: The convergence of LLMs and Robotics.

- Voice-to-Action: Using OpenAI Whisper for voice commands.

- Cognitive Planning: Using LLMs to translate natural language into ROS 2 actions sequences.

- Capstone Project: The Autonomous Humanoid.

**Week-by-Week Breakdown**

Weeks 1–2: Introduction to Physical AI

Weeks 3–5: ROS 2 Fundamentals

Weeks 6–7: Robot Simulation with Gazebo

Weeks 8–10: NVIDIA Isaac Platform

Weeks 11–12: Humanoid Robot Development

Week 13: Conversational Robotics
```

## Response snapshot

```text
The spec `/mnt/d/speckKit-Hackathons/humanoid-robotic-book/specs/001-physical-ai-textbook/spec.md` has been successfully updated with the revised user stories and the 13-week curriculum breakdown. The `requirements.md` checklist has also been re-validated.

All project documentation is now consistent with your latest instructions.
```

## Outcome

- ✅ Impact: User stories in spec.md updated with detailed Docusaurus structure, 13-week curriculum, new User Story 4, and renamed User Story 5.
- 🧪 Tests: N/A
- 📁 Files: Modified spec.md and requirements.md.
- 🔁 Next prompts: Ready for further instructions.
- 🧠 Reflection: Successfully implemented complex multi-part updates to the spec, overcoming previous string matching issues by rewriting the file entirely. Ensured consistency across documentation.

## Evaluation notes (flywheel)

- Failure modes observed: Previous string matching issues with `Edit` tool for large multi-line blocks.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null

