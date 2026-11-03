class RealmDecomposer:
    def decompose(self, task, chunk_size=3):
        lines = [l.strip() for l in task.splitlines() if l.strip()]
        return [" ".join(lines[i:i+chunk_size]) for i in range(0, len(lines), chunk_size)]
