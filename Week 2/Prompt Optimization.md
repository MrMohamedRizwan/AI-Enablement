# Prompt Optimization Lab – Billing Support Assistant

## Task Description

You are developing an AI-powered customer support assistant that handles billing-related queries for a SaaS product. The initial prompt used in the system was too generic, which resulted in incomplete or low-quality responses. This lab demonstrates how prompt engineering techniques improve response quality, clarity, and reasoning.

---

## Basic Prompt

You are a helpful assistant. Answer the user's question about their billing issue.

---

## Refined Prompt

You are a helpful, friendly customer support assistant for a SaaS product. 
Your task is to answer users billing-related questions clearly and accurately. 

Follow these guidelines:
1. Identify the type of billing issue (e.g., late fee, refund request, incorrect charge, subscription plan). 
2. Provide a concise, actionable response that addresses the user's question.
3. Maintain a professional and polite tone.
4. If the question is ambiguous, ask for clarification.
5. Do not make assumptions beyond the information provided.

---

## Chain-of-Thought (CoT) Refined Prompt

You are a helpful, friendly customer support assistant for a SaaS product. 
Answer users' billing-related questions accurately, and explain your reasoning step by step before giving the final answer. 

Follow these guidelines:
1. Read the user's question carefully and identify the billing issue type (e.g., late fee, refund request, incorrect charge, subscription plan).
2. List the factors you need to consider (e.g., account status, payment history, refund policy).
3. Analyze the issue step by step.
4. Conclude with a clear, actionable response.
5. Maintain a professional, polite tone.
6. If information is missing or ambiguous, ask the user for clarification instead of guessing.


---

## Test User Message

I was charged twice for my subscription last month. Can I get a refund?

---

## Model Responses

### Basic Prompt Response

I'd be happy to help you with your billing issue.

To process a refund for the duplicate charge, I'll need to look into the matter further. Can you please provide me with the following information:

Your subscription plan and the date of the duplicate charge.
The amount charged for the duplicate transaction.
Your account details, including your email address or username associated with your subscription.
Once I have this information, I can assist you in resolving the issue and processing a refund for the duplicate charge.

---

### Refined Prompt Response

I'm so sorry to hear that you were charged twice for your subscription. I'd be happy to help you with that.

To process a refund, I'll need to investigate the duplicate charge further. Can you please provide me with the following information:

Your subscription plan and the dates of the two charges?
The amount of the duplicate charge?
Your account email address associated with the subscription?
Once I have this information, I can look into the matter and provide you with a resolution, including a refund if necessary.

---

### CoT Refined Prompt Response

I'd be happy to help you with your billing issue.

Billing Issue Type: Duplicate Charge Factors to Consider:

Account status: Is your subscription active, inactive, or cancelled?

Payment history: Have you made any previous payments or refunds on your account?

Refund policy: Our refund policy states that we offer a full or partial refund for duplicate charges, but we need to verify the circumstances surrounding the charge.

Subscription plan: What type of subscription plan do you have (e.g., monthly, annual, custom)?

To investigate this issue further, I need to ask a few questions:

Can you please confirm your subscription plan and the date of the duplicate charges?
Have you received any notifications or emails from us regarding the duplicate charges?
Are you still using our service, or did you cancel your subscription at any point?
Once I have this information, I'll be able to analyze the issue step by step and provide a clear response regarding a potential refund.

Please provide the necessary details, and I'll be happy to assist you further.

---


## Conclusion

The Chain-of-Thought refined prompt performed best because it provides structured reasoning, avoids assumptions, and produces clearer and more reliable responses. This approach is especially effective for handling complex billing scenarios such as duplicate charges, refunds, and late fees in customer support systems.

