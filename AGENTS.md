# Dexterous Hand Atlas - Agent Instructions

## Project Overview

This project builds a technical knowledge website/database for robotic dexterous hands.

The goal is not to create a simple product catalog, but a structured technical atlas covering:

- robotic hand hardware
- mechanical architecture
- actuation methods
- sensing systems
- control algorithms
- simulation resources
- open-source models
- academic papers
- industrial applications
- engineering trade-offs

The target users are:

- robotics researchers
- robotic engineers
- students
- job candidates in embodied AI and robotics companies


---

# Core Principles

## 1. Evidence-based information

All technical statements should be linked to sources.

Information priority:

1. Official company documentation
2. Peer-reviewed papers
3. Technical reports
4. GitHub repositories
5. Conference videos
6. Community discussions

Avoid unsupported statements.

Do not write:

"XXX hand is bad."

Instead write:

"Several studies report challenges related to XXX, mainly caused by XXX."

Always distinguish:

- fact
- reported limitation
- engineering interpretation


---

# Data Organization

Each robotic hand should contain:

## Basic Information

- Name
- Company / Institution
- Country
- Release year
- Application
- Product status


## Mechanical System

- Number of fingers
- Degrees of freedom
- Actuation method
- Transmission mechanism
- Weight
- Size
- Materials
- Structural characteristics


## Sensing System

Include:

- position sensing
- force sensing
- tactile sensing
- vision integration
- proprioception


## Control System

Include:

- PID control
- impedance control
- force control
- model-based control
- learning-based control
- teleoperation


## Simulation and Software

Record:

- URDF
- MJCF
- MuJoCo model
- Isaac Sim model
- ROS packages
- GitHub repositories
- SDK


## Resources

Every hand should collect:

- official website
- papers
- technical documents
- CAD/model resources
- code repositories
- datasets
- demo videos
- images


## Engineering Analysis

Each hand should include:

### Advantages

Why was this design chosen?

### Limitations

What technical challenges remain?

### Application Suitability

Examples:

- research platform
- industrial manipulation
- humanoid robot
- robot learning


---

# Website Requirements

The website should prioritize:

- clean technical documentation style
- fast loading
- searchable content
- modular expansion

Preferred technology:

First version:

- Markdown based
- MkDocs Material
- local deployment

Future:

- GitHub Pages
- static hosting


---

# Coding Rules

## Before modifying files

First inspect:

- existing directory structure
- current configuration
- existing components


Do not overwrite existing work without checking.


## Code style

Prefer:

- simple
- maintainable
- documented

Avoid unnecessary complexity.


## File naming

Use:

lowercase-with-hyphen

Examples:

```
shadow-hand.md
leap-hand.md
xynova-flex2.md
```

---

# Long-term Vision

The final project should become:

"Dexterous Hand Atlas"

A technical map connecting:

mechanical design

↓

actuation

↓

sensing

↓

control

↓

robot learning

↓

embodied intelligence

The project should demonstrate system-level understanding of robotic manipulation.