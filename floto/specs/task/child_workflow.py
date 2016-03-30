from floto.specs.task import Task


class ChildWorkflow(Task):
    """ChildWorkflow task spec."""

    def __init__(self, *, domain, workflow_type_name, workflow_type_version, workflow_id=None,
                 requires=None, input=None, task_list=None, retry_strategy=None):
        """Defines a child workflow which is scheduled as part of a decider execution logic and
        used in decider specs.
        
        Parameters
        ----------
        workflow_type_name: str
            The name of the workflow type to be scheduled
        workflow_type_version: str
            The version of the workflow type to be scheduled
        workflow_id: Optional[str]
            The id of the workflow. 
            Defaults to <workflow_type_name>:<workflow_type_version>:hash(input/requires)
        requires: Optional[list]
            List of tasks this child workflow execution depends on
        input: Optional[dict]
            Input provided to this child workflow execution
        task_list: Optional[str]
            The name of the task list to be used for decision tasks of the child workflow 
            execution. If not set, the default task list of the workflow type is used.
        retry_strategy: Optional[floto.specs.Strategy]
            The strategy which defines the repeated execution strategy.
        """
        super().__init__(requires=requires)

        self.domain = domain
        self.workflow_type_name = workflow_type_name
        self.workflow_type_version = workflow_type_version
        self.input = input
        self.task_list = task_list
        self.retry_strategy = retry_strategy

        default_id = self._default_id(domain=domain, name=workflow_type_name,
                                      version=workflow_type_version, input=input)
        self.id_ = workflow_id or default_id

    def serializable(self):
        cpy = super().serializable()

        retry_strategy = cpy.get('retry_strategy')
        if retry_strategy:
            cpy['retry_strategy'] = retry_strategy.serializable()

        logger.debug('serialized ActivityTask: {}'.format(cpy))
        return cpy

    @classmethod
    def _deserialized(cls, **kwargs):
        """Construct an instance from a dict of attributes

        Notes
        -----
        Note that the parameter `workflow_id` is assigned to the attribute `id_ `
        """
        cpy = floto.specs.serializer.copy_args_wo_type(kwargs)
        cpy['workflow_id'] = cpy.pop('id_', None)

        if cpy.get('retry_strategy'):
            rs = floto.specs.retry_strategy.Strategy.deserialized(**cpy['retry_strategy'])
            cpy['retry_strategy'] = rs
        return cls(**cpy)
