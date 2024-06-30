from datetime import datetime
import psutil


def get_users_processes() -> dict:
    users_processes = {}
    for p in psutil.process_iter(["name", "username"]):
        users_processes.setdefault(p.info["username"], 0)
        users_processes[p.info["username"]] += 1
    return users_processes


def get_process_with_max_value(atr: str):
    return sorted(
        psutil.process_iter(["name", atr]),
        key=lambda e: sum(e.info[atr][:2]) if e.info[atr] else 0,
        reverse=True,
    )[0].info["name"][:20]


if __name__ == "__main__":
    scan_date = datetime.now().replace(second=0, microsecond=0)
    users_processes = get_users_processes()
    processes_count = sum(1 for proc in psutil.process_iter())
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    process_with_max_memory_usage = get_process_with_max_value("memory_info")
    process_with_max_cpu_usage = get_process_with_max_value("cpu_times")

    print("Отчёт о состоянии системы:")
    print(f"Пользователи системы: {', '.join(user for user in users_processes.keys())}")
    print(f"Процессов запущено: {processes_count}")
    print("\nПользовательских процессов:")
    for k, v in sorted(users_processes.items(), key=lambda item: item[1], reverse=True):
        print(f"{k}:{v}")
    print(f"\nВсего памяти используется: {memory_usage}%")
    print(f"Всего CPU используется: {cpu_usage}%")
    print(f"Больше всего памяти использует: {process_with_max_memory_usage}")
    print(f"Больше всего CPU использует: {process_with_max_cpu_usage}")
    with open(f"{scan_date}-scan.txt", "a") as log_file:
        log_file.write("Отчёт о состоянии системы:\n")
        log_file.write(
            f"Пользователи системы: {', '.join(user for user in users_processes.keys())}\n"
        )
        log_file.write(f"Процессов запущено: {processes_count}\n")
        log_file.write("\nПользовательских процессов:\n")
        for k, v in sorted(
            users_processes.items(), key=lambda item: item[1], reverse=True
        ):
            log_file.write(f"{k}:{v}\n")
        log_file.write(f"\nВсего памяти используется: {memory_usage}%\n")
        log_file.write(f"Всего CPU используется: {cpu_usage}%\n")
        log_file.write(
            f"Больше всего памяти использует: {process_with_max_memory_usage}\n"
        )
        log_file.write(f"Больше всего CPU использует: {process_with_max_cpu_usage}")
