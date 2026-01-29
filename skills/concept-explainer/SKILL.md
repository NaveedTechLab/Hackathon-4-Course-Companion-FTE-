---
name: concept-explainer
description: Explains educational concepts in a clear, step-by-step manner with examples and analogies. Uses deterministic algorithms to generate explanations based on available content.
---

# Concept Explainer Skill

## Purpose
Explains educational concepts in a clear, step-by-step manner using examples, analogies, and visual descriptions to aid understanding. Uses deterministic algorithms to generate explanations based on available content without relying on LLM APIs.

## When to Use This Skill
- When a user asks for clarification of a concept
- When explaining theoretical principles
- When providing educational content in an accessible way
- When breaking down complex topics into digestible parts
- When deterministic explanations are needed without LLM dependencies

## Core Behaviors
1. **Clarity First**: Always explain concepts in the simplest terms possible
2. **Structured Approach**: Break concepts into logical, sequential steps
3. **Use Examples**: Provide concrete examples from available course content
4. **Employ Analogies**: Use familiar concepts to explain unfamiliar ones
5. **Encourage Questions**: Invite users to ask for clarification on any part

## Implementation Pattern
```
USER: Explain [concept]

SKILL RESPONSE:
1. Definition: Provide a clear, concise definition of the concept
2. Context: Explain where and why this concept is important
3. Breakdown: Decompose the concept into smaller parts/components
4. Examples: Give 2-3 concrete examples of the concept in action
5. Analogies: Provide relatable analogies to help visualize the concept
6. Applications: Describe practical applications of the concept
7. Common Mistakes: Highlight misconceptions or common errors
8. Further Reading: Suggest related concepts to explore
```

## Algorithmic Approach

### 1. Content Search and Retrieval
- Use keyword matching to find relevant content
- Apply relevance scoring based on term frequency
- Rank results by conceptual proximity
- Extract examples and analogies from course materials

### 2. Explanation Structure Generation
- Definition section with clear terminology
- Context section explaining relevance
- Component breakdown with step-by-step elements
- Examples section with concrete illustrations
- Application section with practical use cases
- Summary with key takeaways

### 3. Example Generation
- Extract examples from available course content
- Match examples to the concept being explained
- Rank examples by relevance and clarity
- Format examples consistently

### 4. Analogy Creation
- Identify related concepts from course materials
- Find structural or functional similarities
- Create comparisons that illuminate the concept
- Use familiar concepts as reference points

## Quality Standards
- Use language appropriate to the user's knowledge level
- Provide multiple ways to understand the same concept
- Include examples drawn from available course content
- Connect new concepts to previously learned material
- End with a summary of key points
- Ensure all content comes from deterministic sources (no AI-generated content)
- Maintain educational accuracy based on available materials
- Follow accessibility guidelines for educational content