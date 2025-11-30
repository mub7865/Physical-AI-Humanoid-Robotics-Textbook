import os

def create_book_structure(syllabus_path, output_base_path):
    with open(syllabus_path, 'r') as f:
        syllabus_content = f.readlines()

    current_chapter = None
    for line in syllabus_content:
        if line.startswith('# '):  # Main chapter
            chapter_title = line.strip('# ').strip()
            chapter_slug = chapter_title.lower().replace(' ', '-')
            chapter_dir = os.path.join(output_base_path, chapter_slug)
            os.makedirs(chapter_dir, exist_ok=True)
            current_chapter = chapter_dir
            # Create index.md for chapter
            with open(os.path.join(chapter_dir, 'index.md'), 'w') as f:
                f.write(f'# {chapter_title}\n\n')
        elif line.startswith('## ') and current_chapter:  # Section within chapter
            section_title = line.strip('## ').strip()
            section_slug = section_title.lower().replace(' ', '-')
            with open(os.path.join(current_chapter, f'{section_slug}.md'), 'w') as f:
                f.write(f'# {section_title}\n\n')
        # Add logic to generate sidebars.ts (placeholder for now)
    print(f"Generated book structure in {output_base_path}")

if __name__ == "__main__":
    syllabus_path = "specs/input/syllabus.md"
    output_base_path = "book/docs/"
    create_book_structure(syllabus_path, output_base_path)