#!/usr/bin/env python3
"""
Verification script to ensure zero LLM API calls in Phase 1 backend
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict

class ZeroLLMVerifier:
    """
    Verifies that the Phase 1 backend contains zero LLM API calls
    """
    def __init__(self):
        self.llm_patterns = [
            # OpenAI patterns
            r'openai\.',
            r'openai_',
            r'ChatCompletion',
            r'Completion',
            r'Embedding',
            r'Image',
            r'Model',

            # Anthropic patterns
            r'anthropic\.',
            r'anthropic_',
            r'Claude',
            r'messages\.create',
            r'client\.messages',

            # Cohere patterns
            r'cohere\.',
            r'cohere_',
            r'generate',

            # Hugging Face patterns
            r'transformers\.',
            r'HfApi',
            r'pipeline',
            r'AutoModel',
            r'AutoTokenizer',

            # Google patterns
            r'google\.generativelanguage',  # Gemini
            r'google_genai',

            # Other LLM services
            r'groq\.',
            r'perplexity\.',
            r'together\.',
            r'rePLICATE',

            # Vector databases (often used with RAG)
            r'pinecone',
            r'weaviate',
            r'chromadb',
            r'qdrant',
            r'faiss',

            # Embedding services
            r'embed',
            r'embedding',

            # Agent frameworks
            r'langchain',
            r'llama_index',
            r'autogen',
            r'crewai',
            r'agents',

            # RAG patterns
            r'rag',
            r'retrieval.*augment',
            r'augment.*retrieval',
            r'vector.*store',
            r'context.*window',
        ]

        self.file_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']
        self.ignored_dirs = {
            '.git', '.svn', '.hg', '__pycache__', 'node_modules',
            '.venv', 'venv', 'env', 'dist', 'build', '.next',
            'target', 'obj', 'bin', 'out', '.terraform'
        }

    def scan_directory(self, directory: str) -> List[Dict]:
        """
        Scan a directory for LLM API calls
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
        Scan a single file for LLM API calls
        """
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for i, pattern in enumerate(self.llm_patterns):
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

                    violations.append({
                        'file': file_path,
                        'line_number': line_number,
                        'pattern': pattern,
                        'matched_text': match.group(0),
                        'line_content': line_content,
                        'severity': 'critical' if i < 10 else 'high'  # First 10 patterns are more critical
                    })
        except Exception as e:
            print(f"Error scanning file {file_path}: {str(e)}")

        return violations

    def verify_compliance(self, project_path: str) -> Dict:
        """
        Verify that the project complies with zero LLM API calls
        """
        print(f"🔍 Scanning {project_path} for LLM API calls...")

        violations = self.scan_directory(project_path)

        result = {
            'compliant': len(violations) == 0,
            'total_violations': len(violations),
            'violations': violations,
            'project_path': project_path
        }

        if violations:
            print(f"\n❌ FOUND {len(violations)} potential LLM API calls:")
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
        print("Usage: python verify_zero_llm.py <path_to_scan>")
        print("Example: python verify_zero_llm.py /path/to/project")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"Error: Path {project_path} does not exist!")
        sys.exit(1)

    verifier = ZeroLLMVerifier()
    result = verifier.verify_compliance(project_path)

    # Exit with error code if violations found
    if not result['compliant']:
        print(f"\n❌ Compliance check FAILED: {result['total_violations']} violations found")
        sys.exit(1)
    else:
        print(f"\n✅ Compliance check PASSED: Zero LLM API calls detected")
        sys.exit(0)

if __name__ == "__main__":
    main()