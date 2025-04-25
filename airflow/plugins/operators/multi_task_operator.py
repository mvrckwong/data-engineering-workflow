from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class MultiTaskOperator(BaseOperator):
    """
    Example operator that performs multiple tasks.
    """
    @apply_defaults
    def __init__(
        self,
        task1_param: str,
        task2_param: int,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.task1_param = task1_param
        self.task2_param = task2_param

    def execute(self, context):
        self.log.info("Starting multi-task operator...")

        # Task 1: Process a string parameter
        self._perform_task1(context)

        # Task 2: Process an integer parameter
        self._perform_task2(context)

        self.log.info("Multi-task operator finished.")
        # Optionally return a value
        return f"Processed: {self.task1_param}, {self.task2_param}"

    def _perform_task1(self, context):
        """Performs the first task."""
        self.log.info(f"Executing Task 1 with param: {self.task1_param}")
        # Add your task 1 logic here
        processed_string = self.task1_param.upper()
        self.log.info(f"Task 1 result: {processed_string}")
        # Example of pushing to XComs if needed
        context['ti'].xcom_push(key='task1_result', value=processed_string)


    def _perform_task2(self, context):
        """Performs the second task."""
        self.log.info(f"Executing Task 2 with param: {self.task2_param}")
        # Add your task 2 logic here
        result = self.task2_param * 10
        self.log.info(f"Task 2 result: {result}")
        # Example of pushing to XComs if needed
        context['ti'].xcom_push(key='task2_result', value=result)
