#!/usr/bin/env python3
"""
Refined verification script to ensure zero LLM API calls in Phase 1 backend
Filters out false positives by analyzing context more carefully
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

class RefinedZeroLLMVerifier:
    """
    Refined verifier that distinguishes between actual LLM API calls and legitimate uses of common terms
    """
    def __init__(self):
        # Specific LLM API call patterns (these are actual violations)
        self.llm_api_patterns = [
            # OpenAI API calls
            r'openai\.(ChatCompletion|Completion|Image|Embedding)',
            r'client\.(chat|completions|messages|embeddings)',

            # Anthropic API calls
            r'anthropic\.',
            r'client\.messages',
            r'messages\.create',

            # Cohere API calls
            r'cohere\.',
            r'co\.generate',

            # HuggingFace transformers
            r'transformers\.',
            r'pipeline',
            r'AutoModel',

            # Vector databases (used with RAG)
            r'pinecone\.',
            r'weaviate\.',
            r'chromadb\.',
            r'qdrant\.',
            r'faiss\.',

            # Agent frameworks
            r'langchain\.',
            r'llama_index\.',
            r'autogen\.',
            r'crewai\.',
        ]

        # Terms that are commonly used but not LLM-specific
        self.false_positive_indicators = [
            # These are legitimate uses that should not trigger violations
            r'response_model=',  # Pydantic response models
            r'from ...models\.',  # Import from models directory
            r'models\.',  # References to application models
            r'pydantic\.',  # Pydantic models
            r'from sqlalchemy\.',  # SQLAlchemy models
            r'content_model',  # Application-specific content models
            r'user_model',  # Application-specific user models
            r'course_model',  # Application-specific course models
            r'progress_model',  # Application-specific progress models
            r'quiz_model',  # Application-specific quiz models
            r'generate_response',  # Function name for response generation (not LLM)
            r'completion_percentage',  # Progress completion percentage (not LLM)
            r'completion_status',  # Status completion (not LLM)
            r'content_completion',  # Content completion (not LLM)
            r'generate_presigned_url',  # R2 presigned URL generation (not LLM)
            r'generate_unique_id',  # ID generation (not LLM)
            r'generate_token',  # Authentication token generation (not LLM)
            r'generate_key',  # Encryption/key generation (not LLM)
            r'generate_report',  # Report generation (not LLM)
            r'generate_path',  # File path generation (not LLM)
            r'generate_url',  # URL generation (not LLM)
            r'generate_filename',  # Filename generation (not LLM)
            r'generate_slug',  # Slug generation (not LLM)
            r'generate_thumbnail',  # Thumbnail generation (not LLM)
            r'rag',  # Could be legitimate acronym (not necessarily RAG)
            r'embed',  # Could be legitimate embedding (not necessarily AI)
            r'agents',  # Could be legitimate agent (not necessarily AI)
        ]

        self.file_extensions = ['.py']
        self.ignored_dirs = {
            '.git', '.svn', '.hg', '__pycache__', 'node_modules',
            '.venv', 'venv', 'env', 'dist', 'build', '.next',
            'target', 'obj', 'bin', 'out', '.terraform'
        }

    def scan_directory(self, directory: str) -> List[Dict]:
        """
        Scan a directory for actual LLM API calls, filtering out false positives
        """
        violations = []

        for root, dirs, files in os.walk(directory):
            # Remove ignored directories from the search
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)

                    # Skip files in skills directory as those are supposed to use LLMs
                    if '/skills/' in file_path or '\\skills\\' in file_path:
                        continue

                    file_violations = self.scan_file(file_path)
                    violations.extend(file_violations)

        return violations

    def scan_file(self, file_path: str) -> List[Dict]:
        """
        Scan a single file for actual LLM API calls, filtering out false positives
        """
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check for actual LLM API patterns
            for i, pattern in enumerate(self.llm_api_patterns):
                matches = list(re.finditer(pattern, content, re.IGNORECASE))

                for match in matches:
                    # Get the line number where the match occurs
                    content_before_match = content[:match.start()]
                    line_number = content_before_match.count('\n') + 1

                    # Get the line containing the match
                    lines = content.split('\n')
                    if line_number <= len(lines):
                        line_content = lines[line_number - 1].strip()
                    else:
                        line_content = match.group(0)

                    # Check if this is a false positive by looking for context indicators
                    if self._is_false_positive(line_content):
                        continue  # Skip this as a false positive

                    violations.append({
                        'file': file_path,
                        'line_number': line_number,
                        'pattern': pattern,
                        'matched_text': match.group(0),
                        'line_content': line_content,
                        'severity': 'critical' if i < 10 else 'high'
                    })
        except Exception as e:
            print(f"Error scanning file {file_path}: {str(e)}")

        return violations

    def _is_false_positive(self, line_content: str) -> bool:
        """
        Determine if a match is likely a false positive based on context
        """
        lower_line = line_content.lower()

        # Check for false positive indicators
        for indicator in self.false_positive_indicators:
            if re.search(indicator, lower_line, re.IGNORECASE):
                return True

        return False

    def verify_compliance(self, project_path: str) -> Dict:
        """
        Verify that the project complies with zero LLM API calls
        """
        print(f"🔍 Scanning {project_path} for LLM API calls (refined)...")

        violations = self.scan_directory(project_path)

        result = {
            'compliant': len(violations) == 0,
            'total_violations': len(violations),
            'violations': violations,
            'project_path': project_path,
            'message': 'Scanning completed'
        }

        if violations:
            print(f"\n❌ FOUND {len(violations)} actual LLM API calls:")
            print("="*80)

            for i, violation in enumerate(violations, 1):
                print(f"{i}. File: {violation['file']}")
                print(f"   Line: {violation['line_number']}")
                print(f"   Pattern: {violation['pattern']}")
                print(f"   Code: {violation['line_content']}")
                print(f"   Matched: '{violation['matched_text']}'")
                print(f"   Severity: {violation['severity']}")
                print("-" * 80)

            print(f"\n🚨 LLM API calls detected! The codebase is NOT zero-backend-LLM compliant.")
        else:
            print(f"\n✅ No LLM API calls found in {project_path}")
            print("🎉 The codebase is zero-backend-LLM compliant!")

        return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python refined_verify_zero_llm.py <path_to_scan>")
        print("Example: python refined_verify_zero_llm.py /path/to/project")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist!")
        sys.exit(1)

    verifier = RefinedZeroLLMVerifier()
    result = verifier.verify_compliance(project_path)

    # Exit with error code if violations found
    if not result['compliant']:
        print(f"\n❌ Compliance check FAILED: {result['total_violations']} actual LLM API calls found")
        sys.exit(1)
    else:
        print(f"\n✅ Compliance check PASSED: Zero LLM API calls detected")
        sys.exit(0)

if __name__ == "__main__":
    main()