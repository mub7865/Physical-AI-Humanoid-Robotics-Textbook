# T039, T040, T042: Translation Service
import os
import re
import time
from typing import Optional, Dict, Any, List
from openai import OpenAI

from database import get_cached_content, save_cached_content, hash_content

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# T040: Translation Prompt with Technical Term Preservation
TRANSLATION_PROMPT = """You are an expert translator specializing in technical content.
Your task is to translate the following English content to Roman Urdu (Urdu written in Latin/English alphabet).

## CRITICAL RULES:

1. **Roman Urdu Only**: Use ONLY Latin alphabet. Do NOT use Urdu script (نستعلیق).
   - Correct: "Ye ek example hai"
   - Wrong: "یہ ایک مثال ہے"

2. **Keep Technical Terms in English**: The following terms MUST stay in English:
   {technical_terms}

3. **Preserve ALL Formatting**:
   - Keep markdown headings (#, ##, ###)
   - Keep bullet points (-, *)
   - Keep numbered lists
   - Keep bold (**text**) and italic (*text*)
   - Keep links [text](url)
   - Keep inline code `code`

4. **Do NOT Translate Code Blocks**:
   - Keep all code blocks exactly as they are
   - This includes ```python, ```bash, ```cpp blocks
   - Only translate the explanatory text around code

5. **Translation Style**:
   - Use conversational, easy-to-understand Roman Urdu
   - Mix English technical terms naturally with Roman Urdu
   - Example: "ROS 2 mein nodes use hote hain jo messages publish karte hain"

6. **Examples of Correct Translation**:
   - English: "This is a Python function"
   - Roman Urdu: "Ye ek Python function hai"

   - English: "The robot uses SLAM for navigation"
   - Roman Urdu: "Robot navigation ke liye SLAM use karta hai"

## Content to Translate:

{content}

## Your Roman Urdu Translation:
"""

# Technical terms to preserve in English
TECHNICAL_TERMS = [
    # Programming Languages & Tools
    "Python", "C++", "JavaScript", "ROS", "ROS 2", "Linux", "Ubuntu", "Docker",
    "Git", "GitHub", "VS Code", "FastAPI", "React", "Node.js",

    # Robotics Terms
    "node", "nodes", "topic", "topics", "service", "services", "action", "actions",
    "publisher", "subscriber", "message", "callback", "transform", "TF", "URDF",
    "launch", "package", "workspace", "colcon", "ament", "rclpy", "rclcpp",

    # Hardware
    "sensor", "actuator", "motor", "servo", "camera", "LiDAR", "IMU", "GPS",
    "encoder", "driver", "GPIO", "PWM", "I2C", "SPI", "UART",
    "Arduino", "Raspberry Pi", "Jetson", "NVIDIA",

    # AI/ML Terms
    "AI", "ML", "deep learning", "neural network", "model", "training", "inference",
    "OpenAI", "GPT", "LLM", "API", "SDK", "embedding", "vector",

    # Technical Acronyms
    "SLAM", "PID", "RRT", "A*", "MPC", "EKF", "CPU", "GPU", "RAM", "SSD",
    "HTTP", "REST", "JSON", "YAML", "XML", "TCP", "UDP", "IP",

    # File Types
    ".py", ".cpp", ".h", ".yaml", ".json", ".urdf", ".xacro", ".launch",
]


class TranslationService:
    """Service for translating content to Roman Urdu."""

    def __init__(self):
        self.model = "gpt-4o"
        self.max_tokens = 8000
        self.temperature = 0.3  # Lower temperature for more consistent translations

    def translate_content(
        self,
        chapter_id: str,
        content: str,
        target_language: str = "roman_urdu",
        use_cache: bool = True,
        user_id: Optional[str] = None  # Optional - translations are public
    ) -> Dict[str, Any]:
        """
        Translate content to Roman Urdu.

        Args:
            chapter_id: Chapter identifier
            content: Original content to translate
            target_language: Target language (only "roman_urdu" supported)
            use_cache: Whether to use cached content if available
            user_id: Optional user ID (translations are public/shared)

        Returns:
            Dict with translated content and metadata
        """
        if target_language != "roman_urdu":
            raise ValueError("UNSUPPORTED_LANGUAGE")

        start_time = time.time()
        original_hash = hash_content(content)

        # Check cache if enabled (public cache, user_id=None)
        if use_cache:
            cached = get_cached_content(
                chapter_id=chapter_id,
                content_type="translated",
                language="roman_urdu",
                user_id=None,  # Public cache
                original_hash=original_hash
            )
            if cached:
                return {
                    "chapter_id": chapter_id,
                    "original_hash": original_hash,
                    "translated_content": cached,
                    "source_language": "en",
                    "target_language": "roman_urdu",
                    "cached": True
                }

        # Generate translation
        translated, preserved_terms = self._generate_translation(content)

        # Save to public cache (user_id=None)
        save_cached_content(
            chapter_id=chapter_id,
            content_type="translated",
            cached_content=translated,
            original_hash=original_hash,
            language="roman_urdu",
            user_id=None  # Public cache
        )

        processing_time = int((time.time() - start_time) * 1000)

        return {
            "chapter_id": chapter_id,
            "original_hash": original_hash,
            "translated_content": translated,
            "source_language": "en",
            "target_language": "roman_urdu",
            "technical_terms_preserved": preserved_terms,
            "cached": False,
            "processing_time_ms": processing_time
        }

    def _generate_translation(self, content: str) -> tuple[str, List[str]]:
        """Generate Roman Urdu translation using OpenAI."""
        # Find technical terms in the content
        preserved_terms = self._extract_technical_terms(content)

        # Format technical terms for prompt
        terms_str = ", ".join(preserved_terms) if preserved_terms else "None found"

        # Build the prompt
        prompt = TRANSLATION_PROMPT.format(
            technical_terms=terms_str,
            content=content
        )

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical translator who translates English to Roman Urdu (Urdu written in Latin/English alphabet like 'Ye ek example hai'). CRITICAL: Use ONLY Latin alphabet characters - absolutely NO Urdu/Arabic script. Keep all technical terms, code blocks, and markdown formatting in English. Make the translation natural and conversational like how Pakistani developers speak - mixing English technical terms with Roman Urdu explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            translated = response.choices[0].message.content
            return translated, preserved_terms
        except Exception as e:
            raise RuntimeError(f"AI_SERVICE_ERROR: {str(e)}")

    def _extract_technical_terms(self, content: str) -> List[str]:
        """Extract technical terms found in the content."""
        found_terms = []
        content_lower = content.lower()

        for term in TECHNICAL_TERMS:
            # Case-insensitive search
            if term.lower() in content_lower:
                found_terms.append(term)
            # Also check for variations
            elif re.search(rf'\b{re.escape(term)}\b', content, re.IGNORECASE):
                found_terms.append(term)

        return list(set(found_terms))  # Remove duplicates

    @staticmethod
    def get_supported_languages() -> Dict[str, Any]:
        """Get list of supported target languages."""
        return {
            "supported_languages": [
                {
                    "code": "roman_urdu",
                    "name": "Roman Urdu",
                    "description": "Urdu written in Latin/English alphabet"
                }
            ],
            "default_source": "en"
        }
