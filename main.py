from itertools import product, islice
import string
import multiprocessing
import time

class BruteForce():
    def __init__(self) -> None:
        pass

    def start(self, type: str, pwd) -> str:
        if type == 'multi':
            self.break_password(string.printable, pwd, len(pwd))
        elif type == 'single':
            self.simple_brute_force(pwd)


    def gera_lst(self, chars):
        lst = []
        for i in chars:
            k = [i + chars]
            j = dict.fromkeys(k[0]).keys()
            j = list(j)
            lst.append([''.join(j)])
        return lst

    def split(self, a, n):
        k, m = divmod(len(a), n)
        return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

    def brute_force(self, password, chars, max_attempts, rpt, pct):
        # print(max_attempts)
        attempts = 0
        for v in islice(product(chars, repeat=rpt), max_attempts):
            attempts += 1
            if (attempts%50_00_000) == 0:
                print(
                    f'\r| length_percentage = {pct} \ chunk_percentage =  {((attempts/(max_attempts))):.0%} \ {attempts = } \ {max_attempts = }'
                    , end=''
                )
            if ''.join(v) == password:
                print('\n PASSWROD: ', v)
                return v

    def gen_tries(self, lst, rpt, password, pct):
        max_tries = len(lst) ** (rpt-1)
        return self.brute_force(password, lst, max_tries, rpt, pct)

    def do_job(self, lsts, length_try, password):
        s = time.time()
        # print(len(lsts))
        for k, lst in enumerate(lsts):
            pct = f'{((k+1)/len(lsts)):.0%}'
            response = self.gen_tries(str(lst[0]), length_try + 1, password, pct)
            if response:
                e = time.time()
                print(f'{e-s:.2f} seconds')
                return response

    def break_password(self, chars, password, max_length_tries):
        lsts = self.gera_lst(chars)
        for length_try in range(0, max_length_tries):
            print('\n' + str(length_try+1))
            pool_of_lists = list(self.split(lsts, 6))
            process_list = []
            for pool in pool_of_lists:
                p = multiprocessing.Process(target=self.do_job, args=(pool, length_try, password))
                process_list.append(p)
                p.start()
            for process in process_list:
                process.join()
        print('FINAL')

    def simple_brute_force(self, password):
        chars = string.printable
        for length in range(1, 10):
            attempts = 0
            trys = product(chars, repeat=length)
            len_trys = len(chars)**length
            for i in trys:
                attempts += 1
                if (attempts%1_000_000) == 0:
                    print(f'\r {length = }| {((attempts/len_trys)):.2%} | {attempts = } | {len_trys = }', end='')
                if ''.join(i) == password:
                    return f"Tua senha é: '{''.join(i)}'."

# if __name__ == "__main__":
#     pwd = 'abcde'
#     print(break_password(string.printable, pwd, len(pwd)))
    

if __name__ == "__main__":
    bf = BruteForce()
    # bf.start(type='single', pwd='abcde')
    bf.start(type='multi', pwd='abcde')