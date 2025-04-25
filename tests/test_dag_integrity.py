# tests/test_dag_integrity.py
import pytest
from airflow.models import DagBag

# Path to your DAGs folder relative to the project root where pytest is run
# Adjust if your test execution context is different
DAGS_FOLDER = "airflow/dags"

@pytest.fixture(scope="session")
def dag_bag():
    """Fixture to load the DagBag instance."""
    # Include plugins=False if your DAGs don't rely on plugins for basic loading,
    # or ensure plugins are available in the test environment.
    try:
        # Attempt loading with plugins first
        return DagBag(dag_folder=DAGS_FOLDER, include_examples=False, include_plugins=True)
    except Exception as e:
        print(f"Warning: Failed to load DagBag with plugins ({e}). Trying without plugins.")
        # Fallback to loading without plugins if there's an issue
        return DagBag(dag_folder=DAGS_FOLDER, include_examples=False, include_plugins=False)

def test_no_import_errors(dag_bag):
    """Check if any DAGs have import errors."""
    assert not dag_bag.import_errors, f"DAG import errors found: {dag_bag.import_errors}"

def test_dags_load_correctly(dag_bag):
    """Check if specific DAGs are loaded and are valid DAG objects."""
    # Get actual DAG IDs found by DagBag, excluding SubDAGs
    loaded_dag_ids = [dag.dag_id for dag in dag_bag.dags.values() if not dag.is_subdag]
    print(f"DAGs found by DagBag: {loaded_dag_ids}")

    # Replace with your *expected* main DAG IDs
    expected_dag_ids = ["dag_dbt_test_layers", "dag_dbt_test_pipeline", "test"] # Add more as needed

    # Check that all expected DAGs are loaded
    missing_dags = set(expected_dag_ids) - set(loaded_dag_ids)
    assert not missing_dags, f"Expected DAGs not found: {missing_dags}"

    # Check that loaded DAGs are indeed DAG objects
    for dag_id in expected_dag_ids:
        if dag_id in loaded_dag_ids: # Check if it was actually loaded
            dag = dag_bag.get_dag(dag_id)
            assert dag is not None, f"DAG '{dag_id}' could not be retrieved from DagBag (even though listed)."
            assert dag.dag_id == dag_id, f"DAG ID mismatch for '{dag_id}'."
            assert not dag.is_subdag, f"DAG '{dag_id}' should not be a SubDAG."

# @pytest.mark.skip(reason="Task counts need to be updated for actual DAGs")
def test_dag_task_counts(dag_bag):
    """Check if specific DAGs have the expected number of tasks."""
    # IMPORTANT: Update these counts based on your actual DAGs
    expected_task_counts = {
        "dag_dbt_test_layers": 0, # FIXME: Update expected count
        "dag_dbt_test_pipeline": 0, # FIXME: Update expected count
        "test": 0, # FIXME: Update expected count
        # Add other DAGs and their expected counts
    }

    for dag_id, expected_count in expected_task_counts.items():
        dag = dag_bag.get_dag(dag_id)
        if dag:
             # Skip check if expected_count is 0, as it likely hasn't been updated
             if expected_count > 0:
                 assert len(dag.tasks) == expected_count, \
                     f"DAG '{dag_id}' has {len(dag.tasks)} tasks, expected {expected_count}."
             else:
                 print(f"Skipping task count check for '{dag_id}' as expected count is 0 (needs update). Actual tasks: {len(dag.tasks)}")
        else:
             # Fail if the DAG is in expected_task_counts but wasn't loaded
             pytest.fail(f"DAG '{dag_id}' not found, cannot check task count.")

# @pytest.mark.skip(reason="Task dependencies need to be updated for actual DAGs")
def test_dag_task_dependencies(dag_bag):
    """Check specific task dependencies in a DAG."""
    # IMPORTANT: Update DAG ID, task IDs, and expected dependencies
    dag_id_to_test = "dag_dbt_test_pipeline" # FIXME: Choose a DAG with known dependencies
    dag = dag_bag.get_dag(dag_id_to_test)

    if dag:
        # Example: Check if 'downstream_task' is downstream of 'upstream_task'
        upstream_task_id = "your_upstream_task_id" # FIXME: Update with actual task ID
        downstream_task_id = "your_downstream_task_id" # FIXME: Update with actual task ID

        upstream_task = dag.get_task(upstream_task_id)
        downstream_task = dag.get_task(downstream_task_id)

        # Check if tasks exist before checking dependency
        if upstream_task and downstream_task:
            assert downstream_task.task_id in upstream_task.downstream_task_ids, \
                f"Task '{downstream_task_id}' should be downstream of '{upstream_task_id}' in DAG '{dag_id_to_test}'."
            assert upstream_task.task_id in downstream_task.upstream_task_ids, \
                f"Task '{upstream_task_id}' should be upstream of '{downstream_task_id}' in DAG '{dag_id_to_test}'."
        else:
             pytest.fail(f"One or both tasks ('{upstream_task_id}', '{downstream_task_id}') not found in DAG '{dag_id_to_test}'. Cannot check dependency.")
    else:
        # Only fail if the dag_id_to_test was actually expected to load
        if dag_id_to_test in [d.dag_id for d in dag_bag.dags.values()]:
             pytest.fail(f"DAG '{dag_id_to_test}' could not be retrieved, cannot check dependencies.")
        else:
            print(f"Skipping dependency check for DAG '{dag_id_to_test}' as it was not found.")


# Add more tests for:
# - Default arguments (e.g., assert dag.default_args['owner'] == 'expected_owner')
# - Presence of specific tags (e.g., assert 'expected_tag' in dag.tags)
# - Correct schedule_interval (e.g., assert dag.schedule_interval == '@daily')
# - Unit tests for functions in airflow/dags/logic/
# - Unit tests for configuration loading/validation logic
# - Unit tests for custom hooks/operators (might require mocking)
