# Install Atlas model
## Types
### create a relationship type
curl -u admin:admin -d "@create_relationship_type.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/types/typedefs

### create rule type
curl -u admin:admin -d "@rule_type.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/types/typedefs

### create policy type
curl -u admin:admin -d "@create_policy_type.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/types/typedefs

### create a relationship type
curl -u admin:admin -d "@create_policy_rule_relationship_type.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/types/typedefs



## create entities and relationships

### create hive_db
curl -u admin:admin -d "@create_hive_db.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/entity

### create hive table and column manually
curl -u admin:admin -d "@create_hive_table.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/entity

### create Age rule
curl -u admin:admin -d "@create_rule.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/entity

### create relationship between age and hive_column
curl -u admin:admin -d "@create_relationship.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/relationship

### create Age term
curl -u admin:admin -d "@create_term.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/entity

--create semantic assignment relationship between hive_column and GlossaryTerm Age
curl -u admin:admin -d "@create_semantic_assignment_relationship.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/relationship

--create policy KYC
curl -u admin:admin -d "@create_policy.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/entity

--create relationship between a Age rule and a KYC policy
curl -u admin:admin -d "@create_policy_rule_relationship.json" -H "Content-Type: application/json" -X POST http://localhost:21000/api/atlas/v2/relationship
