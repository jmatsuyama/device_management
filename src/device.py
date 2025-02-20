class Device:
    def __init__(self, location_name, pc_id, replacement_flag, status="Preparing", release_deadline=None):
        self.id = id(self)
        self.location_name = location_name
        self.pc_id = pc_id
        self.replacement_flag = replacement_flag
        self.status = status
        self.release_deadline = release_deadline

    def __str__(self):
        return f"ID: {self.id}, Location: {self.location_name}, PC/ID: {self.pc_id}, Replacement: {self.replacement_flag}, Status: {self.status}, Release Deadline: {self.release_deadline}"
