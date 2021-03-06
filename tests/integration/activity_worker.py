import multiprocessing as mp
import time

import floto


@floto.activity(domain='floto_test', name='activity1', version='v5')
def activity1(context):
    print('activity1_v5 started' + 20 * '.')
    result = {'workflow': context['workflow'],
              'status': 'finished'}
    time.sleep(1)
    print('activity1_v5 finished' + 20 * '.')
    return result

@floto.activity(domain='floto_test', name='activity2', version='v4')
def activity2():
    print('activity2 started' + 20 * '.')
    result = {'status': 'finished'}
    time.sleep(1)
    print('activity2 finished' + 20 * '.')
    return result


@floto.activity(domain='floto_test', name='activity3', version='v2')
def activity3(context):
    print('activity3 started' + 20 * '.')
    activity1_result = [v for k, v in context.items() if 'activity1' in k][0]
    result = {'status': 'finished',
              'activity1': activity1_result}
    print('activity3 finished' + 20 * '.')
    return result


FAILURE_COUNT_1 = 0


@floto.activity(domain='floto_test', name='activity_fails_3', version='v2')
def activity_fails_3(context):
    print('activity_fails_3 started' + 20 * '.')
    global FAILURE_COUNT_1
    FAILURE_COUNT_1 += 1
    result = {'workflow_input': context['workflow'],
              'status': 'finished'}
    if FAILURE_COUNT_1 <= 3:
        print('activity_fails_3 finished with error' + 20 * '.')
        raise Exception('Something went wrong')
    else:
        FAILURE_COUNT_1 = 0
    print('activity_fails_3 finished' + 20 * '.')
    return result


FAILURE_COUNT_2 = 0


@floto.activity(domain='floto_test', name='activity_fails_2', version='v2')
def activity_fails_2():
    print('activity_fails_2 started' + 20 * '.')
    global FAILURE_COUNT_2
    FAILURE_COUNT_2 += 1
    if FAILURE_COUNT_2 >= 2: FAILURE_COUNT_2 = 0
    print('activity_fails_2 finished with error' + 20 * '.')
    raise Exception('Something went wrong')


@floto.activity(domain='floto_test', name='activity4', version='v2')
def activity_4(context):
    print('activity_4 started' + 20 * '.')
    print('activity_4 finished' + 20 * '.')
    return context


@floto.activity(domain='floto_test', name='activity5', version='v2')
def activity_5():
    print('activity_5 started' + 20 * '.')
    print('Sleeping for 30s.')
    time.sleep(30)
    print('activity_5 finished' + 20 * '.')
    return {'status':'finished'}

@floto.generator(domain='floto_test', name='generator1', version='v1')
def generator1():
    print('generator_1 started' + 20 * '.')
    rs = floto.specs.retry_strategy.InstantRetry(retries=2)
    domain = 'floto_test'
    task_1 = floto.specs.task.ActivityTask(domain=domain, name='activity4', version='v2', 
            retry_strategy=rs, input={'file':'a.in'})
    task_2 = floto.specs.task.ActivityTask(domain=domain, name='activity4', version='v2', 
            retry_strategy=rs, input={'file':'b.in'})
    print('generator_1 finished' + 20 * '.')
    return [task_1, task_2]

@floto.activity(domain='floto_test', name='activity6', version='v1')
def activity_6(context):
    print('activity_6 started' + 20 * '.')
    time.sleep(7)
    processed_files = [v['activity_task']['file'] for k,v in context.items() if 'activity4' in k]
    print('activity_6 finished' + 20 * '.')
    return processed_files



class ActivityWorkerProcess(object):
    def __init__(self, domain, task_list):
        self._process = None
        self.worker = floto.ActivityWorker(domain=domain, task_list=task_list, 
            task_heartbeat_in_seconds=5)

    def start(self):
        self._process = mp.Process(target=self.worker.run)
        self._process.start()

    def terminate(self):
        self._process.terminate()


if __name__ == '__main__':
    worker = ActivityWorkerProcess(domain='floto_test', task_list='floto_activities')
    worker.start()
