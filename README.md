# Autonomous Supply Chain Disruption Monitor

## Project Overview

The Autonomous Supply Chain Disruption Monitor is a Generative AI-based system designed to identify and classify global supply chain risks from real-time logistics news.

The system collects disruption-related news articles, processes the data, classifies potential supply chain threats, and generates a structured disruption report.

---

## Week 1 Objective

### Web Search Integration and Disruption Classification

The Week 1 implementation focuses on:

- Fetching recent logistics and supply chain news.
- Processing and cleaning retrieved articles.
- Classifying disruption events.
- Generating structured supply chain risk reports.

---

## Week 1 Workflow

---

## Features Implemented

### 1. News Fetching

- Integrated DDGS search engine.
- Retrieves recent logistics and supply chain disruption news.
- Extracts:
  - Title
  - URL
  - Summary

---

### 2. Data Processing

- Cleans fetched news data.
- Removes incomplete records.
- Converts data into structured Pydantic models.

---

### 3. Disruption Classification

The system classifies news into categories:

- Natural Disaster
- Labor Strike
- Geopolitical Conflict
- Transportation Delay
- Safe

Severity levels:

- Low
- Medium
- High
- Critical

---

### 4. Structured Data Validation

Implemented Pydantic models:

- NewsArticle
- ClassifiedArticle

This ensures consistent data flow between modules.

---

### 5. Output Generation

Classified results are automatically saved:

---

## Project Structure

---

## Installation

### 1. Create Virtual Environment

### 2. Activate Environment

Windows:

### 3. Install Dependencies

---

## Running the Application

From the project root directory:

---

## Sample Output

Example:

---

## Technologies Used

- Python
- DDGS Search
- Pydantic
- JSON
- Logging
- Modular Python Architecture

---

## Future Enhancements

Planned Week 2-4 improvements:

- Supply chain knowledge graph.
- Multi-agent architecture using CrewAI/LangGraph.
- Supplier impact analysis.
- Alternative sourcing recommendations.
- Automated disruption action plans.

---

## Author

Internship Project:
**Autonomous Supply Chain Disruption Monitor**
