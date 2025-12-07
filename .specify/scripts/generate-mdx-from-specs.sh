#!/bin/bash
# Script to generate MDX content from Spec-Kit specifications
# This script demonstrates a workflow for generating MDX content from granular specifications

set -e  # Exit on any error

# Configuration
SPEC_DIR="${1:-specs}"
OUTPUT_DIR="${2:-docs}"
TEMPLATE_FILE=".specify/templates/chapter-template.mdx"

# Validate inputs
if [ ! -d "$SPEC_DIR" ]; then
    echo "Error: Specification directory '$SPEC_DIR' does not exist"
    exit 1
fi

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: Template file '$TEMPLATE_FILE' does not exist"
    exit 1
fi

echo "Starting MDX content generation from specifications in: $SPEC_DIR"
echo "Output will be placed in: $OUTPUT_DIR"
echo "Using template: $TEMPLATE_FILE"
echo ""

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Find all spec files and generate MDX content
find "$SPEC_DIR" -name "*.spec.md" -type f | while read spec_file; do
    echo "Processing spec file: $spec_file"

    # Extract spec name without extension
    spec_name=$(basename "$spec_file" .spec.md)
    spec_dir=$(dirname "$spec_file")

    # Determine output path based on spec structure
    # If spec is in a subdirectory like specs/module1/chapter1.spec.md
    # Output goes to docs/module1/chapter1.mdx
    relative_path=$(realpath --relative-to="$SPEC_DIR" "$spec_dir")
    output_path="$OUTPUT_DIR/$relative_path"
    output_file="$output_path/$spec_name.mdx"

    # Create output directory
    mkdir -p "$output_path"

    # Generate MDX content from template and spec
    # This is a simplified example - in a real implementation, you would
    # parse the spec file and populate the template with specific content

    # For now, we'll just copy the template with placeholders
    # A more sophisticated implementation would parse the spec and fill in the template
    cp "$TEMPLATE_FILE" "$output_file"

    # Replace placeholders in the generated file with basic info from spec
    sed -i "s/{{CHAPTER_TITLE}}/$spec_name/g" "$output_file"
    sed -i "s/{{MODULE_PATH}}/$relative_path/g" "$output_file"
    sed -i "s/{{CHAPTER_SLUG}}/$spec_name/g" "$output_file"
    sed -i "s/{{SIDEBAR_POSITION}}/1/g" "$output_file"

    echo "  Generated: $output_file"
done

echo ""
echo "MDX content generation completed!"
echo "Check the '$OUTPUT_DIR' directory for generated content."