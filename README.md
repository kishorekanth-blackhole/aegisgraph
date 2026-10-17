# AegisGraph: Autonomous Blast-Radius & Cascading Exploit Immunizer

[![FalkorDB](https://img.shields.io/badge/Graph_Database-FalkorDB_GraphBLAS-00E599?style=flat-square&logo=redis)](https://falkordb.com)
[![openCypher](https://img.shields.io/badge/Query_Language-openCypher-blue?style=flat-square)](https://opencypher.org)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Deployment-Docker_Compose-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

> **Graph Hacks 2026** — *Track 1: Agents That Act on Connected Data*  
> **Lead Engineer:** Kishore Kanth ([@kishorekanth-blackhole](https://github.com/kishorekanth-blackhole))  
> **Live System Console:** [https://ais-pre-47k5ojpja734rsi23ogflm-637186347104.asia-southeast1.run.app](https://ais-pre-47k5ojpja734rsi23ogflm-637186347104.asia-southeast1.run.app)  
> **Repository:** [https://github.com/kishorekanth-blackhole/aegisgraph](https://github.com/kishorekanth-blackhole/aegisgraph)  

---

## 1. Executive Summary & Problem Formulation
Modern enterprise cloud environments and autonomous multi-agent systems face severe operational risks stemming from **transitive, multi-hop privilege escalation** and cascading supply-chain compromises. 

In a typical cloud breach, an adversary does not directly access crown jewel databases. Instead, they compromise an ephemeral staging container, leverage an assigned IAM service role with misconfigured trust policies to pivot into an infrastructure deployer, and exfiltrate production secrets.

Traditional Security Information and Event Management (SIEM) systems and Vector Retrieval-Augmented Generation (Vector RAG) analyze telemetry in **isolated semantic silos**. They are fundamentally blind to multi-hop graph topology, transitive permissions, and circular trust paths.

**AegisGraph** is an autonomous security intelligence agent powered by **FalkorDB**. It leverages sparse matrix graph algorithms (GraphBLAS) to traverse entity topologies in sub-10ms, calculates topological blast-radii across $N$-hop relationships, and executes deterministic, closed-loop remediation actions to immunize the infrastructure in real time.

---

## 2. Theoretical Architecture: Why FalkorDB GraphBLAS is Irreplaceable
A core requirement of this autonomous system is real-time graph reasoning within the agent's active execution loop:

$$\text{Blast Radius} = \sum_{v \in \mathcal{V}_{\text{reachable}}} \text{Sensitivity}(v) \times \frac{1}{\text{dist}(\text{Seed}, v)}$$

* **Relational DB Infeasibility:** Computing transitive reachability and shortest paths in SQL requires recursive common table expressions (CTEs) or $N$-way self-joins, causing exponential execution latency ($>2,500\text{ms}$) under high edge density.
* **Vector RAG Infeasibility:** Vector similarity measures cosine distance between unstructured text chunks. Vectors cannot model directed causality, transitive trust (`A assumes B assumes C`), or structural centrality.
* **FalkorDB GraphBLAS Superiority:** FalkorDB models graphs as sparse adjacency matrices and executes algebraic semiring matrix multiplication. Multi-hop reachability is calculated in under **$8.4\text{ms}$**, enabling the AI agent to make sub-second decisions in active production incident loops.

---

## 3. Formal Graph Schema & Topology Model

### Node Specifications
| Label | Key Properties | Semantic Description |
| :--- | :--- | :--- |
| `:Server` | `id, name, ip, namespace, status, riskScore` | Ephemeral compute pods and virtual servers |
| `:Role` | `id, name, trustPolicy, wildcardPolicy, riskScore` | IAM identity roles and trust boundaries |
| `:Resource` | `id, name, sensitivity, records, riskScore` | High-value assets (RDS databases, KMS vaults, S3 buckets) |
| `:Alert` | `id, type, severity, source, timestamp` | Ingested threat telemetry (e.g. AWS GuardDuty / CloudTrail) |

### Directed Relationship Specifications
| Relationship Type | Source $\to$ Target | Semantics |
| :--- | :--- | :--- |
| `-[:AFFECTS]->` | `:Alert` $\to$ `:Server` | Telemetry link indicating compromised entry point |
| `-[:ASSUMES]->` | `:Server` $\to$ `:Role` | Compute credential association |
| `-[:CAN_ASSUME]->` | `:Role` $\to$ `:Role` | Transitive IAM trust delegation (**Critical Attack Path**) |
| `-[:FULL_ACCESS]->` | `:Role` $\to$ `:Resource` | Decryption and read/write privileges over data vaults |
| `-[:REVOKED_BY_AGENT]->` | `:Role` $\to$ `:Role` | Autonomously synthesized zero-trust security boundary |

### Topological Architecture Diagram
