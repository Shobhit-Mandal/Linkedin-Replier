# LinkedIn Service Request Automation System

A workflow-based system that automates responding to LinkedIn service marketplace requests by extracting requirements and generating structured proposals.

---

## 🚀 Problem

Service providers receive inbound requests on LinkedIn with:

- unstructured requirements  
- long message threads  
- manual effort to read, understand, and respond  

This slows down response time and reduces efficiency in handling multiple leads.

---

## ⚙️ Solution

Designed a system that:

1. Parses incoming LinkedIn service request emails (HTML/JSON)
2. Extracts key questions and requirements
3. Structures the information into usable format
4. Generates a tailored proposal message
5. Automatically submits the proposal back on LinkedIn

---

## 🧠 System Flow

Input → Processing → Action

- **Input:** LinkedIn service request email (HTML/JSON)
- **Processing:**
  - parse and extract Q&A (BeautifulSoup)
  - structure requirements
  - generate proposal message
- **Action:**
  - automate browser interaction (Selenium)
  - submit proposal to LinkedIn thread

---

## 🔧 Tech Stack

- Python (core logic)
- BeautifulSoup (HTML parsing)
- Selenium + undetected_chromedriver (automation)
- n8n (workflow orchestration)

---

## 📌 Key Features

- Converts unstructured requests into structured data
- Automates proposal generation and submission
- Reduces manual effort in handling inbound leads
- Integrates parsing + generation + execution in one flow

---

## ⚠️ Note

Since this relies on LinkedIn UI automation, some parts may require selector updates or environment setup changes, but the core system logic remains intact.

---

## 👤 Author

Shobhit Mandal
Contact: shobhitmandal0209@gmail.com
