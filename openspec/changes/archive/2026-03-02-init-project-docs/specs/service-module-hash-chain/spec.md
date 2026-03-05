## ADDED Requirements

### Requirement: Service and backend job coverage
The system SHALL inventory runtime services, backend scheduling services, and common modules used by those services.

#### Scenario: Build service scope
- **WHEN** service scanning runs
- **THEN** the output includes gateway, langgraph, frontend, nginx, optional provisioner, and backend scheduler/common module records

### Requirement: Service module hash assignment
Each service/common-module record MUST include a deterministic 16-character lowercase hexadecimal hash derived from `sha256(canonical_id)[:16]`.

#### Scenario: Service hash generation
- **WHEN** a service or common-module canonical ID is scanned
- **THEN** exactly one 16-character hash is generated and stored with that record

### Requirement: Dependency chain output
The system SHALL emit explicit dependency chains using parent-to-child order in the format `Ahash->Bhash->Chash` for multi-hop relationships.

#### Scenario: Multi-hop dependency chain
- **WHEN** a service depends on an intermediate module that depends on another module
- **THEN** the output includes at least one three-node hash chain ordered from parent to child

### Requirement: Reverse index for hash-driven context retrieval
The system MUST produce a reverse index keyed by hash so downstream workflows can input a hash and obtain all connected service/module context.

#### Scenario: Retrieve service context by hash
- **WHEN** a known hash key is queried
- **THEN** the system returns the matched record and its upstream/downstream dependency links

### Requirement: Code-location context and plan evaluation output
The system SHALL support taking a code location or hash as input, auto-summarize relevant context, and output a rationality assessment of the current approach with actionable solution options.

#### Scenario: Evaluate approach from a code location
- **WHEN** a caller provides file path with line range or a resolvable location hash
- **THEN** the system returns context summary, assessment dimensions, and at least one recommended implementation option
