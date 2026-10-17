# AegisGraph: Autonomous Blast-Radius & Cascading Exploit Immunizer

> **Graph Hacks 2026** — Track 1: Agents That Act on Connected Data  
> **Lead Engineer:** Kishore Kanth (@kishorekanth-blackhole)  
> **Live Working Demo:** https://ais-pre-47k5ojpja734rsi23ogflm-637186347104.asia-southeast1.run.app  

---

## 1. Project Overview
AegisGraph is an autonomous security intelligence agent powered by **FalkorDB GraphBLAS**. Unlike traditional tools that look at security alerts in isolation, AegisGraph navigates the multi-hop relational topology of cloud infrastructure to detect toxic privilege escalation chains and execute real-time closed-loop mitigation.

---

## 2. Why FalkorDB is Central (The Cardinal Rule)
This system cannot function without FalkorDB because:
1. **Multi-Hop Traversal:** Relational SQL requires slow, recursive joins. FalkorDB executes sparse matrix shortest-path traversals in under 10ms.
2. **Vector Search Blind Spots:** Vector RAG cannot model transitive trust (`Pod -> Role A -> Role B -> Vault`).
3. **Closed-Loop Action:** The agent actively mutates the graph, severing compromised relationships in real time.

---

## 3. Core openCypher Queries

### Multi-Hop Shortest Path Reachability
```cypher
MATCH (seed:Server {id: 'pod-staging-101'})
MATCH (critical:Resource {sensitivity: 'CRITICAL'})
MATCH path = shortestPath((seed)-[*1..4]->(critical))
RETURN [n in nodes(path) | coalesce(n.name, n.id)] as attackChain,
       length(path) as totalHops,
       critical.name as targetCrownJewel;
MATCH (s:Role {name: 'StagingServiceRole'})-[r:CAN_ASSUME]->(t:Role {name: 'CrossAccountDeployer'})
DELETE r
CREATE (s)-[:REVOKED_BY_AGENT {timestamp: datetime(), proofHash: '0x8a7f4c91b2'}]->(t)
WITH s, t
MATCH (p:Server {id: 'pod-staging-101'})
SET p.status = 'QUARANTINED_ISOLATED', p.riskScore = 0
RETURN s.name, t.name, p.status;
# 1. Start FalkorDB
docker run -p 6379:6379 -it --rm falkordb/falkordb

# 2. Test Live Web App
Open: https://ais-pre-47k5ojpja734rsi23ogflm-637186347104.asia-southeast1.run.app
