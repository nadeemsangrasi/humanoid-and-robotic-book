# Specification-Driven Development (Spec-Kit Plus) for Physical AI & Humanoid Robotics Textbook

This directory contains templates, scripts, and configurations for the specification-driven development of the Physical AI & Humanoid Robotics textbook.

## Directory Structure

- `templates/` - Content templates for generating textbook chapters
- `scripts/` - Scripts for automating content generation workflows
- `memory/` - Project constitution and principles

## Content Generation Workflow

The workflow for generating textbook content from specifications follows these steps:

1. Create granular specification files (`.spec.md`) that define learning objectives, concepts, and content requirements
2. Use the generation script to convert specifications into MDX content based on templates
3. Review and refine the generated content
4. Integrate with the Docusaurus documentation system

### Running the Content Generation Script

```bash
# Generate MDX content from specifications
./.specify/scripts/generate-mdx-from-specs.sh [input_dir] [output_dir]

# Example:
./.specify/scripts/generate-mdx-from-specs.sh specs/ docs/
```

### Chapter Template

The `chapter-template.mdx` provides a consistent structure for all textbook chapters, including:

- Learning objectives
- Theoretical background
- Practical implementation
- Diagrams and visualizations
- Conceptual code examples
- Step-by-step tutorials
- Troubleshooting guides
- Hands-on exercises
- Summary and further reading

## Project Constitution

The project constitution in `memory/constitution.md` outlines the principles and guidelines for developing this textbook, including the "Zero Hallucination" principle and content standards.