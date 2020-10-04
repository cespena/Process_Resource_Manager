'''
design and implement extended version of manager

PCB[16]
3-level RL
RCB[4]

RCB[0] and RCB[1] have 1 unit
RCB[2] has 2 units
RCB[3] has 3 units

create()
destroy()
request()
release()
timeout()
scheduler()
init()
init should
    erase all previous contents of the data structures PCB, RCB, RL
    Create a single running process at PCB[0] with priority 0
    Enter the process into the RL at the lowest-priority level 0

'''
class CreateMoreThan16ProcessesError(Exception):
    pass

class DestroyProcessThatsNotAChildOfCurrentProcessError(Exception):
    pass

class RequestANonExistentResourceError(Exception):
    pass

class RequestAResourceProcessAlreadyHolding(Exception):
    pass

class ReleaseAResourceProcessIsNotHolding(Exception):
    pass

class Process0RequestingAResourceError(Exception):
    pass

class DestroyProcess0Error(Exception):
    pass

class SizeOfUnitsIsZeroError(Exception):
    pass

class IncorrectResourceSizePairError(Exception):
    pass

class RequestedSizeTooBigError(Exception):
    pass

class FixedListClass:
    def __init__(self, s, value):
        self.fixed_size = s
        self.fixed_list = [None] * self.fixed_size
        self.count = 0
        if value == 1:
            self.set_resources()
        if value == 2:
            self.set_rl()

    def __getitem__(self, i):
        return self.fixed_list[i]

    def __setitem__(self, i, value):
        self.fixed_list[i] = value

    def add_process(self, item):
        for i in range(len(self.fixed_list)):
            if self.fixed_list[i] == None:
                self.fixed_list[i] = item
                self.count += 1
                return i
        return None

    def set_resources(self):
        for i in range(self.fixed_size):
            if i == 0 or i == 1:
                self.fixed_list[i] = ResourceClass(1)
            elif i == 2:
                self.fixed_list[i] = ResourceClass(2)
            else:
                self.fixed_list[i] = ResourceClass(3)
        self.count = 4

    def set_rl(self):
        for i in range(self.fixed_size):
            self.fixed_list[i] = []
        self.count = 3

class ProcessClass:
    def __init__(self, parent, prior):
        self.priority = prior
        self.current_state = 1
        self.parent = parent
        self.children = []
        self.resources = []
        self.resource_counter = [[],[], [], []]

    def set_state(self, new_state):
        self.current_state = new_state

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def add_resource(self, resource):
        self.resources.append(resource)

    def remove_resource(self, resource):
        self.resources.remove(resource)

class ResourceClass:
    def __init__(self, state):
        self.current_state = state
        self.waitlist = []
        self.inventory = state

    def set_state(self, new_state):
        self.current_state = new_state

    def add_to_waitlist(self, pcb_index):
        self.waitlist.append(pcb_index)

    def remove_from_waitlist(self, pcb_index):
        self.waitlist.remove(pcb_index)
        

class ManagerClass:
    def __init__(self, db):
        self.debugging = db
        self.pcb = FixedListClass(16, 0)
        self.rcb = FixedListClass(4, 1)
        self.rl = FixedListClass(3, 2)
        self.release_processes = []
        
        #create a single running process at PCB[0] with priority 0
        self.pcb.add_process(ProcessClass(None, 0))
        self.rl[0].append(0)
        if self.debugging == 1:
            print("* initialized")
        else:
            self.scheduler()

    def create(self, prior):
        '''
        allocate new PCB[j]
        state = ready
        insert j into children of i
        parent = i
        children = null
        resources = null
        insert j into RL
        display: "process j created"
        '''
        if self.pcb.count > 15:
            raise CreateMoreThan16ProcessesError
            
        current_process = self.get_current_process()
        new_process = self.pcb.add_process(ProcessClass(current_process, prior))
        self.pcb[current_process].add_child(new_process)
        self.rl[prior].append(new_process)
        if self.debugging == 1:
            print("* process ", new_process, " created")#######
            self.scheduler()
        else:
            self.scheduler()########

    def destroy(self, index):
        '''
        for all k in children of j, destroy(k)
        remove j from the parent's list
        remove j from RL or waiting list
        release all resources of j
        free PCB of j
        '''
        if index == 0:
            raise DestroyProcess0Error
        
        current = self.get_current_process()
        if index not in self.pcb[current].children and index != current:
            raise DestroyProcessThatsNotAChildOfCurrentProcessError
        
        final_count = self.destroy_processes(index)
        if self.debugging == 1:
            print("* ", final_count, " processes destroyed")
            self.scheduler()
        else:
            self.scheduler()


    def request(self, resource, size):
        if resource > 3 or resource < 0:
            raise RequestANonExistentResourceError
        
        current_process = self.get_current_process()
        if current_process == 0:
            raise Process0RequestingAResourceError

        # if resource in self.pcb[current_process].resources:
        #     raise RequestAResourceProcessAlreadyHolding

        # if (resource, size) in self.pcb[current_process].resources:
        #     raise RequestAResourceProcessAlreadyHolding 

        if len(self.pcb[current_process].resource_counter[resource]) != 0:
            if resource == 0 or resource == 1:
                if (resource, size) in self.pcb[current_process].resources:
                    raise RequestAResourceProcessAlreadyHolding
            if resource == 2 and \
                sum(self.pcb[current_process].resource_counter[resource]) == 2:
                raise RequestAResourceProcessAlreadyHolding
            if resource == 3 and \
                sum(self.pcb[current_process].resource_counter[resource]) == 3:
                raise RequestAResourceProcessAlreadyHolding


        if size == 0:
            raise SizeOfUnitsIsZeroError

        if size > self.rcb[resource].inventory:
            raise RequestedSizeTooBigError

        if (self.rcb[resource].current_state >= size and \
            self.rcb[resource].waitlist == []):
            self.rcb[resource].current_state -= size
            self.pcb[current_process].add_resource((resource, size))
            self.pcb[current_process].resource_counter[resource].append(size)
            if self.debugging == 1:
                print("* resource ", resource, " allocated")
            self.scheduler()
        else:
            prior = self.pcb[current_process].priority
            self.pcb[current_process].set_state(0)
            self.rl[prior].remove(current_process)
            self.rcb[resource].add_to_waitlist((current_process, size))
            if self.debugging == 1:
                print("* process ", current_process, " blocked")
                self.scheduler()
            else:
                self.scheduler()

    def release(self, resource, size):
        if resource > 3 or resource < 0:
            raise RequestANonExistentResourceError

        current_process = self.get_current_process()
        if (resource, size) not in self.pcb[current_process].resources:
            if size < sum(self.pcb[current_process].resource_counter[resource]) and \
                len(self.pcb[current_process].resource_counter[resource]) == 1:
                count = size 
                while count != 0:
                    m = self.pcb[current_process].resource_counter[resource][0]
                    self.pcb[current_process].remove_resource((resource, m))
                    self.pcb[current_process].resource_counter[resource].remove(m)
                    self.rcb[resource].current_state += size
                    m -= size
                    self.pcb[current_process].add_resource((resource, m))
                    self.pcb[current_process].resource_counter[resource].append(m)
                    count -= size

            elif size <= sum(self.pcb[current_process].resource_counter[resource]) and \
                sum(self.pcb[current_process].resource_counter[resource]) != 0:
                count = size
                while count != 0:
                    m = max(self.pcb[current_process].resource_counter[resource])
                    self.pcb[current_process].remove_resource((resource, m))
                    self.pcb[current_process].resource_counter[resource].remove(m)
                    count -= m
                    self.rcb[resource].current_state += m 
            else:
                raise IncorrectResourceSizePairError
        else:
            self.pcb[current_process].remove_resource((resource, size))
            self.pcb[current_process].resource_counter[resource].remove(size)
            self.rcb[resource].current_state += size
 
        if self.debugging == 1:
            print("* resource ", resource, " released")
        while (self.rcb[resource].waitlist != [] and self.rcb[resource].current_state > 0):
            next_process = self.rcb[resource].waitlist[0]
            if self.rcb[resource].current_state >= next_process[1]:
                self.rcb[resource].current_state -= next_process[1]
                self.pcb[next_process[0]].add_resource((resource, next_process[1]))
                self.pcb[next_process[0]].resource_counter[resource].append(next_process[1])
                self.pcb[next_process[0]].set_state(1)
                self.rcb[resource].remove_from_waitlist(next_process)
                prior = self.pcb[next_process[0]].priority
                self.rl[prior].append(next_process[0])
                if self.debugging == 1:
                    print("* process ", next_process[0], " got ", resource)
            else:
                break        
        self.scheduler()


    def timeout(self):
        '''
        move process i from the head of RL to end of RL
        scheduler()
        '''
        current_process = self.get_current_process()
        prior = self.pcb[current_process].priority
        self.rl[prior].append(self.rl[prior].pop(0))
        self.scheduler()

    def scheduler(self):
        '''
        find process i currently at the head of RL
        display: "process i running"
        '''
        current = self.get_current_process()
        if self.debugging == 1:
            print("* process ", current, " running")
        else:
            print(current, "", end='')

    ########################################################################
        
    def destroy_processes(self, index):
        count = 0
        process = self.pcb[index]
        priority = process.priority
        for i in range(len(process.children)):
            count += self.destroy_processes(process.children[0])

        if index != 0:
            parent = self.pcb[process.parent]
            parent.remove_child(index)
            
            '''check for waitlist also'''#########################
            if process.current_state == 1:
                self.rl[priority].remove(index)
            else:
                for i in range(self.rcb.fixed_size):
                    for j in range(len(self.rcb[i].waitlist)):
                        waiting = self.rcb[i].waitlist[j]
                        if waiting[0] == index:
                            self.rcb[i].waitlist.remove(waiting)
                            break
            '''release all resources of j'''######################
            for i in range(len(process.resources)):
                self.destroy_release(process.resources[0], index)
            
            self.pcb[index] = None
            self.pcb.count -= 1
            return count + 1
        else:
            return count          
            

    def get_current_process(self):
        for i in range(self.rl.fixed_size - 1, -1, -1):
            for j in self.rl[i]:
                return j

        print("get_current_process failed")
        return -1

    def destroy_release(self, pair, index):
        resource = pair[0]
        size = pair[1]
        current_process = index

        self.pcb[current_process].remove_resource((resource, size))
        self.pcb[current_process].resource_counter[resource].remove(size)
        self.rcb[resource].current_state += resource

        if self.debugging == 1:
            print("* d_resource ", resource, " released")
        
        while (self.rcb[resource].waitlist != [] and self.rcb[resource].current_state > 0):
            next_process = self.rcb[resource].waitlist[0]
            if self.rcb[resource].current_state >= next_process[1]:
                self.rcb[resource].current_state -= next_process[1]
                self.pcb[next_process[0]].add_resource((resource, next_process[1]))
                self.pcb[next_process[0]].resource_counter[resource].append(next_process[1])
                self.pcb[next_process[0]].set_state(1)
                self.rcb[resource].remove_from_waitlist(next_process)
                prior = self.pcb[next_process[0]].priority
                self.rl[prior].append(next_process[0])

                if self.debugging == 1:
                    print("* d_process ", next_process[0], " got ", resource)
            else:
                break