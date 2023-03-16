import time
import requests

def get_time_difference(url):

    # Mengembalikan selisih waktu antara server web publik dan sistem lokal dalam detik.

    response = requests.head(url, allow_redirects=True)
    web_time = response.headers.get('date')
    web_time = time.strptime(web_time, '%a, %d %b %Y %H:%M:%S %Z')
    web_time_in_seconds = time.mktime(web_time)
    local_time_in_seconds = time.time()
    return web_time_in_seconds - local_time_in_seconds

def synchronize_time(url):
    # Menyesuaikan waktu sistem lokal dengan waktu server web publik menggunakan algoritma Berkeley.

    # Mendapatkan waktu lokal
    local_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime())
    print(f'Waktu lokal: {local_time}')

    # Mendapatkan waktu web publik
    web_time_difference = get_time_difference(url)
    web_time = time.localtime(time.time() + web_time_difference)
    print(f'Waktu web publik: {time.strftime("%a, %d %b %Y %H:%M:%S %Z", web_time)}')

    # Mendapatkan selisih waktu dari setiap mesin
    time_differences = []
    for i in range(3):
        time_difference = get_time_difference(url)
        time_differences.append(time_difference)

    # Menghitung rata-rata selisih waktu
    avg_time_difference = sum(time_differences) / len(time_differences)
    print(f'Selisih waktu: {avg_time_difference} detik')

    # Menyesuaikan waktu setiap mesin dengan rata-rata selisih waktu
    for i in range(3):
        corrected_time = time.time() + (avg_time_difference - time_differences[i])
        print(f'Waktu mesin {i+1} yang disesuaikan: {time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(corrected_time))}')

if __name__ == '__main__':
    url = 'https://www.instagram.com'
    synchronize_time(url)

# Hasilnya :
# Waktu lokal: Thu, 16 Mar 2023 21:25:18 SE Asia Standard Time
# Waktu web publik: Thu, 16 Mar 2023 14:25:19 SE Asia Standard Time
# Selisih waktu: -25200.564603249233 detik
# Waktu mesin 1 yang disesuaikan: Thu, 16 Mar 2023 14:25:20 SE Asia Standard Time
# Waktu mesin 2 yang disesuaikan: Thu, 16 Mar 2023 14:25:20 SE Asia Standard Time
# Waktu mesin 3 yang disesuaikan: Thu, 16 Mar 2023 14:25:20 SE Asia Standard Time
