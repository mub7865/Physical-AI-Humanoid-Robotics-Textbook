# T031, T032, T034: Personalization Service
import os
import time
from typing import Optional, Dict, Any
from openai import OpenAI

from database import (
    get_cached_content, save_cached_content, hash_content,
    get_user_profile
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# T032: Personalization Prompt Templates
PERSONALIZATION_PROMPT = """You are an expert educator specializing in robotics and AI.
Your task is to personalize the following educational content based on the learner's profile.

## Learner Profile:
- Software Development Experience: {software_exp}
- Hardware/Electronics Experience: {hardware_exp}
- Robotics Background: {robotics_bg}
- Known Programming Languages: {languages}
- Learning Goals: {learning_goals}

## Personalization Guidelines:

### For Software Experience Level:
- **Beginner**: Add more code explanations, explain syntax basics, use real-world analogies, add "What this means" sections
- **Intermediate**: Standard explanations with some context, assume basic programming knowledge
- **Expert**: Skip basics, focus on advanced concepts, be concise, reference design patterns

### For Hardware Experience:
- **None**: Explain electronics basics, avoid hardware assumptions, use software analogies
- **Arduino/Raspberry Pi**: Reference familiar platforms like GPIO, PWM, use hobbyist terminology
- **Jetson/Industrial**: Use professional terminology, assume embedded systems knowledge

### For Robotics Background:
- **Student**: Academic tone, theory focus, add exercises and study questions
- **Hobbyist**: Practical focus, project ideas, tips and tricks, hands-on approach
- **Professional**: Industry context, best practices, efficiency and reliability focus

## Rules:
1. Keep the ENTIRE response in ENGLISH only - do NOT use any other language
2. Keep ALL technical terms in English (ROS 2, Python, nodes, topics, etc.)
3. Preserve ALL markdown formatting (headings, lists, code blocks, links)
4. Do NOT modify code examples - keep them exactly as they are
5. Add helpful analogies or examples appropriate for the learner's level
6. Maintain the same overall structure but adjust depth and complexity
7. IMPORTANT: This is personalization by EXPERIENCE LEVEL, not translation. Output must be in English.

## Original Content to Personalize:

{content}

## Your Personalized Version:
"""


class PersonalizationService:
    """Service for personalizing content based on user profiles."""

    def __init__(self):
        self.model = "gpt-4o"
        self.max_tokens = 8000
        self.temperature = 0.7

    def personalize_content(
        self,
        user_id: str,
        chapter_id: str,
        content: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Personalize content based on user's profile.

        Args:
            user_id: The user's ID
            chapter_id: Chapter identifier
            content: Original content to personalize
            use_cache: Whether to use cached content if available

        Returns:
            Dict with personalized content and metadata
        """
        start_time = time.time()
        original_hash = hash_content(content)

        # Get user profile
        profile = get_user_profile(user_id)
        if not profile:
            raise ValueError("PROFILE_NOT_FOUND")

        # Check cache if enabled
        if use_cache:
            cached = get_cached_content(
                chapter_id=chapter_id,
                content_type="personalized",
                language="en",
                user_id=user_id,
                original_hash=original_hash
            )
            if cached:
                return {
                    "chapter_id": chapter_id,
                    "original_hash": original_hash,
                    "personalized_content": cached,
                    "profile_used": {
                        "software_exp": profile["software_exp"],
                        "hardware_exp": profile["hardware_exp"],
                        "robotics_bg": profile["robotics_bg"]
                    },
                    "cached": True
                }

        # Generate personalized content
        personalized = self._generate_personalized(content, profile)

        # Save to cache
        save_cached_content(
            chapter_id=chapter_id,
            content_type="personalized",
            cached_content=personalized,
            original_hash=original_hash,
            language="en",
            user_id=user_id
        )

        processing_time = int((time.time() - start_time) * 1000)

        return {
            "chapter_id": chapter_id,
            "original_hash": original_hash,
            "personalized_content": personalized,
            "profile_used": {
                "software_exp": profile["software_exp"],
                "hardware_exp": profile["hardware_exp"],
                "robotics_bg": profile["robotics_bg"]
            },
            "cached": False,
            "processing_time_ms": processing_time
        }

    def _generate_personalized(self, content: str, profile: Dict[str, Any]) -> str:
        """Generate personalized content using OpenAI."""
        # Format languages list
        languages = profile.get("languages", ["python"])
        if isinstance(languages, list):
            languages_str = ", ".join(languages)
        else:
            languages_str = str(languages)

        # Build the prompt
        prompt = PERSONALIZATION_PROMPT.format(
            software_exp=self._format_exp_level(profile["software_exp"], "software"),
            hardware_exp=self._format_exp_level(profile["hardware_exp"], "hardware"),
            robotics_bg=self._format_exp_level(profile["robotics_bg"], "robotics"),
            languages=languages_str,
            learning_goals=profile.get("learning_goals") or "Not specified",
            content=content
        )

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educator who personalizes robotics content based on user experience level. Always respond in ENGLISH only. Preserve all markdown formatting and code blocks. Do NOT translate - only adjust complexity and explanations for the user's level."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"AI_SERVICE_ERROR: {str(e)}")

    def _format_exp_level(self, value: str, category: str) -> str:
        """Format experience level for prompt."""
        labels = {
            "software": {
                "beginner": "Beginner (just starting to learn programming)",
                "intermediate": "Intermediate (comfortable with basic projects)",
                "expert": "Expert (professional developer experience)"
            },
            "hardware": {
                "none": "None (software-only background)",
                "arduino_rpi": "Arduino/Raspberry Pi level (hobby electronics)",
                "jetson_industrial": "Jetson/Industrial level (advanced embedded systems)"
            },
            "robotics": {
                "student": "Student (learning robotics in academic setting)",
                "hobbyist": "Hobbyist (personal robotics projects)",
                "professional": "Professional (industry work experience)"
            }
        }
        return labels.get(category, {}).get(value, value)
