---
name: quiz-master
description: Creates, administers, and grades educational quizzes with immediate feedback using rule-based evaluation systems. No LLM calls for grading.
---

# Quiz Master Skill

## Purpose
Creates, administers, and grades educational quizzes with immediate feedback using rule-based evaluation systems. Ensures deterministic, fair, and consistent grading without relying on LLM API calls.

## When to Use This Skill
- When a user wants to take a quiz or assessment
- When creating practice quizzes for educational content
- When providing formative assessment opportunities
- When offering immediate feedback on user responses
- When deterministic grading is required without AI dependencies

## Core Behaviors
1. **Rule-Based Grading**: Uses predefined answer keys and rubrics for grading
2. **Immediate Feedback**: Provides instant feedback on answers with explanations
3. **Educational Focus**: Focuses on reinforcing learning rather than just testing
4. **Consistent Scoring**: Maintains consistent grading standards across all users
5. **Detailed Explanations**: Explains both correct answers and why incorrect options are wrong

## Implementation Pattern
```
USER: Create a quiz about [topic] OR Take me through a quiz about [topic] OR Grade this response: [answer]

SKILL RESPONSE:
1. Quiz Creation: Generate quiz with questions and answer keys based on content
2. Quiz Administration: Present questions one at a time with clear instructions
3. Response Collection: Accept and validate user responses
4. Rule-Based Grading: Evaluate against stored answer keys and rubrics
5. Feedback Generation: Provide detailed feedback based on rule-based evaluation
6. Score Calculation: Compute score based on points assigned to correct answers
7. Improvement Suggestions: Recommend areas for improvement based on incorrect answers
8. Progress Tracking: Update learning progress based on quiz performance
```

## Algorithmic Approach

### 1. Quiz Creation
- Select questions from available content database
- Apply randomization to question order if needed
- Ensure balanced difficulty distribution
- Generate answer keys with point values

### 2. Rule-Based Grading
- **Multiple Choice**: Compare against correct answer keys
- **True/False**: Direct comparison with answer keys
- **Fill-in-the-Blank**: Exact match or close approximation scoring
- **Essay Questions**: Keyword matching and structural analysis against rubrics

### 3. Feedback Generation
- Identify specific areas where response was correct/incorrect
- Provide targeted suggestions for improvement
- Connect to relevant course materials for further study
- Highlight common misconceptions

### 4. Score Calculation
- Apply predetermined point values to each question
- Calculate weighted scores based on question difficulty
- Generate percentage-based overall scores
- Apply grading curves if configured

### 5. Quiz Administration
- Present questions in logical sequence
- Implement time limits if specified
- Track user's progress through quiz
- Validate responses before grading

## Quality Standards
- Maintain consistent scoring across all users
- Provide specific, actionable feedback
- Ensure grading aligns with educational objectives
- Identify and flag potential misconceptions
- Suggest specific next steps for improvement
- Use only deterministic algorithms (no LLM calls)
- Ensure fairness and reliability in grading
- Maintain security of answer keys and rubrics
- Provide clear explanations of scoring criteria