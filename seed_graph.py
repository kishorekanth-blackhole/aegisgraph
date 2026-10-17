import os
from falkordb import FalkorDB

# Connect to local or cloud FalkorDB
client = FalkorDB(host=os.getenv('FALKORDB_HOST', 'localhost'), port=int(os.getenv('FALKORDB_PORT', 6379)))
graph = client.select_graph('aegis_iam_topology')

# Clear previous test data
graph.query("MATCH (n) DETACH DELETE n")

# Seed Nodes
print("Seeding AegisGraph nodes...")
graph.query("""
CREATE (:Server {id: 'pod-staging-101', name: 'Staging Auth Pod', ip: '10.0.4.12', riskScore: 85, status: 'RUNNING'}),
       (:Role {id: 'role-staging-svc', name: 'StagingServiceRole', trustPolicy: 'AssumeRole', riskScore: 70}),
       (:Role {id: 'role-cross-deployer', name: 'CrossAccountDeployer', policy: 'iam:PassRole', riskScore: 95}),
       (:Resource {id: 'rds-prod-vault', name: 'Prod Customer RDS Vault', sensitivity: 'CRITICAL', records: 450000, riskScore: 99}),
       (:Resource {id: 's3-staging-logs', name: 'Staging Logs Bucket', sensitivity: 'LOW', riskScore: 15}),
       (:Alert {id: 'alert-guardduty-892', type: 'PrivilegeAnomaly', severity: 'CRITICAL'})
""")

# Seed Directed Relationships
print("Seeding relationships & toxic privilege combinations...")
graph.query("""
MATCH (a:Alert {id: 'alert-guardduty-892'}), (s:Server {id: 'pod-staging-101'})
CREATE (a)-[:FLAGGED]->(s)
""")

graph.query("""
MATCH (s:Server {id: 'pod-staging-101'}), (r:Role {id: 'role-staging-svc'})
CREATE (s)-[:ASSUMES]->(r)
""")

graph.query("""
MATCH (r:Role {id: 'role-staging-svc'}), (s3:Resource {id: 's3-staging-logs'})
CREATE (r)-[:ATTACHED_TO]->(s3)
""")

graph.query("""
MATCH (r1:Role {id: 'role-staging-svc'}), (r2:Role {id: 'role-cross-deployer'})
CREATE (r1)-[:CAN_ASSUME {toxicPrivEsc: true}]->(r2)
""")

graph.query("""
MATCH (r2:Role {id: 'role-cross-deployer'}), (db:Resource {id: 'rds-prod-vault'})
CREATE (r2)-[:FULL_ACCESS]->(db)
""")

print("✅ FalkorDB graph initialized with 6 nodes and 5 directed edges!")