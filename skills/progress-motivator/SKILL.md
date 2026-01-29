---
name: progress-motivator
description: Tracks and motivates learning progress with streaks, achievements, and personalized encouragement using deterministic algorithms to generate motivational content based on user progress data.
---

# Progress Motivator Skill

## Purpose
Tracks and motivates learning progress with streaks, achievements, and personalized encouragement using deterministic algorithms to generate motivational content based on user progress data. Provides consistent, data-driven motivation without LLM integration.

## When to Use This Skill
- When providing progress updates to users
- When encouraging continued learning activity
- When celebrating achievements and milestones
- When identifying and addressing learning plateaus
- When providing personalized motivation based on user behavior
- When deterministic motivation is required without AI dependencies

## Core Behaviors
1. **Progress Tracking**: Monitors and records learning activities and achievements
2. **Streak Maintenance**: Tracks and encourages consistent learning habits
3. **Personalized Encouragement**: Provides tailored motivational messages based on user data
4. **Achievement Recognition**: Celebrates milestones and accomplishments
5. **Engagement Recovery**: Reaches out when users show signs of disengagement

## Implementation Pattern
```
USER: How am I doing? OR What's my progress? OR I'm feeling stuck

SKILL RESPONSE:
1. Progress Summary: Provide current status with metrics and achievements
2. Streak Status: Report current learning streak and days active
3. Milestone Recognition: Highlight recent achievements or upcoming goals
4. Personalized Motivation: Offer encouragement based on user's learning pattern
5. Suggested Next Steps: Recommend specific next actions based on progress
6. Gamification Elements: Use badges, points, or challenges if appropriate
```

## Algorithmic Approach

### 1. Progress Analysis
- Calculate completion percentages across courses/content
- Track learning consistency and time spent
- Identify patterns in learning behavior
- Measure engagement levels over time periods

### 2. Streak Calculation
- Determine consecutive learning days
- Identify optimal learning windows for user
- Calculate streak value and significance
- Flag streak maintenance opportunities

### 3. Motivational Message Generation
- **Achievement Messages**: "Congratulations on completing [X]! You're doing great!"
- **Streak Messages**: "Amazing! You've maintained your learning streak for [X] days!"
- **Progress Messages**: "You're [X]% through this course. Keep up the excellent work!"
- **Encouragement Messages**: "You're making steady progress. Remember, learning is a journey!"
- **Recovery Messages**: "We noticed you haven't been studying lately. Pick up where you left off!"

### 4. Achievement System
- Course completion badges
- Streak achievement medals
- Time-based milestones (hours learned)
- Difficulty-based achievements (completed advanced content)
- Consistency rewards (regular study patterns)

### 5. Suggestion Algorithms
- Recommend content based on incomplete sections
- Suggest next logical course based on progress
- Propose review sessions for low-scoring areas
- Identify optimal study times based on user patterns

## Quality Standards
- Use positive, encouraging language consistently
- Base encouragement on actual progress and achievements
- Personalize motivation to the individual user's progress
- Balance celebration of wins with constructive guidance
- Respect user's autonomy in learning choices
- Provide actionable next steps based on data
- Maintain consistency in motivation approach
- Use only deterministic algorithms (no LLM calls)
- Ensure privacy of learning data
- Adapt tone to user's engagement level and progress