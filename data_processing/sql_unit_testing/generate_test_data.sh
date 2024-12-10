#!/bin/bash

# Base directory for tests
BASE_DIR="./queries/1"
rm -r $BASE_DIR
QUERY_FILE="$BASE_DIR/query.sql"
CONFIG_FILE="$BASE_DIR/config.yaml"
TEST_CASES_DIR="$BASE_DIR/test_cases"

# Create directories
mkdir -p $TEST_CASES_DIR/suite_1
mkdir -p $TEST_CASES_DIR/suite_2
mkdir -p $TEST_CASES_DIR/suite_3

# Write query.sql
cat <<EOF > $QUERY_FILE
SELECT
    u.id AS user_id,
    u.name,
    COUNT(o.id) AS total_orders,
    COALESCE(SUM(o.order_total), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
ORDER BY total_spent DESC, u.name ASC;
EOF

# Write test_config.yaml
cat <<EOF > $CONFIG_FILE
query:
  file: query.sql

test_suites:
  suite_1:
    description: "Default datasets for users and orders"
    tests:
      - description: "Test full query with default datasets"
        inputs:
          - table: users
            file: test_cases/suite_1/input_users.csv
          - table: orders
            file: test_cases/suite_1/input_orders.csv
        expected_results: test_cases/suite_1/expected_results_query.csv

  suite_2:
    description: "No orders present"
    tests:
      - description: "Test full query with no orders"
        inputs:
          - table: users
            file: test_cases/suite_2/input_users.csv
          - table: orders
            file: test_cases/suite_2/input_orders.csv
        expected_results: test_cases/suite_2/expected_results_query.csv

  suite_3:
    description: "High-value orders only"
    tests:
      - description: "Test full query with high-value orders"
        inputs:
          - table: users
            file: test_cases/suite_3/input_users.csv
          - table: orders
            file: test_cases/suite_3/input_orders.csv
        expected_results: test_cases/suite_3/expected_results_query.csv
EOF

# Generate test case data
generate_csv() {
  local file=$1
  shift
  {
    for row in "$@"; do
      echo "$row"
    done
  } > "$file"
}

# Suite 1
generate_csv "$TEST_CASES_DIR/suite_1/input_users.csv" "id,name" "1,Alice" "2,Bob" "3,Charlie" "4,Diana"
generate_csv "$TEST_CASES_DIR/suite_1/input_orders.csv" "id,user_id,order_total,created_at" \
  "1,1,120.50,2023-01-05" "2,1,80.00,2022-12-15" "3,2,50.00,2023-02-10" "4,3,200.00,2023-01-20" "5,3,300.00,2023-02-01"
generate_csv "$TEST_CASES_DIR/suite_1/expected_results_query.csv" "user_id,name,total_orders,total_spent" \
  "3,Charlie,2,500.00" "1,Alice,1,120.50" "2,Bob,1,50.00" "4,Diana,0,0.00"

# Suite 2 (No orders)
generate_csv "$TEST_CASES_DIR/suite_2/input_users.csv" "id,name" "1,Alice" "2,Bob" "3,Charlie" "4,Diana"
generate_csv "$TEST_CASES_DIR/suite_2/input_orders.csv" "id,user_id,order_total,created_at"
generate_csv "$TEST_CASES_DIR/suite_2/expected_results_query.csv" "user_id,name,total_orders,total_spent" \
  "1,Alice,0,0.00" "2,Bob,0,0.00" "3,Charlie,0,0.00" "4,Diana,0,0.00"

# Suite 3 (High-value orders)
generate_csv "$TEST_CASES_DIR/suite_3/input_users.csv" "id,name" "1,Alice" "2,Bob" "3,Charlie" "4,Diana"
generate_csv "$TEST_CASES_DIR/suite_3/input_orders.csv" "id,user_id,order_total,created_at" \
  "1,3,300.00,2023-02-01" "2,3,400.00,2023-01-20"
generate_csv "$TEST_CASES_DIR/suite_3/expected_results_query.csv" "user_id,name,total_orders,total_spent" \
  "3,Charlie,2,700.00" "1,Alice,0,0.00" "2,Bob,0,0.00" "4,Diana,0,0.00"

echo "Test data generation complete."
