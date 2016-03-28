import pytest
import floto.specs

class TestChildWorkflow():
    def test_init(self):
        cw = floto.specs.ChildWorkflow(workflow_type_name='wft_name',
                workflow_type_version='wft_version',
                workflow_id='wid',
                requires=['a'],
                input={'foo':'bar'},
                retry_strategy='retry_strategy')

        assert cw.workflow_type_name == 'wft_name' 
        assert cw.workflow_type_version == 'wft_version' 
        assert cw.id_ == 'wid'
        assert cw.requires == ['a']
        assert cw.input == {'foo':'bar'}
        assert cw.retry_strategy == 'retry_strategy'

    def test_default_worfklow_id(self, mocker):
        mocker.patch('floto.specs.Task._default_id', return_value='did')
        cw = floto.specs.ChildWorkflow(workflow_type_name='wft_name',
                workflow_type_version='wft_version',
                input={'foo':'bar'})
        floto.specs.Task._default_id.assert_called_once_with('wft_name', 'wft_version', 
                {'foo':'bar'})
        assert cw.id_ == 'did' 


