**Neo4j installation and migration**

1. Design AWS target topology for Neo4j primary nodes, read replicas, and clustering - 1.5 SP  
2. Provision and size AWS infrastructure (EC2, EBS, networking, security groups) for Neo4j across environments - 2 SP  
3. Install and configure Neo4j Enterprise cluster with HA, causal clustering, and security settings - 3 SP  
4. Migrate graph data, schema, indexes, constraints, users, and privileges from on-prem - 4 SP  
5. Implement data sync approach and develop cutover + rollback procedures - 2 SP  
6. Execute performance validation, failover testing, and DR readiness checks - 2 SP  

One-time effort ≈ 14.5 SP  

Dependencies: Platform foundation complete (networking, IAM, storage, monitoring, AVM accounts, SIAM/Netgroup/AD groups, Splunk index).  

**Dependencies and security components**

1. Inventory Protegrity jars, UDFs, and current tokenization usage patterns - 1 SP  
2. Migrate Protegrity jars and configure UDF patterns on AWS Neo4j - 2 SP  
3. Validate tokenization and detokenization end-to-end behavior in AWS - 2 SP  
4. Confirm secrets handling (Secrets Manager / Parameter Store) and encryption controls - 1.5 SP  
5. Perform security and compliance validation of protected data flows - 1 SP  

One-time effort ≈ 7.5 SP  

Dependencies: Neo4j cluster installed and data migrated; Protegrity tooling already provisioned under Platform foundation.  

**Linkurious Installation and MySQL backend migration**

1. Design and provision Linkurious infrastructure on AWS - 1.5 SP  
2. Migrate Linkurious platform binaries, configuration, and settings - 2 SP  
3. Migrate Linkurious backend MySQL database to AWS (RDS or equivalent) - 3 SP  
4. Reconnect Linkurious to Neo4j, configure user access and authentication - 1 SP  
5. Migrate and validate saved visualizations, alerts, and user workflows - 2 SP  
6. Execute end-to-end functional and performance testing - 1 SP  

One-time effort ≈ 10.5 SP  

Dependencies: Neo4j cluster fully operational and data migrated; Platform foundation (networking, IAM, monitoring) complete.  

**NeoDash migration**

1. Design and provision NeoDash platform on AWS - 1 SP  
2. Migrate NeoDash platform and configuration - 1 SP  
3. Reconnect NeoDash to Neo4j and configure user access - 1 SP  
4. Migrate saved dashboards - 1 SP  
5. Validate NeoDash dashboards and end-user workflows - 1 SP  

One-time effort ≈ 5 SP  

Dependencies: Neo4j cluster fully operational with data migrated; Platform foundation complete.
