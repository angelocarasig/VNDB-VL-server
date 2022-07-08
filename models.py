from vndb_thigh_highs import VNDB
from vndb_thigh_highs.models import VN, UserVN
import time
import threading

class ElapsedTimeThread(threading.Thread):
    """"Stoppable thread that prints the time elapsed"""
    def __init__(self):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        thread_start = time.time()

        while not self.stopped():
            print("\rElapsed Time {:.3f} seconds".format(time.time()-thread_start), end="")
            #include a delay here so the thread doesn't uselessly thrash the CPU
            time.sleep(0.01)


def load_user_data(userID, debug=True) -> dict:
    thread = ElapsedTimeThread()
    thread.start()
    vndb = VNDB()
    start_time = time.time()
    user_vn_data = []             #Data stored in here will be converted to a json

    # Get initial user data
    user = vndb.get_all_ulist(UserVN.user_id == userID)


    # Get all VN Data

    vns = []
    for i in user:
        vns.append(i.vn_id)

    try:
        vns = vndb.get_all_vn(VN.id == vns)
    except:
        end_time = time.time()
        thread.stop()
        thread.join()
        print(f"\nProcessing Time: {end_time - start_time:.10f}\n")
        raise Exception("User ID Invalid.")

    for user_data, vn_data in zip(user, vns):
        entry = {}
        entry.update(vars(user_data))
        entry.update(vars(vn_data))

        # Only popping unmanaged objects right now, maybe manage properly later

        # entry.pop('screens')
        entry.pop('tags')
        entry.pop('staff')
        # entry.pop('labels')
        # entry.pop('image_flagging')
        entry.pop('links')
        entry.pop('relations')
        entry.pop('length')
        entry.pop('anime')
        
        ### IMAGE FLAGGING
        screens = []
        for screenshot in entry['screens']:
            screen_data = {}
            screen_data['image'] = screenshot.image
            screen_data['flag'] = screenshot.flagging.sexual_avg + screenshot.flagging.violence_avg
            screens.append(screen_data)
        
        entry['screens'] = screens

        entry['image_flag'] = entry['image_flagging'].sexual_avg
        entry.pop('image_flagging')
        ### IMAGE FLAGGING

        user_vn_labels = []
        for labels in entry['labels']:
            user_vn_labels.append(labels.name)
        
        entry['labels'] = user_vn_labels

        added_date = entry['added_date'].strftime("%d/%m/%Y")
        last_mod_date = entry['last_modification_date'].strftime("%d/%m/%Y")
        
        entry['added_date'] = added_date
        entry['last_modification_date'] = last_mod_date
        
        if entry['voted_date'] != None:
            voted_date = entry['voted_date'].strftime("%d/%m/%Y")
            entry['voted_date'] = voted_date

        user_vn_data.append(entry)

    end_time = time.time()
    thread.stop()
    thread.join()
    if debug:
        print(f"Processing Time: {end_time - start_time:.10f}\n")

    return user_vn_data