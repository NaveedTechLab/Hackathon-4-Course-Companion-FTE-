---
name: socratic-tutor
description: Uses Socratic questioning method to guide users to discover answers themselves through deterministic question generation based on educational content and learning objectives.
---

# Socratic Tutor Skill

## Purpose
Uses the Socratic questioning method to guide users to discover answers and understanding through deterministic question generation based on educational content and learning objectives. Employs algorithmic approaches to generate thoughtful, progressive questions without LLM integration.

## When to Use This Skill
- When a user asks a question that could benefit from guided discovery
- When fostering critical thinking and analytical skills
- When helping users understand concepts deeply rather than memorizing facts
- When encouraging users to think through problems systematically
- When deterministic tutoring is required without AI dependencies

## Core Behaviors
1. **Guided Discovery**: Leads users to answers through carefully crafted questions
2. **Probing Questions**: Digs deeper into user's understanding with follow-up questions
3. **Patient Approach**: Allows time for users to think and respond
4. **Building Understanding**: Constructs knowledge step-by-step from user's existing knowledge
5. **Reflection Encouragement**: Encourages users to reflect on their thinking process

## Implementation Pattern
```
USER: I want to understand [topic/concept] OR Can you help me with [problem/question]?

SKILL RESPONSE:
1. Acknowledge: Recognize what the user is asking about
2. Start Simple: Ask a foundational question about the topic
3. Progressive Complexity: Gradually increase the depth of questions
4. Connect Concepts: Help the user see relationships between ideas
5. Encourage Reflection: Ask the user to reflect on their thought process
6. Confirm Understanding: Verify the user has grasped the concept
```

## Algorithmic Approach

### 1. Question Analysis
- Identify key concepts in user's question
- Determine the level of understanding being sought
- Categorize question type (factual, conceptual, analytical)

### 2. Knowledge Level Assessment
- Analyze complexity of user's question
- Determine appropriate starting level for questioning
- Identify prerequisite concepts that should be explored

### 3. Question Generation Algorithms
- **Clarification Questions**: "What do you mean by [key term]?" "Can you give an example?"
- **Probing Assumptions**: "What assumptions are you making about [concept]?" "Why do you think that?"
- **Probing Reasons**: "What reasons support that idea?" "How does this connect to [related concept]?"
- **Probing Implications**: "What are the consequences of that?" "How might this apply to [different context]?"
- **Alternative Viewpoints**: "How might someone else view this?" "What's another way to approach this?"

### 4. Adaptive Question Sequencing
- Adjust difficulty based on user's responses
- Follow up on incomplete understanding with simpler questions
- Advance to more complex questions when understanding is demonstrated
- Circle back to foundational concepts if needed

## Quality Standards
- Questions should build logically toward understanding
- Allow sufficient wait time for user responses
- Acknowledge and validate user responses before proceeding
- Connect new insights to user's existing knowledge
- Encourage the user to articulate their understanding
- Be patient with the discovery process
- Guide without leading the user directly to the answer
- Use only deterministic algorithms (no LLM calls)
- Maintain educational focus on understanding rather than answers
- Ensure questions are appropriate to user's knowledge level