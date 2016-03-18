import floto
import logging
from floto.specs import ActivityTask, DeciderSpec, ChildWorkflow
import floto.decider

logger = logging.getLogger(__name__)

# ---------------------------------- #
# Create Activity Tasks and Decider
# ---------------------------------- #
decider_spec = DeciderSpec(domain='floto_test',
                           task_list='demo_step_decisions_child',
                           activity_task_list='demo_step_activities_philipp',
                           terminate_decider_after_completion=False)

decider = floto.decider.DynamicDecider(decider_spec=decider_spec)

# ---------------------------------- #
# Start the decider
# ---------------------------------- #
decider.run()
