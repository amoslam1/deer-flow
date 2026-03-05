## ADDED Requirements

### Requirement: Architecture module inventory
The system SHALL scan and inventory architecture modules from backend, frontend, skills, and runtime entrypoints, and produce one canonical record per module.

#### Scenario: Build architecture inventory
- **WHEN** the architecture scan is executed for this change
- **THEN** the output includes module records for scanned architecture domains with unique canonical IDs

### Requirement: Deterministic 16-character hash generation
Each module record MUST include a deterministic 16-character lowercase hexadecimal hash generated from `sha256(canonical_id)` truncated to 16 characters.

#### Scenario: Repeatable hash generation
- **WHEN** the same canonical ID is processed multiple times without renaming
- **THEN** the generated hash remains identical across runs

### Requirement: Parent-to-child dependency annotation
Each architecture module record SHALL declare direct dependencies using parent-to-child direction and SHALL include both name-based and hash-based references.

#### Scenario: Dependency link emission
- **WHEN** a module depends on child modules
- **THEN** the output contains parent->child links in both `moduleA->moduleB` and `hashA->hashB` forms

### Requirement: Hash lookup context bundle
The inventory MUST support lookup by hash and return module context including canonical ID, domain, parents, children, and chain snippets.

#### Scenario: Resolve module by hash
- **WHEN** a valid module hash is provided
- **THEN** the system returns the full module context and related dependency chain entries
