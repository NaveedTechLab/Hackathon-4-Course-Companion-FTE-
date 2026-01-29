#!/usr/bin/env python3
"""
Final verification script to ensure zero LLM API calls in Phase 1 backend
Focuses only on actual application code, excluding verification tools
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

class FinalZeroLLMVerifier:
    """
    Final verifier that focuses only on application code and excludes verification tools
    """
    def __init__(self):
        # Specific LLM API call patterns (these are actual violations)
        self.llm_api_patterns = [
            # OpenAI API calls
            r'openai\.(ChatCompletion|Completion|Image|Embedding)',
            r'openai\.',
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
            r'pipeline\(',
            r'AutoModel\(',
            r'AutoTokenizer\(',

            # Google Gemini
            r'google\.generativelanguage',
            r'genai\.',

            # Vector databases (used with RAG)
            r'pinecone\.',
            r'weaviate\.',
            r'chromadb\.',
            r'qdrant\.',
            r'faiss\.',

            # Embedding services
            r'embeddings\.',
            r'client\.embeddings',

            # Agent frameworks
            r'langchain\.',
            r'llama_index\.',
            r'autogen\.',
            r'crewai\.',
        ]

        self.file_extensions = ['.py']
        self.ignored_dirs = {
            '.git', '.svn', '.hg', '__pycache__', 'node_modules',
            '.venv', 'venv', 'env', 'dist', 'build', '.next',
            'target', 'obj', 'bin', 'out', '.terraform'
        }

    def scan_directory(self, directory: str) -> List[Dict]:
        """
        Scan a directory for actual LLM API calls, excluding verification tools
        """
        violations = []

        for root, dirs, files in os.walk(directory):
            # Remove ignored directories from the search
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)

                    # Skip files in tools directory (verification scripts)
                    if '/tools/' in file_path or '\\tools\\' in file_path:
                        continue

                    # Skip files in skills directory as those are supposed to use LLMs
                    if '/skills/' in file_path or '\\skills\\' in file_path:
                        continue

                    file_violations = self.scan_file(file_path)
                    violations.extend(file_violations)

        return violations

    def scan_file(self, file_path: str) -> List[Dict]:
        """
        Scan a single file for actual LLM API calls
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

                    # Filter out comment lines that mention these patterns
                    if line_content.strip().startswith('#'):
                        continue

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

    def verify_compliance(self, project_path: str) -> Dict:
        """
        Verify that the project complies with zero LLM API calls
        """
        print(f"🔍 Scanning {project_path} for LLM API calls (final verification)...")

        violations = self.scan_directory(project_path)

        result = {
            'compliant': len(violations) == 0,
            'total_violations': len(violations),
            'violations': violations,
            'project_path': project_path,
            'message': 'Final scanning completed'
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
        print("Usage: python final_verify_zero_llm.py <path_to_scan>")
        print("Example: python final_verify_zero_llm.py /path/to/project")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist!")
        sys.exit(1)

    verifier = FinalZeroLLMVerifier()
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