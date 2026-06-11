def FIFO(processes, frame_size):
    tracker = [[-1] * frame_size for _ in range(len(processes))]
    replace = 0
    page_fault = 0

    for i, process in enumerate(processes):
        if i >= 1:
            tracker[i] = list(tracker[i - 1])

        if process not in tracker[i]:
            page_fault += 1
            tracker[i][replace] = process
            replace = (replace + 1) % frame_size

    return {
        "steps": tracker,
        "processes": processes,
        "page_faults": page_fault,
        "fault_rate": round(page_fault / len(processes) * 100, 1)
    }