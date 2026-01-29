#!/usr/bin/env python3
"""
LLM API Scanner
Scans codebase for any LLM API calls to ensure zero-backend-LLM compliance
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict

class LLMScanner:
    """
    Scans for LLM API calls in codebase
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

            # Other LLM services
            r'google\.generativelanguage',  # Gemini
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
            r'context.*window',
        ]

        self.file_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.java', '.cpp', '.rb', '.php']
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
                        'severity': 'high' if i < 10 else 'medium'  # First 10 patterns are more critical
                    })
        except Exception as e:
            print(f"Error scanning file {file_path}: {str(e)}")

        return violations

    def scan_content(self, content: str, file_path: str = "unknown") -> List[Dict]:
        """
        Scan content string for LLM API calls
        """
        violations = []

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
                    'severity': 'high' if i < 10 else 'medium'
                })

        return violations

def main():
    if len(sys.argv) < 2:
        print("Usage: python llm_scanner.py <directory_to_scan>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist!")
        sys.exit(1)

    print(f"🔍 Scanning {directory} for LLM API calls...")

    scanner = LLMScanner()
    violations = scanner.scan_directory(directory)

    if violations:
        print(f"\n❌ Found {len(violations)} potential LLM API calls!")
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
        sys.exit(1)  # Exit with error code to indicate non-compliance
    else:
        print(f"\n✅ No LLM API calls found in {directory}")
        print("🎉 The codebase is zero-backend-LLM compliant!")
        sys.exit(0)  # Exit successfully

if __name__ == "__main__":
    main()