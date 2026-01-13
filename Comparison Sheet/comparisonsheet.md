# AI Model Comparison Sheet

## Department Use Cases
- AppDev (Code Generation, Code Quality)
- Data Analysis & SQL (Data)
- Infrastructure Automation (DevOps)
- Ease of Use
- Speed / Latency

## Models Evaluated
- GPT-5  
- Claude 4.5  
- Gemini Flash  
- DeepSeek-R1:7B (Ollama)

## Rating Legend
- **excellent**
- **good**
- **basic / limited support**
- **not supported**

---

## AI Model Comparison Table

| Use Case / Criteria | GPT-5 | Claude 4.5 | Gemini Flash | DeepSeek-R1:7B (Ollama) | Comments |
|---------------------|-------|------------|--------------|--------------------------|----------|
| **AppDev – Code Generation (Code Quality)** | excellent | excellent | good | basic / limited support | **Prompt:** “Backend API Design: Create a RESTful API in Node.js (Express) for a Task Management System with CRUD for tasks, JWT authentication, role-based access (admin, user), PostgreSQL integration. Provide folder structure and sample code.”<br><br>**GPT-5:** Excellent file structure, clean modular API, routes and controllers well separated, correct HTTP methods and status codes. Minor gap: no centralized error-handling layer.<br><br>**Claude 4.5:** Very good folder structure with excellent modularization. Business logic is sound, error handling is thorough, though responses are slightly verbose.<br><br>**Gemini Flash:** Modular API with readable endpoints. ID generation is simplistic and validation is limited.<br><br>**DeepSeek-R1:7B:** Produced partially non-functional code, hallucinated libraries, and invalid imports. |
| **Data – SQL Generation** | excellent | excellent | good | good | **Prompt:** “Optimize and explain the following query: `SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE country = 'India')`.”<br><br>**GPT-5 & Claude 4.5:** Provided optimized queries, indexing recommendations, database-constraint considerations, and performance comparisons.<br><br>**Gemini Flash:** Provided optimized query and indexing strategies, but with less depth of explanation.<br><br>**DeepSeek-R1:7B:** Provided a correct optimized solution, with minimal explanation. |
| **Data – Analysis & Business Insights** | excellent | excellent | good | good | **Prompt:** “Given a table `orders(id, customer_id, amount, created_at)`, write a SQL query to calculate the total revenue generated in the last 30 days.”<br><br>**GPT-5:** Accurate results with structured insights, optimization suggestions, and actionable business interpretations.<br><br>**Claude 4.5:** Correct solution with optimizations and future-oriented considerations. Also provided variants for different SQL environments.<br><br>**Gemini Flash:** Provided the correct solution along with basic optimization strategies.<br><br>**DeepSeek-R1:7B:** Provided a correct solution with minimal contextual explanation. |
| **Infra Automation – DevOps (Bash / Scripts)** | excellent | excellent | good | basic / limited support | **Prompt:** “Write a Bash script that checks if port 8080 is in use. If in use, print the process ID and process name. If free, print a confirmation message.”<br><br>**GPT-5:** Correct, executable, and production-ready script.<br><br>**Claude 4.5:** Robust script with additional validation and helpful messages, though slightly verbose.<br><br>**Gemini Flash:** Simple, working script that meets basic requirements with limited error handling.<br><br>**DeepSeek-R1:7B:** Simple working script that meets only the basic requirement. |
| **Ease of Use** | excellent | excellent | good | basic / limited support | **Observation:** GPT-5 requires minimal prompt refinement and produces consistent outputs. Claude 4.5 provides clear, human-like explanations but is slightly verbose. Gemini Flash is simple and fast. DeepSeek-R1:7B requires local setup and prompt tuning, with inconsistent outputs. |
| **Speed / Latency** | excellent | good | good | good | **Observation:** GPT-5 is fast and stable. Claude 4.5 is slightly slower but delivers high-quality responses. Gemini Flash is very fast and well-suited for low-latency tasks. DeepSeek-R1:7B performance depends on local hardware—fast for small prompts, slower for complex reasoning. |

---

## Summary / Recommendations

- **Best Overall (Balanced Across Use Cases):** GPT-5  
- **Best for Explanations and Detailed Reports:** Claude 4.5  
- **Best for Speed and Lightweight Tasks:** Gemini Flash  
- **Local Model (Experimental / Cost-Sensitive Use):** DeepSeek-R1:7B (Ollama)
