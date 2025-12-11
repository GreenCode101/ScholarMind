# 📄 Semantic Query Extraction Benchmark

At the start, **ScholarMind** relied on **keyword-based extraction**. Users typed questions, and the system tried to match exact words in documents. However, scientific queries are rarely exact — different researchers phrase the same concept differently.

**Challenge:**  
> Two queries can mean the same thing but look very different:  

Traditional keyword search struggles to recognize that these queries share the same intent.

---

## Step 1 — Keyword Extraction (V1)

In the first version, ScholarMind used **KeyBERT** to extract keywords from user queries. This approach relied on identifying important words and phrases without understanding context.

* **Method:** KeyBERT (based on MiniLM embeddings) + Maximum Marginal Relevance (MMR)  
* **Features:**  
  - Extracts top-N keywords or phrases (1–3 words)  
  - Uses diversity to avoid redundant keywords  
* **Limitations:**  
  - Misses paraphrased or reworded queries  
  - Cannot capture the semantic meaning behind the question  

> Works for simple matches, but complex scientific queries require deeper understanding.

---

## Step 2 — Semantic Embeddings (V2)

We upgraded to **semantic embedding–based retrieval**, capturing the meaning and intent behind queries using **SPECTER**.

* **Goal:** Extract semantic intent, not just exact words  
* **Method:** Convert queries into dense vector embeddings using **SentenceTransformers (SPECTER model)**  
* **Features:**  
  - Caches query embeddings for repeated use (`functools.lru_cache`)  
  - Returns a 768-dimensional embedding vector per query  
* **Metric:** Cosine similarity between query and document vectors to measure semantic closeness  

> With this upgrade, ScholarMind can match paraphrased queries to relevant scientific documents with high accuracy.

---

## Step 3 — Model Benchmarking

We tested multiple embedding models on the SciFact dataset:

| Model    | Dim | Latency (ms) | Vector Norm | Query–Doc Similarity |
| -------- | --- | ------------ | ----------- | ------------------ |
| SciBERT  | 768 | 129.99       | 17.60       | 0.5054             |
| SPECTER  | 768 | 383.98       | 21.96       | 0.6242             |
| MPNet    | 768 | 588.03       | 1.00        | 0.1254             |
| MiniLM   | 384 | 67.85        | 1.00        | 0.1329             |

---

## Step 4 — Why SPECTER?

* Highest **Query–Doc similarity** in benchmarks → best for semantic retrieval  
* Trained specifically on **scientific papers**  
* Captures context, intent, and paraphrased queries  
* Embedding dimension 768 → efficient and standard  
* Integrates smoothly with **SentenceTransformers**  

--- 
> **Conclusion:** SPECTER provides the best balance between semantic accuracy and scientific relevance, making it the ideal choice for ScholarMind's query extraction pipeline.

---
## References

1. [Extraction Model Selection Documentation](Docs/Extraction_Model_Selection.pdf)
2. [Extraction Engine Notebook](AI/Extraction_engine/ModelBenchmark_Embeddings.ipynb)


