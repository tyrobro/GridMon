import multiprocessing
import time
import os


def attack_core(x):
    print(f"Core {x} under attack!", flush=True)
    while True:
        _ = 21341 * 21341


if __name__ == "__main__":
    cores = multiprocessing.cpu_count()
    print(f"WARNING: Attacking all {cores} cores.")
    print(" Press CTRL+C immediately to stop.")
    time.sleep(2)

    with multiprocessing.Pool(cores) as p:
        try:
            p.map(attack_core, range(cores))
        except KeyboardInterrupt:
            print("\n🛑 Attack stopped.")
