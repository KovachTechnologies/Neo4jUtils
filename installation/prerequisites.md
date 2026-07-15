# Prerequisites for Installing Neo4j and Linkurious on Amazon EC2

*Assumes the latest versions of Neo4j (2026.x) and Linkurious Enterprise (4.3.x) as of July 2026.*

---

## 1. AWS Account & Access Prerequisites

- An active AWS account with permissions to create/manage EC2 instances, VPCs, Security Groups, and (optionally) Elastic IPs.
- An IAM user/role with EC2 launch, security-group, and networking permissions.
- An EC2 key pair for SSH access.
- A VPC with at least one subnet, an internet gateway, and route table configured for outbound/inbound access.

---

## 2. EC2 Instance Sizing

| Component | Minimum | Recommended |
|---|---|---|
| **Neo4j (cloud environments)** | 2 vCPU, 2 GB RAM, 10 GB block storage | 16+ vCPU, memory sized to fit your graph, NVMe SSD / gp3 or io2 EBS |
| **Linkurious Enterprise server** | 5–6 GB RAM, 2–4 CPU cores, 3–5 GB free disk (SSD preferred) | 6 GB+ RAM, 8 CPU cores, additional disk for embedded Elasticsearch (~50% of graph DB size) |

Notes:
- Neo4j performance is generally memory- or I/O-bound for large graphs and compute-bound for graphs that fit entirely in memory.
- Linkurious hardware needs scale with user count and alert volume — the figures above assume a small deployment (~20 users); larger deployments (100+ users) should offload Elasticsearch and the user-data store to dedicated instances.
- Both products require a **64-bit** OS/instance architecture.

**Suggested instance types:** `m6i.xlarge`/`m6i.2xlarge` (or `m7g` Graviton/ARM equivalents, both Neo4j and Node.js support ARM64) for Neo4j; `t3.large`/`m6i.large` or larger for Linkurious, depending on user load.

---

## 3. Operating System

Choose one EC2 AMI that satisfies **both** products:

| OS | Neo4j Support | Linkurious Support |
|---|---|---|
| Amazon Linux 2023 | ✅ (Amazon Corretto 17/OracleJDK 17) | Not officially listed — Amazon Linux is RHEL-family; test against RHEL 8+ baseline |
| Ubuntu Server 20.04 / 22.04+ | ✅ | ✅ (20.04+) |
| Debian 11 / 12 | ✅ | ✅ (10+) |
| RHEL / CentOS Stream 8, 9 | ✅ | ✅ (RHEL 8+ / CentOS 8.5+) |

**Recommendation:** Ubuntu Server 22.04 LTS is the safest common denominator — it's explicitly supported by both vendors and has the most community documentation for EC2 deployments.

Kernel/library baseline for Linkurious (due to its Node.js runtime):
- Linux kernel **>= 4.18**
- **GLIBC >= 2.28**

Check with `uname -r` and `ldd --version` before installing.

---

## 4. Java Requirements (Neo4j)

- Neo4j requires a pre-installed, compatible JVM.
- Current Neo4j versions (2025.x/2026.x) require **Java 21** (Java 17 is no longer supported from Neo4j 2025.01 onward); **Java 25** is supported starting with Neo4j 2025.10.
- Supported distributions: OpenJDK, OracleJDK, ZuluJDK, or Amazon Corretto (on Amazon Linux).
- If you don't pre-install a JDK, the Neo4j package manager install will typically pull in a default OpenJDK build automatically — but pinning a specific JDK version explicitly is recommended for production.

```bash
# Example: Ubuntu/Debian — install OpenJDK 21 before Neo4j
sudo apt-get update
sudo apt-get install -y openjdk-21-jdk
java -version
```

---

## 5. Node.js Requirement (Linkurious)

- Linkurious Enterprise bundles/depends on Node.js internally; ensure the kernel/GLIBC baseline above is met so the bundled runtime functions correctly.
- No separate manual Node.js install is normally required (Linkurious ships its own runtime), but verify against the specific release's install guide in case that changes.

---

## 6. Filesystem & Storage

- Neo4j requires a filesystem that supports proper flush operations (`fsync`, `fdatasync`) for ACID compliance — standard EBS-backed ext4/xfs volumes satisfy this.
- Reserve separate storage volumes/mount points for:
  - Neo4j data directory (`/var/lib/neo4j/data` by default)
  - Neo4j logs
  - Linkurious's application/data directory (needs full read/write permission for its service account)
  - Elasticsearch index storage, if using the embedded or an external Elasticsearch instance for Linkurious search
- SSD-backed storage (gp3/io2 EBS or instance-attached NVMe) is recommended for both products.

---

## 7. Networking / Security Group Rules

Open the following inbound ports on the EC2 security group:

| Port | Protocol | Purpose |
|---|---|---|
| 22 | TCP | SSH administration |
| 7474 | TCP | Neo4j HTTP (Browser/REST API) — unencrypted |
| 7473 | TCP | Neo4j HTTPS (encrypted HTTP) |
| 7687 | TCP | Neo4j Bolt (driver/client connections, used by Linkurious to talk to Neo4j) |
| 443 (or custom, e.g. 3000) | TCP | Linkurious Enterprise web application (HTTPS) |
| 9200 (internal only) | TCP | Elasticsearch, if run as an external/dedicated service — should NOT be exposed publicly |

Best practices:
- Restrict all of the above to known IP ranges/CIDR blocks rather than `0.0.0.0/0`, especially 7474/7687/7473 and the Linkurious web port.
- Keep the Neo4j backup port (default `6362`) and Elasticsearch ports blocked from external access entirely; only allow internal VPC traffic.
- If Neo4j and Linkurious run on **separate** EC2 instances, ensure their security groups allow traffic between each other on the Bolt port (7687).

---

## 8. Package Repositories & Keys (Neo4j)

For Debian/Ubuntu-based AMIs:

```bash
# Add Neo4j GPG key and repository
sudo mkdir -p /etc/apt/keyrings
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/neotechnology.gpg
echo 'deb [signed-by=/etc/apt/keyrings/neotechnology.gpg] https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
```

For RHEL/CentOS-based AMIs, Neo4j provides an equivalent `yum`/`dnf` repo — consult the Neo4j RPM installation docs for the current repo URL and GPG key.

Alternatively, Neo4j Enterprise Edition can be deployed via the **official AWS Marketplace listing**, which uses a Neo4j-maintained CloudFormation template that provisions the VPC, subnets, security groups, and EC2 Auto Scaling group automatically (supports both single-instance and clustered deployments).

---

## 9. Linkurious Package & License

- Download the Linkurious Enterprise package (`.zip`/`.tar.gz`) from your Linkurious account/download portal — a valid license key/file is required.
- Dedicated, non-privileged service account (e.g. `linkurious`) recommended, with full read/write permissions on the Linkurious install directory. No administrative/root rights are required to run it, except if binding to a port below 1024.
- Confirm connectivity from the Linkurious host to the Neo4j Bolt port before installation.

---

## 10. Pre-Installation Checklist

- [ ] EC2 instance(s) sized per Section 2, running a supported 64-bit OS (Section 3)
- [ ] Security groups opened per Section 7, scoped to trusted CIDRs
- [ ] JDK 21 (or supported version) installed prior to Neo4j installation
- [ ] Kernel ≥ 4.18 and GLIBC ≥ 2.28 verified for Linkurious
- [ ] Dedicated storage volumes provisioned for Neo4j data/logs and Linkurious data
- [ ] Neo4j APT/YUM repository (or AWS Marketplace CloudFormation template) selected
- [ ] Linkurious license file obtained and package downloaded
- [ ] Dedicated service accounts created for both Neo4j and Linkurious
- [ ] Decision made on Elasticsearch: embedded (small graphs, <50M nodes+edges) vs. external cluster (large graphs)
- [ ] Decision made on Linkurious user-data store: embedded SQLite (dev/small) vs. external MySQL/MariaDB/MSSQL (production)

---

### Sources
- Neo4j Operations Manual — System Requirements & AWS Deployment docs (neo4j.com/docs/operations-manual)
- Linkurious Administration Manual — Technical Requirements (doc.linkurious.com/admin-manual/latest)
