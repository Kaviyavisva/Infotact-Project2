# Autonomous Supply Chain Disruption Monitor

## Project Overview

The Autonomous Supply Chain Disruption Monitor is a Generative AI-based system designed to identify and classify global supply chain disruptions from real-time logistics news.

The system continuously collects supply chain-related news articles, processes the information, identifies disruption categories, evaluates severity levels, and generates structured disruption reports.

This project is developed as part of the **Infotact Internship - Project 3: Logistics & Supply Chain - Autonomous Disruption Monitoring Agent**.

---

# Week 1: Web Search Integration and Disruption Classification

## Objective

The objective of Week 1 is to build the foundation of the autonomous disruption monitoring system by integrating web search capabilities and implementing disruption classification.

The system performs:

- Real-time logistics news retrieval.
- News data processing and validation.
- Supply chain disruption classification.
- Severity assessment.
- Structured report generation.

---

# Week 1 Workflow
          START
            |
            ↓
    News Fetcher Module
      (DDGS Search)
            |
            ↓
   Data Processor Module
  (Clean & Validate Data)
            |
            ↓
   News Classification
(Category + Severity Detection)
            |
            ↓
    Pydantic Models
(Structured Data Validation)
            |
            ↓
    Output Writer Module
            |
            ↓
            
---

# Features Implemented

## 1. News Fetching Module

File:

Responsibilities:

- Integrated DDGS search engine.
- Fetches recent supply chain and logistics-related news.
- Extracts:

  - Article title
  - URL
  - News summary

---

## 2. Data Processing Module

File:

Responsibilities:

- Cleans retrieved news data.
- Removes incomplete records.
- Converts raw data into structured objects.

---

## 3. Disruption Classification Module

File:

The system identifies disruption categories:

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

Example:

---

## 4. Pydantic Data Validation

File:

Implemented structured models:

### NewsArticle

Stores:

- Title
- URL
- Snippet


### ClassifiedArticle

Stores:

- Title
- Category
- Severity
- Reason

This ensures consistent data exchange between modules.

---

## 5. Configuration Management

File:

Contains:

- Search query configuration.
- Maximum search results.
- Classification categories.
- Severity levels.
- Output file path.

---

## 6. Logging System

File:

Implemented application logging for:

- News fetching status.
- Successful execution.
- Error tracking.

---

## 7. Output Generation

File:

Automatically generates:

containing classified supply chain disruption information.

---

# Project Structure

---

# Installation

## 1. Create Virtual Environment

```bash
python -m venv venv